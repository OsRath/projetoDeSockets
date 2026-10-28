"""Shared interface and timing measurements for both clients."""
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
    address = lookup(service)  # Always resolve the service address dynamically!
    kind = socket.SOCK_STREAM if transport == "TCP" else socket.SOCK_DGRAM
    with socket.socket(socket.AF_INET, kind) as connection:
        connection.settimeout(TIMEOUT)
        # With UDP, connect only selects the peer; there is no handshake.
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
        raise ValueError(f"Unexpected server response: {response}")
    print(f"You: {parts[1]} | Server: {parts[2]} | Result: {parts[3]}")
    print(
        f"Request/response: {elapsed:.3f} ms | "
        f"Total including lookup/connection: {total:.3f} ms"
    )


def main(transport):
    parser = argparse.ArgumentParser(
        description=f"Rock, Paper, Scissors over {transport}"
    )
    parser.add_argument("choice", nargs="?", choices=CHOICES)
    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="Number of rounds using the same choice",
    )
    parser.add_argument(
        "--csv",
        help="Write measurements to this CSV file (overwrites existing file)",
    )
    args = parser.parse_args()
    if args.repeat < 1 or (
        args.choice is None and (args.repeat != 1 or args.csv)
    ):
        parser.error(
            "Specify a choice when using --repeat/--csv; "
            "--repeat must be positive."
        )
    rows = []

    def run(choice):
        response, elapsed, total = request(transport, choice)
        show(response, elapsed, total)
        rows.append(
            (transport, len(rows) + 1, choice, response, elapsed, total)
        )

    try:
        if args.choice:
            for _ in range(args.repeat):
                run(args.choice)
        else:
            while True:
                choice = input(
                    f"\nChoose {', '.join(CHOICES)}, or q to quit: "
                ).strip().lower()
                if choice in ("q", "quit", "exit"):
                    break
                if choice not in CHOICES:
                    print(f"Please enter one of: {', '.join(CHOICES)}.")
                    continue
                run(choice)
    except (OSError, ValueError) as error:
        print(
            f"Error: {error}. Are all servers running? "
            "With UDP, a response may not arrive."
        )
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\nGame ended.")
    if rows:
        print(
            f"\n{len(rows)} rounds; "
            f"average request time: "
            f"{statistics.mean(r[4] for r in rows):.3f} ms"
        )
    if args.csv:
        try:
            with open(args.csv, "w", newline="", encoding="utf-8") as output:
                writer = csv.writer(output)
                writer.writerow(
                    (
                        "transport",
                        "round",
                        "choice",
                        "response",
                        "request_ms",
                        "total_ms",
                    )
                )
                writer.writerows(rows)
            print(f"Measurements saved: {args.csv}")
        except OSError as error:
            print(f"Could not save CSV file: {error}")
            return 1
    return 0