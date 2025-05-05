import itertools
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from poker import Card, create_deck, RANK_ORDER, SUITS

def test_card_ordering():
    low, high = Card("2", "♠"), Card("A", "♠")
    assert low < high

def test_deck_has_52_unique_cards():
    deck = create_deck()
    assert len(deck) == 52
    assert len(set(deck)) == 52
    for r, s in itertools.product(RANK_ORDER, SUITS):
        assert Card(r, s) in deck