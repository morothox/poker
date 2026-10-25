from poker.deepcfr.networks import CardEmbedder, DeepCFRNet
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


def deepcfr(T, players, K, inputs):
    # initialize advantage networks
    player_0_advantage = DeepCFRNet(3)
    player_1_advantage = DeepCFRNet(3)
    # initialize M (storage)
    M_p0_adv = []
    M_p1_adv = []
    # initialize M (strategy)
    strategy_model = DeepCFRNet(3)
    strategy_model.compile(
        optimizer="adam",
        loss="mean_squared_error",  # Macht exakt Summe( (y_true - y_pred)^2 ) / N
    )

    M_strategy = []
    for t in range(T):
        for p in players:
            for k in range(K):
                TRAVERSE()
            if p == 0:
                player_0_advantage.compile(
                    optimizer="adam",
                    loss="mean_squared_error",  # Macht exakt Summe( (y_true - y_pred)^2 ) / N
                )
                player_0_advantage.fit(inputs, M_p0_adv, sample_weight=t)
            else:
                player_1_advantage.compile(
                    optimizer="adam",
                    loss="mean_squared_error",  # Macht exakt Summe( (y_true - y_pred)^2 ) / N
                )
    strategy_model.fit()
