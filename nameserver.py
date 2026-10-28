"""Zentrales Adressbuch; Registrierung und Suche laufen ueber TCP."""
import ipaddress
import re
import socket
import threading
from config import NAME_SERVER, TIMEOUT
from protocol import encode, receive_line

services = {}
lock = threading.Lock()


def process(message):
    parts = message.split()
    if len(parts) == 4 and parts[0] == "REGISTER":
        _, name, host, port_text = parts
        try:
            ipaddress.IPv4Address(host)
            port = int(port_text)
            if not 1024 <= port <= 65535 or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", name):
                raise ValueError()
        except ValueError:
            return "ERROR invalid_registration"
        with lock:
            services[name] = (host, port)
        print(f"Registered: {name} -> {host}:{port}", flush=True)
        return "OK"
    if len(parts) == 2 and parts[0] == "LOOKUP":
        with lock:
            address = services.get(parts[1])
        if address is None:
            return "ERROR service_not_found"
        return f"OK {address[0]} {address[1]}"
    return "ERROR invalid_command"


def handle(connection):
    with connection:
        connection.settimeout(TIMEOUT)
        try:
            try:
                response = process(receive_line(connection))
            except (ValueError, UnicodeError):
                response = "ERROR invalid_message"
            connection.sendall(encode(response))
        except OSError as error:
            print(f"Connection error: {error}", flush=True)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(NAME_SERVER)
        server.listen()
        print(f"Nameserver ready: {NAME_SERVER}", flush=True)
        while True:
            connection, _ = server.accept()
            threading.Thread(target=handle, args=(connection,), daemon=True).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nNamensserver stopped.")
    except OSError as error:
        print(f"Startingerror: {error}")
        raise SystemExit(1)