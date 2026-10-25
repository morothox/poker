from poker.cactus_kev.cactus import Card, evaluate_7_cards


def hand(*cards):
    return [Card(rank, suit) for rank, suit in cards]


def test_royal_flush_is_best_hand():
    royal = hand(("A", "SPADE"), ("K", "SPADE"), ("Q", "SPADE"), ("J", "SPADE"), ("10", "SPADE"), ("2", "HEART"), ("3", "CLUB"))
    assert evaluate_7_cards(royal) == 1


def test_quads_beat_full_house():
    board = [("K", "SPADE"), ("K", "HEART"), ("7", "CLUB"), ("7", "DIAMOND"), ("2", "SPADE")]
    quads = hand(*board, ("K", "CLUB"), ("K", "DIAMOND"))
    full_house = hand(*board, ("7", "SPADE"), ("3", "HEART"))
    # kleinerer Wert = bessere Hand
    assert evaluate_7_cards(quads) < evaluate_7_cards(full_house)
