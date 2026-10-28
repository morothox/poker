from poker.cactus_kev.cactus import Card, evaluate_7_cards

# Ranks: 0="2" ... 8="10", 9="J", 10="Q", 11="K", 12="A"
# Suits: 0=CLUB, 1=DIAMOND, 2=HEART, 3=SPADE


def hand(*cards):
    return [Card(rank, suit) for rank, suit in cards]


def test_royal_flush_is_best_hand():
    royal = hand((12, 3), (11, 3), (10, 3), (9, 3), (8, 3), (0, 2), (1, 0))
    assert evaluate_7_cards(royal) == 1


def test_quads_beat_full_house():
    board = [(11, 3), (11, 2), (5, 0), (5, 1), (0, 3)]
    quads = hand(*board, (11, 0), (11, 1))
    full_house = hand(*board, (5, 3), (1, 2))
    # kleinerer Wert = bessere Hand
    assert evaluate_7_cards(quads) < evaluate_7_cards(full_house)
