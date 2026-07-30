import json

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

with open("arrays/flushes.json", "w") as f:
    json.dump(flushes, f)
