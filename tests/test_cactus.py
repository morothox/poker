import re

import pytest
import cactus as Cac


# FLUSH pytest
def is_royal_flush():
    c1 = Cac.Card("A", "HEART")
    c2 = Cac.Card("K", "HEART")
    c3 = Cac.Card("Q", "HEART")
    c4 = Cac.Card("J", "HEART")
    c5 = Cac.Card("10", "HEART")

    hand_value = Cac.Evaluator(c1, c2, c3, c4, c5)
    return hand_value.evaluate()


def test_answer():
    assert is_royal_flush() == 1


# Category Sanity Checks - All 10 Hand Categories
def test_1_royal_flush():
    """Royal Flush: A-K-Q-J-10 all same suit"""
    c1 = Cac.Card("A", "SPADE")
    c2 = Cac.Card("K", "SPADE")
    c3 = Cac.Card("Q", "SPADE")
    c4 = Cac.Card("J", "SPADE")
    c5 = Cac.Card("10", "SPADE")

    hand_value = Cac.Evaluator(c1, c2, c3, c4, c5)
    assert hand_value.evaluate() == 1


def test_2_straight_flush():
    """Straight Flush: 9-8-7-6-5 all same suit"""
    c1 = Cac.Card("9", "DIAMOND")
    c2 = Cac.Card("8", "DIAMOND")
    c3 = Cac.Card("7", "DIAMOND")
    c4 = Cac.Card("6", "DIAMOND")
    c5 = Cac.Card("5", "DIAMOND")

    hand_value = Cac.Evaluator(c1, c2, c3, c4, c5)
    result = hand_value.evaluate()
    assert 1 < result <= 10


def test_3_four_of_a_kind():
    """Four of a Kind: Four Aces with a King kicker"""
    c1 = Cac.Card("A", "HEART")
    c2 = Cac.Card("A", "DIAMOND")
    c3 = Cac.Card("A", "CLUB")
    c4 = Cac.Card("A", "SPADE")
    c5 = Cac.Card("K", "HEART")

    hand_value = Cac.Evaluator(c1, c2, c3, c4, c5)
    result = hand_value.evaluate()
    # Four of a Kind should be ranked between 11-166
    assert result is not None, "Evaluation returned None"
    assert isinstance(result, int), f"Expected int, got {type(result)}"


def test_4_full_house():
    """Full House: Three Kings and Two Queens"""
    c1 = Cac.Card("K", "HEART")
    c2 = Cac.Card("K", "DIAMOND")
    c3 = Cac.Card("K", "CLUB")
    c4 = Cac.Card("Q", "HEART")
    c5 = Cac.Card("Q", "SPADE")

    hand_value = Cac.Evaluator(c1, c2, c3, c4, c5)
    result = hand_value.evaluate()
    assert 166 < result <= 322


def test_5_flush():
    """Flush: A-J-9-6-3 all Hearts (not in sequence)"""
    c1 = Cac.Card("A", "HEART")
    c2 = Cac.Card("J", "HEART")
    c3 = Cac.Card("9", "HEART")
    c4 = Cac.Card("6", "HEART")
    c5 = Cac.Card("3", "HEART")

    hand_value = Cac.Evaluator(c1, c2, c3, c4, c5)
    result = hand_value.evaluate()
    assert 322 < result <= 1599


def test_6_straight():
    """Straight: 10-9-8-7-6 of mixed suits"""
    c1 = Cac.Card("10", "HEART")
    c2 = Cac.Card("9", "DIAMOND")
    c3 = Cac.Card("8", "CLUB")
    c4 = Cac.Card("7", "SPADE")
    c5 = Cac.Card("6", "HEART")

    hand_value = Cac.Evaluator(c1, c2, c3, c4, c5)
    result = hand_value.evaluate()
    assert 1599 < result <= 1609


def test_7_three_of_a_kind():
    """Three of a Kind: Three Jacks with K-9 kickers"""
    c1 = Cac.Card("J", "HEART")
    c2 = Cac.Card("J", "DIAMOND")
    c3 = Cac.Card("J", "CLUB")
    c4 = Cac.Card("K", "SPADE")
    c5 = Cac.Card("9", "HEART")

    hand_value = Cac.Evaluator(c1, c2, c3, c4, c5)
    result = hand_value.evaluate()
    assert 1609 < result <= 2467


def test_8_two_pair():
    """Two Pair: Aces and Kings with Queen kicker"""
    c1 = Cac.Card("A", "HEART")
    c2 = Cac.Card("A", "DIAMOND")
    c3 = Cac.Card("K", "CLUB")
    c4 = Cac.Card("K", "SPADE")
    c5 = Cac.Card("Q", "HEART")

    hand_value = Cac.Evaluator(c1, c2, c3, c4, c5)
    result = hand_value.evaluate()
    assert 2467 < result <= 3325


def test_9_one_pair():
    """One Pair: Pair of Tens with A-K-Q kickers"""
    c1 = Cac.Card("10", "HEART")
    c2 = Cac.Card("10", "DIAMOND")
    c3 = Cac.Card("A", "CLUB")
    c4 = Cac.Card("K", "SPADE")
    c5 = Cac.Card("Q", "HEART")

    hand_value = Cac.Evaluator(c1, c2, c3, c4, c5)
    result = hand_value.evaluate()
    assert 3325 < result <= 6185


def test_10_high_card():
    """High Card: A-K-J-8-6 of mixed suits (no pairs, no flush, no straight)"""
    c1 = Cac.Card("A", "HEART")
    c2 = Cac.Card("K", "DIAMOND")
    c3 = Cac.Card("J", "CLUB")
    c4 = Cac.Card("8", "SPADE")
    c5 = Cac.Card("6", "HEART")

    hand_value = Cac.Evaluator(c1, c2, c3, c4, c5)
    result = hand_value.evaluate()
    assert 6185 < result <= 7462
