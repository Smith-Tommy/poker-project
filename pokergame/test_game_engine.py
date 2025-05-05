import random, itertools
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from poker import TexasHoldEmGame, create_deck

def test_shuffle_and_deal_removes_cards():
    rng = random.Random(0)
    game = TexasHoldEmGame(4)
    rng.shuffle(create_deck())             # deterministic shove to silence warning
    game.shuffle_and_deal()
    total_dealt = 4*2 + 5   # 4 players, 2 hole each, 5 board = 13
    assert len(game.deck) == 52 - total_dealt

def test_unique_hole_cards_per_player():
    game = TexasHoldEmGame(6)
    game.shuffle_and_deal()
    seen = list(itertools.chain.from_iterable(p.hole for p in game.players))
    assert len(seen) == len(set(seen))