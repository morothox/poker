from itertools import permutations

from poker.kuhn import cfr_kuhn

TERMINAL = {"pp", "bp", "bb", "pbp", "pbb"}


def payoff_p0(cards, history):
    if history == "bp":
        return 1
    if history == "pbp":
        return -1
    sign = 1 if cfr_kuhn.cards_[cards[0]] > cfr_kuhn.cards_[cards[1]] else -1
    return sign * (1 if history == "pp" else 2)


def expected_value(cards, history=""):
    if history in TERMINAL:
        return payoff_p0(cards, history)
    player = len(history) % 2
    strategy = cfr_kuhn.node_map[(cards[player], history)].get_avg_strategy()
    return strategy[0] * expected_value(cards, history + "p") + strategy[1] * expected_value(
        cards, history + "b"
    )


def test_converges_to_nash_game_value():
    cfr_kuhn.node_map.clear()
    cfr_kuhn.train(50000)
    deals = list(permutations("KQJ", 2))
    value = sum(expected_value(d) for d in deals) / len(deals)
    # Nash-Spielwert von Kuhn Poker für Spieler 0 ist -1/18
    assert abs(value - (-1 / 18)) < 0.01
