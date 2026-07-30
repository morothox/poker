import cactus_kev as cac

flushes = [0] * 8192
rank = 323
for i in range(8192, -1, -1):
    if bin(i).count("1") == 5:
        flushes[i] = rank
        rank += 1
