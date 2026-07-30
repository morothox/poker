import json
from itertools import combinations
from cactus_kev import Card, Evaluator

with open("arrays/flushes.json", "r") as f:
    flushes = json.load(f)

with open("arrays/unique5.json", "r") as f:
    unique5 = json.load(f)

Suits = ["CLUB", "DIAMOND", "Heart", "SPADE"]
Ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

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
    eval = Evaluator(*input)
    if not eval.evaluate():
        prime = eval.prime()
        prime_set.add(prime)

primes = sorted(prime_set)

with open("arrays/primes.json", "w") as f:
    json.dump(primes, f)
