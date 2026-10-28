"""UDP-Spielserver: ein Datagramm enthaelt genau eine Spielanfrage."""
import socket
from concurrent.futures import ThreadPoolExecutor
from config import UDP_ADDRESS, UDP_SERVICE, MAX_MESSAGE
from protocol import register, encode
from game import play


def handle(server, data, address):
    try:
        if len(data) > MAX_MESSAGE:
            response = "ERROR message_too_long"
        else:
            try:
                response = play(data.decode("utf-8").strip())
            except UnicodeError:
                response = "ERROR invalid_encoding"
        server.sendto(encode(response), address)
    except OSError as error:
        print(f"UDP-Fehler: {error}", flush=True)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind(UDP_ADDRESS)
        register(UDP_SERVICE, UDP_ADDRESS)
        print(f"UDP-Spielserver bereit: {UDP_ADDRESS}", flush=True)
        with ThreadPoolExecutor(max_workers=8) as workers:
            while True:
                data, address = server.recvfrom(MAX_MESSAGE + 1)
                workers.submit(handle, server, data, address)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nUDP-Spielserver beendet.")
    except (OSError, ValueError) as error:
        print(f"Startfehler: {error}. Laeuft der Namensserver?")
        raise SystemExit(1)