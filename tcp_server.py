"""TCP-Spielserver: eigene Thread-Verarbeitung pro Client."""
import socket
import threading
from config import TCP_ADDRESS, TCP_SERVICE, TIMEOUT
from protocol import register, receive_line, encode
from game import play


def handle(connection):
    with connection:
        connection.settimeout(TIMEOUT)
        try:
            try:
                response = play(receive_line(connection))
            except (ValueError, UnicodeError):
                response = "ERROR invalid_message"
            connection.sendall(encode(response))
        except OSError as error:
            print(f"Verbindungsfehler: {error}", flush=True)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(TCP_ADDRESS)
        server.listen()
        register(TCP_SERVICE, TCP_ADDRESS)
        print(f"TCP-Spielserver bereit: {TCP_ADDRESS}", flush=True)
        while True:
            connection, _ = server.accept()
            threading.Thread(target=handle, args=(connection,), daemon=True).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTCP-Spielserver beendet.")
    except (OSError, ValueError) as error:
        print(f"Startfehler: {error}. Laeuft der Namensserver?")
        raise SystemExit(1)