class TerminalNode:
    def __init__(self, node_type, pot, winner=None):
        self.node_type = node_type  # "SHOWDOWN" oder "FOLD"
        self.pot = pot
        self.winner = winner  # Spieler-Index bei FOLD, sonst None


class Node:
    def __init__(self, player, actions):
        self.player = player
        self.actions = actions
        self.children = []


# Aktionen
FOLD = 0
CHECK = 1
CALL = 2
BET33 = 3
BET50 = 4
JAM = 5

MAX_RAISES = 2  # Verhindert endlose Re-Raise-Schleifen


def game_tree(player, pot, to_call, last_action, raises=0):
    if last_action == FOLD:
        # Der Spieler, der nicht dran ist (1 - player), gewinnt kampflos
        return TerminalNode(node_type="FOLD", pot=pot, winner=1 - player)

    if last_action == CALL:
        return TerminalNode(node_type="SHOWDOWN", pot=pot)

    if last_action == CHECK and player == 0:
        return TerminalNode(node_type="SHOWDOWN", pot=pot)

    if to_call == 0:
        legal_actions = [CHECK]
        if raises < MAX_RAISES:
            legal_actions.extend([BET33, BET50, JAM])
    else:
        legal_actions = [FOLD, CALL]
        if raises < MAX_RAISES:
            legal_actions.append(JAM)

    play = Node(player, legal_actions)
    next_player = 1 - player

    for action in legal_actions:
        new_pot = pot
        next_to_call = 0
        next_raises = raises

        if action == CHECK:
            next_to_call = 0

        elif action == CALL:
            new_pot = pot + to_call
            next_to_call = 0

        elif action == FOLD:
            next_to_call = 0

        elif action == BET33:
            bet_size = pot * 0.33
            new_pot = pot + bet_size
            next_to_call = bet_size
            next_raises = raises + 1

        elif action == BET50:
            bet_size = pot * 0.50
            new_pot = pot + bet_size
            next_to_call = bet_size
            next_raises = raises + 1

        elif action == JAM:
            # Beispielhafte All-in-Größe (oder verbleibender Stack)
            bet_size = pot * 1.5
            new_pot = pot + bet_size
            next_to_call = bet_size
            next_raises = raises + 1

        child = game_tree(
            player=next_player,
            pot=new_pot,
            to_call=next_to_call,
            last_action=action,
            raises=next_raises,
        )
        play.children.append(child)

    return play


if __name__ == "__main__":
    start_pot = 100.0
    # Spieler 0 startet am River, to_call = 0, keine Voraktion
    root = game_tree(player=0, pot=start_pot, to_call=0, last_action=None)

    def count_nodes(node):
        if isinstance(node, TerminalNode):
            return 1
        return 1 + sum(count_nodes(child) for child in node.children)

    def traverse(node):
        if isinstance(node, TerminalNode):
            return
        else:
            print(node.player, node.actions)
            children = node.children
            for child in children:
                traverse(node=child)

    test = traverse(root)
