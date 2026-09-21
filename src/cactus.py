import json
from itertools import combinations, combinations_with_replacement
import os
from random import sample

Suits = ["CLUB", "DIAMOND", "Heart", "SPADE"]
Ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

arrays_dir = os.path.join(os.path.dirname(__file__), "arrays")

with open(os.path.join(arrays_dir, "flushes.json"), "r") as f:
    flushes = json.load(f)

with open(os.path.join(arrays_dir, "unique5.json"), "r") as f:
    unique5 = json.load(f)

with open(os.path.join(arrays_dir, "primes.json"), "r") as f:
    primes = json.load(f)


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        else:
            return False

    def make_bit(self):
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

        prime_bit = 0b000000
        target = PRIMES[idx]
        prime_bit = calculate_bit(prime_bit, lenght=6, target=target)

        fertiger_bit = prime_bit
        fertiger_bit |= rrrr << 8
        fertiger_bit |= suit_bit << 12
        fertiger_bit |= rank_bit << 16

        return fertiger_bit


class Evaluator:
    def __init__(self, c1, c2, c3, c4, c5):
        self.c1 = c1.make_bit()
        self.c2 = c2.make_bit()
        self.c3 = c3.make_bit()
        self.c4 = c4.make_bit()
        self.c5 = c5.make_bit()

    def evaluate(self):
        if (self.c1 & self.c2 & self.c3 & self.c4 & self.c5 & 0xF000) != 0:
            q = (self.c1 | self.c2 | self.c3 | self.c4 | self.c5) >> 16
            return flushes[q]

        q = (self.c1 | self.c2 | self.c3 | self.c4 | self.c5) >> 16
        if bin(q).count("1") == 5:
            return unique5[q]

        return primes[str(self.prime())]

    def prime(self):
        return (
            (self.c1 & 0xFF)
            * (self.c2 & 0xFF)
            * (self.c3 & 0xFF)
            * (self.c4 & 0xFF)
            * (self.c5 & 0xFF)
        )


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


c1 = Card("J", "HEART")
c2 = Card("J", "DIAMOND")
c3 = Card("J", "CLUB")
c4 = Card("K", "SPADE")
c5 = Card("9", "HEART")
c6 = Card("A", "DIAMOND")
c7 = Card("Q", "CLUB")
seven = [c1, c2, c3, c4, c5, c6, c7]


def evaluate_7_cards(seven_cards):
    best_score = float("inf")
    for combo in combinations(seven_cards, 5):
        value = Evaluator(*combo).evaluate()
        if value <= best_score:
            best_score = value
    return best_score


test = evaluate_7_cards(seven)

hero = [Card("A", "SPADE"), Card("K", "SPADE")]
villain = [Card("K", "CLUB"), Card("K", "Heart")]


# deck = combinations_with_replacement(Ranks, 2)
# print(list(deck))
deck = []
for rank in Ranks:
    for suit in Suits:
        deck.append(Card(rank, suit))
deck.remove(hero[0])
deck.remove(villain[0])
deck.remove(hero[1])
deck.remove(villain[1])

print(len(deck))


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


test = monte_carlo(deck, hero, villain)
print(test)
