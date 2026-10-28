import unittest
from unittest.mock import patch
from game import play, winner


class GameTests(unittest.TestCase):
    def test_all_nine_results(self):
        cases = [
            ("scissors", "scissors", "equal"),
            ("scissors", "rock", "lost"),
            ("scissors", "paper", "won"),
            ("rock", "scissors", "won"),
            ("rock", "rock", "equal"),
            ("rock", "paper", "lost"),
            ("paper", "scissors", "lost"),
            ("paper", "rock", "won"),
            ("paper", "paper", "equal"),
        ]
        for player, server, expected in cases:
            with self.subTest(player=player, server=server):
                self.assertEqual(winner(player, server), expected)
                with patch("game.random.choice", return_value=server):
                    self.assertEqual(
                        play(f"PLAY {player}"),
                        f"OK {player} {server} {expected}",
                    )

    def test_invalid_requests(self):
        for message in (
            "",
            "PLAY",
            "PLAY water",
            "DELETE rock",
            "PLAY rock paper",
        ):
            self.assertTrue(play(message).startswith("ERROR "))


if __name__ == "__main__":
    unittest.main()