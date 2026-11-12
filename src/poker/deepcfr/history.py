from poker.cactus_kev.cactus import Card, Evaluator, compare
from itertools import combinations, combinations_with_replacement
from random import sample

Suits = [
    0,
    1,
    2,
    3,
]
Ranks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# PRIMES[rank] = Primzahl fuer den Rank-Index (0="2" -> 2, ..., 12="A" -> 41)
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
deck = []
for i in range(51):
    deck.append(i)
c1 = sample(deck, 3)
print(c1)
FOLD = 0
CHECK = 1
CALL = 2
BET = 3


class History:
    def __init__(self, player, board, total_pot, action_round):
        self.player = player
        self.board = board
        self.total_pot = total_pot
        self.action_round = action_round

    def is_terminal(self):
        for action in self.action_round:
            for colm in action:
                if colm == FOLD:
                    return True
        if len(self.board) == 5:
            if self.action_round == []:
                return False
            else:
                current_list = self.action_round[-1]
                if len(current_list) == 0:
                    return False
                if len(current_list) < 2:
                    if current_list[-1] == CALL:
                        return True
                    else:
                        return False
                elif len(current_list) >= 2:
                    if (
                        current_list[-1] == CHECK and current_list[-2] == CHECK
                    ) or current_list[-1] == CALL:
                        return True
                return False
        return False

    def payoff(self, p):
        raise NotImplementedError
    def current_turn(self):


    # def terminal(self):
    #     if len(self.board) == 5:
    #         board_cards = []
    #         for card in self.board:
    #             rank = card // 4
    #             suit = card % 4
    #             c = Card(rank, suit)
    #             board_cards.append(c)
    #         p1_cards = []
    #         for card in self.p1:
    #             rank = card // 4
    #             suit = card % 4
    #             c = Card(rank, suit)
    #             p1_cards.append(c)
    #         p2_cards = []
    #         for card in self.p2:
    #             rank = card // 4
    #             suit = card % 4
    #             c = Card(rank, suit)
    #             p2_cards.append(c)
    #         score = compare(board_cards, p1_cards, p2_cards)
    #         return score
    #     else:
    #         return False

    def chance_node(self):
        if len(self.board) == 0:
            flop = sample(deck, 3)
            self.board = flop
            return self.board

        elif len(self.board) == 3:
            turn = sample(deck, 1)
            self.board.append(turn)
            return self.board
        elif len(self.board) == 4:
            river = sample(deck, 1)
            self.board.append(river)
            return self.board
