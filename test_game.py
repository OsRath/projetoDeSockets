import unittest
from unittest.mock import patch
from game import play, winner


class GameTests(unittest.TestCase):
    def test_all_nine_results(self):
        cases = [
            ("schere", "schere", "unentschieden"),
            ("schere", "stein", "verloren"),
            ("schere", "papier", "gewonnen"),
            ("stein", "schere", "gewonnen"),
            ("stein", "stein", "unentschieden"),
            ("stein", "papier", "verloren"),
            ("papier", "schere", "verloren"),
            ("papier", "stein", "gewonnen"),
            ("papier", "papier", "unentschieden"),
        ]
        for player, server, expected in cases:
            with self.subTest(player=player, server=server):
                self.assertEqual(winner(player, server), expected)
                with patch("game.random.choice", return_value=server):
                    self.assertEqual(play(f"PLAY {player}"), f"OK {player} {server} {expected}")

    def test_invalid_requests(self):
        for message in ("", "PLAY", "PLAY wasser", "DELETE stein", "PLAY stein papier"):
            self.assertTrue(play(message).startswith("ERROR "))


if __name__ == "__main__":
    unittest.main()