import tensorflow as tf
import keras
import numpy as np


def transform_to_12(rows, pad_val=0):
    """Turns a list of bet histories into the (n, 12) bet input.

    Each row is the list of bet sizes so far, e.g. [5, 6].
    First 6 columns: was there a bet at this position (0/1)
    Last 6 columns:  the bet size at this position
    """
    n_rows = len(rows)
    res = np.zeros((n_rows, 12), dtype=np.float32)  # (n, 12), everything empty
    # optional different value for empty bet sizes
    if pad_val != 0:
        res[:, 6:] = pad_val

    for i, row in enumerate(rows):
        k = len(row)  # how many bets happened in this situation
        if k > 0:
            row_arr = np.array(row)
            # flag half: 1 where a bet happened
            res[i, :k] = (row_arr > 0).astype(int)
            # size half: same positions, shifted by 6
            res[i, 6 : 6 + k] = row_arr

    return res


class Memory:
    """Stores training samples column by column.

    One insert = one situation. Lists only get turned into
    arrays when the training data is requested.
    """

    def __init__(self) -> None:
        # one list per part of an entry, index i belongs to the same situation everywhere
        self.hole = []
        self.board = []
        self.bet = []
        self.t = []  # iteration the sample came from -> sample_weight later
        self.advantages = []  # target values -> y

    def insert_memory(self, hole, board, bet, t, advantages):
        # add one situation to every list
        self.hole.append(hole)
        self.board.append(board)
        self.bet.append(bet)
        self.t.append(t)
        self.advantages.append(advantages)

    def return_x_y(self):
        # pad hole to 2 and board to 5 cards with -1 so every row has the same length
        padded = [row + [-1] * (2 - len(row)) for row in self.hole]
        hole_array = np.array(padded, dtype=np.int32)  # (n, 2)
        padded = [row + [-1] * (5 - len(row)) for row in self.board]
        board_array = np.array(padded, dtype=np.int32)  # (n, 5)
        bet_array = transform_to_12(self.bet)  # (n, 12)
        # model input, same order as hole, board, bets = inputs in call
        x = (hole_array, board_array, bet_array)
        # y = advantages
        y = np.array(self.advantages, dtype=np.float32)
        # sample_weight
        sample_weight = np.array(self.t, dtype=np.float32)
        return x, y, sample_weight
