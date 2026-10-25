from random import sample

N = 100000


class Node:
    def __init__(self, my_card, history):
        self.my_card = my_card
        self.history = history
        self.regrets = [0.0, 0.0]
        self.strategy = [0.0, 0.0]
        self.avg_strategy = [0.0, 0.0]

    def get_strategy(self, weight):
        p0 = max(0.0, self.regrets[0])
        p1 = max(0.0, self.regrets[1])
        total = p0 + p1
        if total > 0:
            self.strategy = [p0 / total, p1 / total]
        else:
            self.strategy = [0.5, 0.5]

        # Strategie mit Spieler-Wahrscheinlichkeit (Reach Probability) akkumulieren
        self.avg_strategy[0] += weight * self.strategy[0]
        self.avg_strategy[1] += weight * self.strategy[1]
        return self.strategy

    def get_avg_strategy(self):
        total = self.avg_strategy[0] + self.avg_strategy[1]
        if total > 0:
            return [self.avg_strategy[0] / total, self.avg_strategy[1] / total]
        else:
            return [0.5, 0.5]

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.my_card == other.my_card and self.history == other.history


cards_ = {"K": 3, "Q": 2, "J": 1}

node_map = {}


def cfr(
    history,
    cards,
    p0,
    p1,
    iteration,
):
    player = len(history) % 2
    opponent = 1 - player
    # terminal state
    if (len(history) == 2 and history != "pb") or len(history) >= 3:
        if history != "pp" and history.endswith("p"):
            return 1
        else:
            if history.endswith("b"):
                if cards_[cards[player]] > cards_[cards[opponent]]:
                    return 2
                else:
                    return -2
            if history.endswith("p"):
                if cards_[cards[player]] > cards_[cards[opponent]]:
                    return 1
                else:
                    return -1
        return NotImplemented
    # game is still running
    else:
        key = (cards[player], history)
        if key not in node_map:
            node_map[key] = Node(cards[player], history)
        play = node_map[key]

        # alternating updates: pro Iteration wird nur ein Spieler aktualisiert
        traverser = iteration % 2
        if player == 0:
            own_reach, opponent_reach = p0, p1
        else:
            own_reach, opponent_reach = p1, p0

        # linear averaging: Iteration t zählt t-mal, gewichtet mit der eigenen Reach
        weight = 0
        if player == traverser:
            weight = (iteration + 1) * own_reach

        distribution = play.get_strategy(weight)
        if player == 0:
            p0_p = p0 * distribution[0]
            p0_b = p0 * distribution[1]
            pass_func = -cfr(history + "p", cards, p0_p, p1, iteration)
            bet_func = -cfr(history + "b", cards, p0_b, p1, iteration)

        else:
            p1_p = p1 * distribution[0]
            p1_b = p1 * distribution[1]
            pass_func = -cfr(history + "p", cards, p0, p1_p, iteration)
            bet_func = -cfr(history + "b", cards, p0, p1_b, iteration)
        node_value = pass_func * distribution[0] + bet_func * distribution[1]

        if player == traverser:
            # Regrets mit der Reach des Gegners gewichten, CFR+ floor bei 0
            pass_regret = (pass_func - node_value) * opponent_reach
            bet_regret = (bet_func - node_value) * opponent_reach
            play.regrets[0] = max(0.0, play.regrets[0] + pass_regret)
            play.regrets[1] = max(0.0, play.regrets[1] + bet_regret)
    return node_value


def train(iterations=N):
    deck = ["K", "Q", "J"]
    for i in range(iterations):
        board = sample(deck, 2)
        cfr("", board, 1.0, 1.0, i)


if __name__ == "__main__":
    train()
    for node in sorted(node_map.values(), key=lambda n: (n.history, n.my_card)):
        print(node.my_card, node.history, node.get_avg_strategy())
