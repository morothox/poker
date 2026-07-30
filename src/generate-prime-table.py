from itertools import combinations

Suits = ["CLUB", "DIAMOND", "Heart", "SPADE"]
Ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]


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


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def make_bit(self):
        idx = 0
        for index, rank in enumerate(Ranks):
            if rank == self.rank:
                idx = index
                break

        rank_bit = 0b0000000000000
        for i in range(13):
            if i == idx:
                rank_bit ^= 1 << i

        idx2 = 0
        suit_bit = 0b0000
        for index, suit in enumerate(Suits):
            if suit == self.suit:
                idx2 = index
                break
        suit_bit ^= 1 << idx2

        rrrr = calculate_bit(0b0000, lenght=4, target=idx)
        prime_bit = calculate_bit(0b000000, lenght=6, target=PRIMES[idx])

        fertiger_bit = prime_bit
        fertiger_bit |= rrrr << 8
        fertiger_bit |= suit_bit << 12
        fertiger_bit |= rank_bit << 16

        return fertiger_bit


# Erstelle alle 52 Karten
deck = []
for rank in Ranks:
    for suit in Suits:
        card = Card(rank, suit)
        deck.append(card)


all_hands = list(combinations(deck, 5))

print(f"Deck erstellt: {len(deck)} Karten")
print(f"Anzahl aller Hände: {len(all_hands)}")
print("Berechne Primzahl-Produkte...")

# Berechne für jede Hand das Primzahl-Produkt
for hand in all_hands[:10]:  # Test mit ersten 10 Händen
    c1, c2, c3, c4, c5 = hand

    # Konvertiere zu Bits
    b1 = c1.make_bit()
    b2 = c2.make_bit()
    b3 = c3.make_bit()
    b4 = c4.make_bit()
    b5 = c5.make_bit()

    # Berechne Primzahl-Produkt
    prime_product = (b1 & 0xFF) * (b2 & 0xFF) * (b3 & 0xFF) * (b4 & 0xFF) * (b5 & 0xFF)

    print(f"{c1.rank}{c1.suit[0]} {c2.rank}{c2.suit[0]} {c3.rank}{c3.suit[0]} {c4.rank}{c4.suit[0]} {c5.rank}{c5.suit[0]} -> Prime: {prime_product}")
