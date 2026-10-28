"""Text protocol: one UTF-8 message per line, one request per connection."""
import socket
from config import NAME_SERVER, TIMEOUT, MAX_MESSAGE


def encode(text):
    return (text + "\n").encode("utf-8")


def receive_line(connection):
    # TCP may deliver a message in multiple chunks.
    data = bytearray()
    while len(data) <= MAX_MESSAGE:
        part = connection.recv(1)
        if not part:
            raise ValueError("Connection closed before the end of the line")
        if part == b"\n":
            return data.decode("utf-8").strip()
        data.extend(part)
    raise ValueError("Message too long")


def tcp_request(address, message):
    with socket.create_connection(address, timeout=TIMEOUT) as connection:
        connection.sendall(encode(message))
        return receive_line(connection)


def register(name, address):
    response = tcp_request(NAME_SERVER, f"REGISTER {name} {address[0]} {address[1]}")
    if response != "OK":
        raise ValueError(f"Registration failed: {response}")


def lookup(name):
    response = tcp_request(NAME_SERVER, f"LOOKUP {name}")
    parts = response.split()
    if len(parts) != 3 or parts[0] != "OK":
        raise ValueError(f"Service lookup failed: {response}")
    return parts[1], int(parts[2])