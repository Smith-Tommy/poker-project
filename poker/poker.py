from __future__ import annotations

import itertools
import random
from collections import Counter
from typing import List, Tuple, Dict, NamedTuple

RANK_ORDER = "23456789TJQKA"
SUITS = "♠♥♦♣"

class Card(NamedTuple):
    rank: str 
    suit: str 

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __lt__(self, other: "Card") -> bool:
        return RANK_ORDER.index(self.rank) < RANK_ORDER.index(other.rank)


def create_deck() -> List[Card]:
    return [Card(r, s) for r in RANK_ORDER for s in SUITS]

HAND_RANKS = {
    9: "Straight Flush",
    8: "Four of a Kind",
    7: "Full House",
    6: "Flush",
    5: "Straight",
    4: "Three of a Kind",
    3: "Two Pair",
    2: "One Pair",
    1: "High Card",
}


class EvaluatedHand(NamedTuple):
    score: Tuple[int, List[int]]
    best_five: List[Card]

    @property
    def category(self) -> str:
        return HAND_RANKS[self.score[0]]


def card_value(card: Card) -> int:
    return RANK_ORDER.index(card.rank)


def is_straight(ranks: List[int]) -> Tuple[bool, int]:
    wheel = [0, 1, 2, 3, 12]
    if ranks[-4:] + [ranks[0]] == wheel:  
        return True, 3 

    for i in range(len(ranks) - 4):
        window = ranks[i : i + 5]
        if window == list(range(window[0], window[0] + 5)):
            return True, window[-1]
    return False, -1


def evaluate_7cards(cards: List[Card]) -> EvaluatedHand:
    best_score: Tuple[int, List[int]] | None = None
    best_hand: List[Card] | None = None

    for five in itertools.combinations(cards, 5):
        score = score_five_cards(list(five))
        if best_score is None or score > best_score:
            best_score = score
            best_hand = list(five)
    return EvaluatedHand(best_score, sorted(best_hand, reverse=True)) 


def score_five_cards(cards: List[Card]) -> Tuple[int, List[int]]:
    """Return a sortable score tuple for exactly five cards."""
    ranks = sorted((card_value(c) for c in cards), reverse=True)
    rank_counter = Counter(ranks)
    counts = sorted(rank_counter.values(), reverse=True)
    suits = [c.suit for c in cards]
    flush = len(set(suits)) == 1

    unique_ranks = sorted(set(ranks))
    ace_low_ranks = [0 if r == 12 else r + 1 for r in unique_ranks] 
    straight, high_st = is_straight(unique_ranks) or is_straight(ace_low_ranks)

    if straight and flush:
        return 9, [high_st]
    if counts[0] == 4:
        four_rank = rank_counter.most_common(1)[0][0]
        kicker = max(r for r in ranks if r != four_rank)
        return 8, [four_rank, kicker]
    if counts[0] == 3 and counts[1] == 2:
        triple = rank_counter.most_common(1)[0][0]
        pair = next(r for r, c in rank_counter.items() if c == 2)
        return 7, [triple, pair]
    if flush:
        return 6, ranks
    if straight:
        return 5, [high_st]
    if counts[0] == 3:
        triple = rank_counter.most_common(1)[0][0]
        kickers = sorted([r for r in ranks if r != triple], reverse=True)
        return 4, [triple] + kickers
    if counts[0] == 2 and counts[1] == 2:
        pairs = [r for r, c in rank_counter.items() if c == 2]
        high_pair, low_pair = sorted(pairs, reverse=True)
        kicker = next(r for r in ranks if r != high_pair and r != low_pair)
        return 3, [high_pair, low_pair, kicker]
    if counts[0] == 2:
        pair = rank_counter.most_common(1)[0][0]
        kickers = sorted([r for r in ranks if r != pair], reverse=True)
        return 2, [pair] + kickers
    return 1, ranks

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hole: List[Card] = []
        self.best: EvaluatedHand | None = None


class TexasHoldEmGame:
    def __init__(self, num_players: int):
        if not (2 <= num_players <= 6):
            raise ValueError("This demo supports 2–6 players only.")
        self.players: List[Player] = [Player(f"P{i + 1}") for i in range(num_players)]
        self.deck: List[Card] = []
        self.board: List[Card] = [] 

    def shuffle_and_deal(self):
        self.deck = create_deck()
        random.shuffle(self.deck)

        for p in self.players:
            p.hole.clear()
            p.best = None
        self.board.clear()

        for _ in range(2):
            for p in self.players:
                p.hole.append(self.deck.pop())
       
        self.deck.pop()
        self.board.extend(self._deal_n(3))
        
        self.deck.pop()
        self.board.extend(self._deal_n(1))
       
        self.deck.pop()
        self.board.extend(self._deal_n(1))

    def _deal_n(self, n: int) -> List[Card]:
        return [self.deck.pop() for _ in range(n)]

    def evaluate_players(self):
        for p in self.players:
            p.best = evaluate_7cards(p.hole + self.board)

    def winners(self) -> List[Player]:
        best_score = max(p.best.score for p in self.players)
        return [p for p in self.players if p.best.score == best_score]


def print_cards(cards: List[Card]):
    print(" ".join(str(c) for c in sorted(cards, reverse=True)))


def main():
    print("\n=== Texas Hold 'Em ===")
    while True:
        try:
            n = int(input("How many players? (2-6) ➜ ").strip())
            if 2 <= n <= 6:
                break
            raise ValueError
        except ValueError:
            print("Please enter a number from 2 to 6.")

    game = TexasHoldEmGame(n)
    play_again = True
    while play_again:
        game.shuffle_and_deal()
        game.evaluate_players()

        # Show hole cards
        print("\n--- Hole cards ---")
        for p in game.players:
            print(f"{p.name}: ", end="")
            print_cards(p.hole)

        # Show board
        print("\n--- Board ---")
        print("Flop:  ", end=""); print_cards(game.board[:3])
        print("Turn:  ", end=""); print_cards(game.board[:4])
        print("River: ", end=""); print_cards(game.board)

        # Showdown
        print("\n--- Showdown ---")
        for p in game.players:
            assert p.best is not None
            cat = p.best.category
            print(f"{p.name} → {cat:<15} | best 5: ", end="")
            print_cards(p.best.best_five)

        winners = game.winners()
        if len(winners) == 1:
            print(f"\nWinner: {winners[0].name} ({winners[0].best.category})")
        else:
            joined = ", ".join(w.name for w in winners)
            category = winners[0].best.category
            print(f"\nSplit pot between: {joined} ({category})")

        # Play again?
        replay = input("\nPlay another hand? [Y/n] ➜ ").strip().lower()
        play_again = replay in ("", "y", "yes")

    print("Thanks for playing – goodbye!")


if __name__ == "__main__":
    main()