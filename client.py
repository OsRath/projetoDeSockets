"""Gemeinsame Bedienung und Zeitmessung fuer beide Clients."""
import argparse
import csv
import socket
import statistics
import time
from config import TCP_SERVICE, UDP_SERVICE, TIMEOUT, MAX_MESSAGE
from protocol import lookup, encode, receive_line
from game import CHOICES


def request(transport, choice):
    start_total = time.perf_counter()
    service = TCP_SERVICE if transport == "TCP" else UDP_SERVICE
    address = lookup(service)  # Anwendungsadresse immer dynamisch ermitteln!
    kind = socket.SOCK_STREAM if transport == "TCP" else socket.SOCK_DGRAM
    with socket.socket(socket.AF_INET, kind) as connection:
        connection.settimeout(TIMEOUT)
        # Bei UDP waehlt connect nur den Gegenpart, es gibt keinen Handshake.
        connection.connect(address)
        start_request = time.perf_counter()
        connection.sendall(encode(f"PLAY {choice}"))
        if transport == "TCP":
            response = receive_line(connection)
        else:
            response = connection.recv(MAX_MESSAGE).decode("utf-8").strip()
        end = time.perf_counter()
    return response, (end - start_request) * 1000, (end - start_total) * 1000


def show(response, elapsed, total):
    parts = response.split()
    if len(parts) != 4 or parts[0] != "OK":
        raise ValueError(f"Unerwartete Serverantwort: {response}")
    print(f"Du: {parts[1]} | Server: {parts[2]} | Ergebnis: {parts[3]}")
    print(f"Anfrage/Antwort: {elapsed:.3f} ms | Gesamt inkl. Suche/Verbindung: {total:.3f} ms")


def main(transport):
    parser = argparse.ArgumentParser(description=f"Schere, Stein, Papier ueber {transport}")
    parser.add_argument("choice", nargs="?", choices=CHOICES)
    parser.add_argument("--repeat", type=int, default=1, help="Anzahl Runden mit fester Wahl")
    parser.add_argument("--csv", help="Messungen in diese CSV-Datei schreiben (ueberschreibt)")
    args = parser.parse_args()
    if args.repeat < 1 or (args.choice is None and (args.repeat != 1 or args.csv)):
        parser.error("Fuer --repeat/--csv eine Wahl angeben; --repeat muss positiv sein.")
    rows = []

    def run(choice):
        response, elapsed, total = request(transport, choice)
        show(response, elapsed, total)
        rows.append((transport, len(rows) + 1, choice, response, elapsed, total))

    try:
        if args.choice:
            for _ in range(args.repeat):
                run(args.choice)
        else:
            while True:
                choice = input("\nSchere, Stein, Papier oder q zum Beenden: ").strip().lower()
                if choice in ("q", "quit", "exit"):
                    break
                if choice not in CHOICES:
                    print("Bitte schere, stein oder papier eingeben.")
                    continue
                run(choice)
    except (OSError, ValueError) as error:
        print(f"Fehler: {error}. Sind alle Server gestartet? Bei UDP kann eine Antwort ausbleiben.")
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\nSpiel beendet.")
    if rows:
        print(f"\n{len(rows)} Runden; mittlere Anfragezeit: {statistics.mean(r[4] for r in rows):.3f} ms")
    if args.csv:
        try:
            with open(args.csv, "w", newline="", encoding="utf-8") as output:
                writer = csv.writer(output)
                writer.writerow(("transport", "round", "choice", "response", "request_ms", "total_ms"))
                writer.writerows(rows)
            print(f"Messungen gespeichert: {args.csv}")
        except OSError as error:
            print(f"CSV konnte nicht gespeichert werden: {error}")
            return 1
    return 0