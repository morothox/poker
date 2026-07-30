import json

unique5 = [0] * 8192

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

for offset, pattern in enumerate(straight_patterns):
    unique5[pattern] = 1600 + offset

rank = 6186
for i in range(8191, -1, -1):
    if bin(i).count("1") == 5 and unique5[i] == 0:
        unique5[i] = rank
        rank += 1

with open("arrays/unique5.json", "w") as f:
    json.dump(unique5, f)
