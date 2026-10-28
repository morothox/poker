from poker.cactus_kev.cactus import Card, Evaluator, compare


class History:
    def __init__(self, p1, p2, board, p1_fold, p2_fold, total_pot):
        self.p1 = p1
        self.p2 = p2
        self.board = board
        self.p1_fold = p1_fold
        self.p2_fold = p2_fold
        self.total_pot = total_pot

    def is_terminal(self):
        if self.p1_fold:
            return self.total_pot
        elif self.p2_fold:
            return -self.total_pot
        if len(self.board) == 5:
            board_cards = []
            for card in self.board:
                rank = card // 12
                suit = card % 4
                c = Card(rank, suit)
                board_cards.append(c)
            p1_cards = []
            for card in self.board:
                rank = card // 12
                suit = card % 4
                c = Card(rank, suit)
                p1_cards.append(c)
            p2_cards = []
            for card in self.p2:
                rank = card // 12
                suit = card % 4
                c = Card(rank, suit)
                p2_cards.append(c)

        score = compare(board_cards, p1_cards, p2_cards)
