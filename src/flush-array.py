flushes = [0] * 8192

straight_patterns = [
    0b1111100000000,
    0b0111110000000,
    0b0011111000000,
    0b0001111100000,
    0b0000111110000,
    0b0000011111000,
    0b0000001111100,
    0b0000000111110,
    0b0000000011111,
    0b1000000001111,
]

for rank, pattern in enumerate(straight_patterns, start=1):
    flushes[pattern] = rank

rank = 323
for i in range(8191, -1, -1):
    if bin(i).count("1") == 5 and flushes[i] == 0:
        flushes[i] = rank
        rank += 1

unique5 = [0] * 8192

# Straights (gleiche Bit-Muster wie Straight Flushes) - Ranks 1600-1609
for offset, pattern in enumerate(straight_patterns):
    unique5[pattern] = 1600 + offset

# High Card Hands (alle restlichen 5-Bit-Muster) - Ranks 6186-7462
rank = 6186
for i in range(8191, -1, -1):
    if bin(i).count("1") == 5 and unique5[i] == 0:
        unique5[i] = rank
        rank += 1

if __name__ == "__main__":
    print(f"King-High Straight (unique5[3968], erwartet 1601): {unique5[3968]}")
    print(f"Worst High Card 7-5-4-3-2 (unique5[47], erwartet 7462): {unique5[47]}")
    print(f"Bester High Card AKQJ9 (unique5[7808], erwartet 6186): {unique5[7808]}")
