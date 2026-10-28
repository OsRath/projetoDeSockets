"""Textprotokoll: eine UTF-8-Nachricht pro Zeile, eine Anfrage pro Verbindung."""
import socket
from config import NAME_SERVER, TIMEOUT, MAX_MESSAGE


def encode(text):
    return (text + "\n").encode("utf-8")


def receive_line(connection):
    # TCP kann eine Nachricht in mehrere Pakete zerlegen.
    data = bytearray()
    while len(data) <= MAX_MESSAGE:
        part = connection.recv(1)
        if not part:
            raise ValueError("Verbindung vor dem Zeilenende geschlossen")
        if part == b"\n":
            return data.decode("utf-8").strip()
        data.extend(part)
    raise ValueError("Nachricht zu lang")


def tcp_request(address, message):
    with socket.create_connection(address, timeout=TIMEOUT) as connection:
        connection.sendall(encode(message))
        return receive_line(connection)


def register(name, address):
    response = tcp_request(NAME_SERVER, f"REGISTER {name} {address[0]} {address[1]}")
    if response != "OK":
        raise ValueError(f"Registrierung fehlgeschlagen: {response}")


def lookup(name):
    response = tcp_request(NAME_SERVER, f"LOOKUP {name}")
    parts = response.split()
    if len(parts) != 3 or parts[0] != "OK":
        raise ValueError(f"Dienstsuche fehlgeschlagen: {response}")
    return parts[1], int(parts[2])