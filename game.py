"""Gemeinsame Spiellogik fuer beide Server; keine Netzwerkfunktionen."""
import random

CHOICES = ("scissors", "rock", "paper")
BEATS = {"scissors": "paper", "rock": "scissors", "paper": "rock"}


def winner(player, server):
    if player == server:
        return "equal"
    return "won" if BEATS[player] == server else "lost"


def play(message):
    parts = message.lower().split()
    if len(parts) != 2 or parts[0] != "play" or parts[1] not in CHOICES:
        return "ERROR Benutze: PLAY scissors|rock|paper"
    player = parts[1]
    server = random.choice(CHOICES)
    return f"OK {player} {server} {winner(player, server)}"