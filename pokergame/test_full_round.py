import random
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from poker import TexasHoldEmGame

def test_round_winner_deterministic(monkeypatch):
    rng = random.Random(42)
    monkeypatch.setattr("poker.poker.random", rng)   # inject deterministic RNG
    game = TexasHoldEmGame(3)
    game.shuffle_and_deal()
    game.evaluate_players()
    winners = game.winners()
    # The snapshot below is stable because RNG is fixed
    assert [w.name for w in winners] == ["P1"]