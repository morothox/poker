"""This is the link to the Paper [[/Users/morothox/Project/poker/DeepCFR+.pdf][DeepCFR]]"""

import tensorflow as tf
import keras


class CardEmbedder(keras.layers.Layer):
    """Turns a group of cards (hole or board) into one 64-dim vector.

    In:  (batch, n) card ids 0-51, -1 = no card yet
    Out: (batch, 64)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # one embedding each for rank, suit and the exact card
        self.embedding_rank = keras.layers.Embedding(13, 64)  # rank 0-12
        self.embedding_suit = keras.layers.Embedding(4, 64)  # suit 0-3
        self.embedding_value = keras.layers.Embedding(52, 64)  # card 0-51

    def call(self, inputs):
        # remember which slots hold real cards before touching the -1s
        mask = inputs != -1  # (batch, n)

        # -1 isn't a valid index, swap it for 0 (gets zeroed out later anyway)
        result = tf.multiply(inputs, tf.cast(mask, inputs.dtype))

        # cards are numbered 4*rank + suit
        suit = result % 4
        rank = result // 4

        rank_vec = self.embedding_rank(rank)
        suit_vec = self.embedding_suit(suit)
        value_vec = self.embedding_value(result)
        card = rank_vec + suit_vec + value_vec  # (batch, n, 64)

        # kill the vectors of empty slots, extra axis so it broadcasts over 64
        mask_float = tf.cast(mask[..., tf.newaxis], dtype=tf.float32)
        card = card * mask_float

        # sum over the cards -> order doesn't matter anymore
        card_summed = tf.reduce_sum(card, axis=1)  # (batch, 64)
        return card_summed


class DeepCFRNet(keras.Model):
    """Network from the Deep CFR paper (Fig. 1).

    Same architecture is used for the advantage net and the strategy net,
    only the training target is different.

    In:  (hole, board, bets)
         hole  (batch, 2)   card ids
         board (batch, 5)   card ids, -1 = not dealt yet
         bets  (batch, 2*P) bet occurred flags + bet sizes
    Out: (batch, n_actions) one raw value per action, no activation
    """

    def __init__(self, n_actions=3, **kwargs):
        super().__init__(**kwargs)
        # separate embedders so hole and board get their own weights
        self.hole_embedder = CardEmbedder()
        self.board_embedder = CardEmbedder()
        # card branch
        self.card_dense_layer1 = keras.layers.Dense(192, "relu")
        self.card_dense_layer2 = keras.layers.Dense(192, "relu")
        self.card_dense_layer3 = keras.layers.Dense(64, "relu")
        # bet branch

        self.bet_dense_layer1 = keras.layers.Dense(64, "relu")
        self.bet_dense_layer2 = keras.layers.Dense(64, "relu")
        # after cards and bets are merged
        self.combined_layer1 = keras.layers.Dense(64, "relu")
        self.combined_layer2 = keras.layers.Dense(64, "relu")
        self.combined_layer3 = keras.layers.Dense(64, "relu")
        # no activation, advantages can be negative and logits get softmaxed outside
        self.output_layer = keras.layers.Dense(
            n_actions, kernel_initializer="zeros", bias_initializer="zeros"
        )

    def call(self, inputs):  # pyright: ignore[reportIncompatibleMethodOverride]
        hole, board, bets = inputs

        hole_vec = self.hole_embedder(hole)  # (batch, 64)
        board_vec = self.board_embedder(board)  # (batch, 64)
        concatenated_vec = tf.concat([hole_vec, board_vec], axis=-1)  # (batch, 128)

        # card branch
        x1_card = self.card_dense_layer1(concatenated_vec)  # (batch, 192)
        x2_card = self.card_dense_layer2(x1_card)  # (batch, 192)
        x3_card = self.card_dense_layer3(x2_card)  # (batch, 64)

        # bet branch
        x1_bet = self.bet_dense_layer1(bets)  # (batch, 64)
        x2_bet = self.bet_dense_layer2(x1_bet)  # (batch, 64)

        # put cards and bets side by side, the next layer learns how to mix them
        combined_bet_card = tf.concat([x3_card, x2_bet], -1)  # (batch, 128)

        x1_combined = self.combined_layer1(combined_bet_card)  # (batch, 64)
        x2_combined = self.combined_layer2(x1_combined)
        x3_combined = self.combined_layer3(x2_combined)

        # standardize each row (z-score), epsilon so we never divide by 0
        avg_all = tf.reduce_mean(x3_combined, axis=-1, keepdims=True)
        deviation = tf.math.reduce_std(x3_combined, axis=-1, keepdims=True)
        normalization = (x3_combined - avg_all) / (deviation + 1e-7)

        # one value per action (fold, call, raise)
        action_values = self.output_layer(normalization)  # (batch, n_actions)
        return action_values
