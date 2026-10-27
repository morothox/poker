from poker.deepcfr.networks import CardEmbedder, DeepCFRNet
from poker.deepcfr.memory import Memory, transform_to_12
import tensorflow as tf
import keras

cards = []
for i in range(52):
    cards.append(i)
players = 2
board = []
for _ in range(5):
    board.append(cards)


def TRAVERSE():
    raise NotImplemented

    """ In:  (hole, board, bets)
         hole  (batch, 2)   card ids
         board (batch, 5)   card ids, -1 = not dealt yet
         bets  (batch, 2*P) bet occurred flags + bet size
    """


hole = []
board = []
bets = []

inputs = [hole, board, bets]


def deepcfr(T, players, K):
    # initialize M (player storage)
    M_p0_adv = Memory()
    M_p1_adv = Memory()
    # initialize advantage_model_0
    advantage_model_0 = DeepCFRNet(3)
    advantage_model_1 = DeepCFRNet(3)
    # initialize M (strategy)
    strategy_model = DeepCFRNet(3)
    # strategy memory
    M_strategy = Memory()
    for t in range(T):
        for p in range(players):
            for k in range(K):
                TRAVERSE()
            if p == 0:
                advantage_model_0 = DeepCFRNet(3)
                advantage_model_0.compile(
                    optimizer="adam",
                    loss="mean_squared_error",  # Macht exakt Summe( (y_true - y_pred)^2 ) / N
                )
                x, y, sample_weight = M_p0_adv.return_x_y()
                advantage_model_0.fit(x, y, sample_weight=sample_weight)
            else:
                advantage_model_1 = DeepCFRNet(3)
                advantage_model_1.compile(
                    optimizer="adam",
                    loss="mean_squared_error",  # Macht exakt Summe( (y_true - y_pred)^2 ) / N
                )
                x, y, sample_weight = M_p1_adv.return_x_y()
                advantage_model_1.fit(x, y, sample_weight=sample_weight)
    strategy_model.compile(
        optimizer="adam",
        loss="mean_squared_error",
    )
    x, y, sample_weight = M_strategy.return_x_y()
    strategy_model.fit(x, y, sample_weight=sample_weight)
    return strategy_model
