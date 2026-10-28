"""Gemeinsame Spiellogik fuer beide Server; keine Netzwerkfunktionen."""
import random

CHOICES = ("schere", "stein", "papier")
BEATS = {"schere": "papier", "stein": "schere", "papier": "stein"}


def winner(player, server):
    if player == server:
        return "unentschieden"
    return "gewonnen" if BEATS[player] == server else "verloren"


def play(message):
    parts = message.lower().split()
    if len(parts) != 2 or parts[0] != "play" or parts[1] not in CHOICES:
        return "ERROR Benutze: PLAY schere|stein|papier"
    player = parts[1]
    server = random.choice(CHOICES)
    return f"OK {player} {server} {winner(player, server)}"