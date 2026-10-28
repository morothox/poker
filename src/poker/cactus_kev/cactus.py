import json
from itertools import combinations, combinations_with_replacement
import os
from random import sample

# Suits: 0=CLUB, 1=DIAMOND, 2=HEART, 3=SPADE
Suits = [0, 1, 2, 3]
# Ranks: 0="2" ... 8="10", 9="J", 10="Q", 11="K", 12="A"
Ranks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# PRIMES[rank] = Primzahl fuer den Rank-Index (0="2" -> 2, ..., 12="A" -> 41)
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

arrays_dir = os.path.join(os.path.dirname(__file__), "arrays")

with open(os.path.join(arrays_dir, "flushes.json"), "r") as f:
    flushes = json.load(f)

with open(os.path.join(arrays_dir, "unique5.json"), "r") as f:
    unique5 = json.load(f)

with open(os.path.join(arrays_dir, "primes.json"), "r") as f:
    # JSON-Keys sind Strings -> einmal beim Laden in ints umwandeln
    primes = {int(k): v for k, v in json.load(f).items()}

# alle 21 Moeglichkeiten, 5 aus 7 Karten zu waehlen (als Indizes)
COMBOS_7 = list(combinations(range(7), 5))


class Card:
    def __init__(self, rank, suit):
        if rank not in Ranks:
            raise ValueError(f"rank muss 0-12 sein, war {rank}")
        if suit not in Suits:
            raise ValueError(f"suit muss 0-3 sein, war {suit}")
        self.rank = rank
        self.suit = suit
        # Bit-Darstellung nur einmal berechnen statt bei jeder Auswertung
        self.bit = self.make_bit()

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        else:
            return False

    def __repr__(self):
        return f"Card({self.rank}, {self.suit})"

    def make_bit(self):
        # xxxbbbbb bbbbbbbb cdhsrrrr xxpppppp
        rank_bit = 1 << self.rank
        suit_bit = 1 << self.suit
        rrrr = self.rank
        prime_bit = PRIMES[self.rank]

        fertiger_bit = prime_bit
        fertiger_bit |= rrrr << 8
        fertiger_bit |= suit_bit << 12
        fertiger_bit |= rank_bit << 16

        return fertiger_bit


class Evaluator:
    def __init__(self, c1, c2, c3, c4, c5):
        self.c1 = c1.bit
        self.c2 = c2.bit
        self.c3 = c3.bit
        self.c4 = c4.bit
        self.c5 = c5.bit

    def evaluate(self):
        return evaluate_5(self.c1, self.c2, self.c3, self.c4, self.c5)

    def prime(self):
        return (
            (self.c1 & 0xFF)
            * (self.c2 & 0xFF)
            * (self.c3 & 0xFF)
            * (self.c4 & 0xFF)
            * (self.c5 & 0xFF)
        )


def evaluate_5(c1, c2, c3, c4, c5):
    q = (c1 | c2 | c3 | c4 | c5) >> 16
    if c1 & c2 & c3 & c4 & c5 & 0xF000:
        return flushes[q]

    # unique5 ist 0, wenn nicht 5 verschiedene Ranks -> kein bin().count() noetig
    value = unique5[q]
    if value:
        return value

    return primes[(c1 & 0xFF) * (c2 & 0xFF) * (c3 & 0xFF) * (c4 & 0xFF) * (c5 & 0xFF)]


def compare(board, p1, p2):
    """Wil return 1 if p1 won and -1 if p2 won and 0 if a tie"""
    p1_score = evaluate_7_cards(board + p1)
    p2_score = evaluate_7_cards(board + p2)
    if p1_score < p2_score:
        return 1
    elif p1_score == p2_score:
        return 0
    else:
        return -1


def evaluate_7_cards(seven_cards):
    b = [card.bit for card in seven_cards]
    best_score = 7463
    for i1, i2, i3, i4, i5 in COMBOS_7:
        value = evaluate_5(b[i1], b[i2], b[i3], b[i4], b[i5])
        if value < best_score:
            best_score = value
    return best_score


N = 100000


def monte_carlo(deck, hero, villain):
    hero_won = 0
    villain_won = 0
    tie = 0

    for i in range(N):
        board = sample(deck, 5)
        villain_hand = board + villain
        hero_hand = board + hero
        villain_score = evaluate_7_cards(villain_hand)
        hero_score = evaluate_7_cards(hero_hand)
        if villain_score < hero_score:
            villain_won += 1
        elif villain_score > hero_score:
            hero_won += 1
        else:
            tie += 1
    hero_equity = (hero_won + 0.5 * tie) / N * 100
    return hero_equity


if __name__ == "__main__":
    c1 = Card(9, 2)
    c2 = Card(9, 1)
    c3 = Card(9, 0)
    c4 = Card(11, 3)
    c5 = Card(7, 2)
    c6 = Card(12, 1)
    c7 = Card(10, 0)
    seven = [c1, c2, c3, c4, c5, c6, c7]

    test = evaluate_7_cards(seven)

    hero = [Card(12, 3), Card(11, 3)]
    villain = [Card(11, 0), Card(11, 2)]

    deck = [Card(rank, suit) for rank in Ranks for suit in Suits]
    deck.remove(hero[0])
    deck.remove(villain[0])
    deck.remove(hero[1])
    deck.remove(villain[1])

    print(len(deck))

    test = monte_carlo(deck, hero, villain)
    print(test)
