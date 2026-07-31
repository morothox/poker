from collections import Counter
import json
from itertools import combinations, combinations_with_replacement
from cactus import Card, Evaluator

with open("arrays/flushes.json", "r") as f:
    flushes = json.load(f)

with open("arrays/unique5.json", "r") as f:
    unique5 = json.load(f)

Suits = ["CLUB", "DIAMOND", "Heart", "SPADE"]
ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
corresponding = dict(zip(ranks, PRIMES))


all_hands = list(combinations_with_replacement(ranks, 5))
schluessel_values = dict()

prime_set = set()
for hand in all_hands:
    counter = Counter(hand)
    kind = counter.most_common()
    sortierte_paare = sorted(kind, key=lambda x: (x[1], x[0]), reverse=True)
    haeufigkeiten_tupel = tuple(anzahl for rang, anzahl in sortierte_paare)
    raenge_tupel = tuple(rang for rang, anzahl in sortierte_paare)
    sortier_schluessel = (haeufigkeiten_tupel, raenge_tupel)
    if haeufigkeiten_tupel == (5,):
        continue
    prime_value = 1
    for card in hand:
        prime_value *= corresponding[card]
    schluessel_values[prime_value] = sortier_schluessel

sorted_by_value = dict(
    sorted(schluessel_values.items(), key=lambda item: item[1], reverse=True)
)

final_primes = {}
rang = 11
letzte_kat = None

for primprodukt, sortier_schluessel in sorted_by_value.items():
    kat = sortier_schluessel[0]
    if kat != letzte_kat:
        if kat == (3, 2):
            rang = 167
        elif kat == (3, 1, 1):
            rang = 1610
        elif kat == (2, 2, 1):
            rang = 2468
        elif kat == (2, 1, 1, 1):
            rang = 3326
        letzte_kat = kat
    final_primes[str(primprodukt)] = rang
    rang += 1

with open("arrays/primes.json", "w") as f:
    json.dump(final_primes, f)
