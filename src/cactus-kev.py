from typing import Tuple
from itertools import combinations
import importlib.util

_spec = importlib.util.spec_from_file_location("flush_array", "flush-array.py")
_flush_array = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_flush_array)
flushes = _flush_array.flushes
unique5 = _flush_array.unique5


Suits = ["CLUB", "DIAMOND", "Heart", "SPADE"]
Ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
flops = []
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]


class Card:
    def __init__(
        self,
        rank,
        suit,
    ):
        self.rank = rank
        self.suit = suit

    def make_bit(self):
        padding = 0b000
        idx = 0
        for index, rank in enumerate(Ranks):
            if rank == self.rank:
                idx = index
                break
        rank_bit = 0b0000000000000
        j = 0
        for i in range(13):
            if i == idx:
                rank_bit ^= 1 << j
            j += 1

        idx2 = 0
        suit_bit = 0b0000
        for index, suit in enumerate(Suits):
            if suit == self.suit:
                idx2 = index
                break
        for i in range(4):
            if i == idx2:
                suit_bit ^= 1 << i
        rrrr = 0b0000
        rrrr = calculate_bit(rrrr, lenght=4, target=idx)

        padding2 = 0b00
        prime_bit = 0b000000

        target = PRIMES[idx]
        prime_bit = calculate_bit(prime_bit, lenght=6, target=target)

        fertiger_bit = prime_bit
        fertiger_bit |= rrrr << 8
        fertiger_bit |= suit_bit << 12
        fertiger_bit |= rank_bit << 16

        return fertiger_bit


class Evaluator:
    def __init__(self, c1, c2, c3, c4, c5, flushes_array, unique5):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4
        self.c5 = c5
        self.flushes = flushes_array
        self.unique5 = unique5

    def evaluate(self):
        if (self.c1 & self.c2 & self.c3 & self.c4 & self.c5 & 0xF000) != 0:
            q = (self.c1 | self.c2 | self.c3 | self.c4 | self.c5) >> 16
            return self.flushes[q]

        # TODO: Hier kommen weitere Hand-Typen (Straight, Trips, etc.)
        else:
            q = (self.c1 | self.c2 | self.c3 | self.c4 | self.c5) >> 16
            return self.unique5[q]

    def evaluate_prime(self):
        q = self.prime()

    def prime(self):
        q = (
            (self.c1 & 0xFF)
            * (self.c2 & 0xFF)
            * (self.c3 & 0xFF)
            * (self.c4 & 0xFF)
            * (self.c5 & 0xFF)
        )
        return q


def calculate_bit(bit, lenght, target):
    sizes = [1]
    cur = 2
    for i in range(lenght):
        if i >= 1:
            sizes.append(cur)
            cur = cur * 2
    sizes.reverse()
    for idx, val in enumerate(sizes):
        if target >= val:
            bit ^= 1 << lenght - 1 - idx
            target = target - val
    return bit


deck = []
for rank in Ranks:
    for suit in Suits:
        card = Card(rank, suit)
        deck.append(card)


all_hands = list(combinations(deck, 5))
prime_set = set()
for hand in all_hands:
    input = []
    i = 0
    for card in hand:
        input.append(card.make_bit())
        i += 1
        if i == 5:
            break
    eval = Evaluator(*input, flushes, unique5)
    prime = eval.prime()
    prime_set.add(prime)

prime_array = sorted(prime_set)
print(f"Anzahl einzigartiger Primzahl-Produkte: {len(prime_array)}")
print(prime_array[:20])
