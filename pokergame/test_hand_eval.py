import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from poker import (
    Card, score_five_cards, evaluate_7cards, HAND_RANKS, RANK_ORDER
)

def cv(rank):
    return RANK_ORDER.index(rank)

def make_hand(cards):
    return [Card(r, s) for r, s in cards]

def test_four_of_a_kind_beats_full_house():
    quads = make_hand([("A","♠"),("A","♥"),("A","♦"),("A","♣"),("K","♠")])
    full  = make_hand([("K","♠"),("K","♥"),("K","♦"),("Q","♠"),("Q","♥")])
    assert score_five_cards(quads) > score_five_cards(full)

def test_straight_flush_identified():
    sf = make_hand([("9","♥"),("T","♥"),("J","♥"),("Q","♥"),("K","♥")])
    cat, *_ = score_five_cards(sf)
    assert HAND_RANKS[cat] == "Straight Flush"

def test_best_of_seven():
    seven = make_hand([
        ("A","♠"),("A","♥"), 
        ("A","♦"),("K","♣"),("K","♠"),
        ("2","♣"),
        ("3","♦") 
    ])
    best = evaluate_7cards(seven)
    assert best.category == "Full House"