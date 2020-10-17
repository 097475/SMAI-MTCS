#
# Add code here as needed.
#
import copy
import math
import functools
import random

# reset this structure every time
tree = dict()
move_tree = dict()
used_moves = []

def reset_tree():
    tree.clear()
    move_tree.clear()


###############à ADVANCED FUNCTIONS HERE ########################
def rave_tree_policy(state, c, k):  # state is always the root state at first
    def expand(node):  # node is a game state whose we want to generate all children
        key = node.get_key()  # get the hash key of node
        moves = node.generate()  # get all moves from node
        tree[key]["moves"] = moves  # save that node's children were expanded
        for move in moves:
            node.make(move)  # apply the move
            # add the move to the tree, saving the hash key of its parent, unless the node already exist (transposition)
            if not node.get_key() in tree:
                tree[node.get_key()] = {'moves': None, 'parent': key, 'count': 0, 'value': 0, 'rave_count': 0, 'rave': 0}
                move_key = hash((move, node.get_to_move()))
                if move_key not in move_tree:
                    move_tree[move_key] = [node.get_key()]
                else:
                    move_tree[move_key].append(node.get_key())
            node.retract(move)  # retract the move

    if state.is_terminal() or tree[state.get_key()]["count"] == 0:
        return state
    else:
        # if node was not expanded, generate all children
        if not tree[state.get_key()]["moves"]:
            expand(state)
        # no ghost nodes, then pick best child according to UCT and apply tree policy again
        return rave_tree_policy(rave_best_child(state, c, k), c, k)


# modifies state permanently
def rave_best_child(state, c, k):
    moves = tree[state.get_key()]["moves"]  # generate all moves from current state
    # save the number of times the current state was visited for future. Due to transpositions, sometimes ghost nodes
    # have children, in which case state_count becomes 1
    state_count = tree[state.get_key()]["count"] if tree[state.get_key()]["count"] > 0 else 1
    children = []
    # save all the children in a list with a copy of their state
    for move in moves:
        state.make(move)
        if tree[state.get_key()]["count"] == 0:  # if there's a ghost node, return it
            used_moves.append((move, state.get_to_move()))  # save the hash key of the reached state
            return state
        children.append({"move": move, "values": tree[state.get_key()]})
        state.retract(move)

    def rave_UCT(node):
        uct = -(node["values"]["value"] / node["values"]["count"])
        rave = -(node["values"]["rave"] / node["values"]["rave_count"]) if node["values"]["rave_count"] > 0 else 0
        expl = c * (math.sqrt(math.log(state_count)) / node["values"]["count"])
        beta = math.sqrt(k / ((3 * (node["values"]["count"] + node["values"]["rave_count"])) + k))
        return (beta * rave + (1 - beta) * uct) + expl

    # compute the node that has the highest UCT value
    best_node = functools.reduce(lambda a, b: a if rave_UCT(a) > rave_UCT(b) else b, children)
    state.make(best_node["move"])
    used_moves.append((best_node["move"], state.get_to_move()))  # save the hash key of the reached state
    return state


def rave_simulation_policy(state):
    # save whose turn it is in current state
    color = state.get_to_move()
    # simulate until a terminal state
    while not state.is_terminal():
        moves = state.generate()
        move = None
        for m in moves:
            if m[2] != -1:
                move = m
                break
        if not move:
            move = random.choice(moves)
        state.make(move)  # apply the move
        used_moves.append((move, state.get_to_move()))  # save the hash key of the reached state
    # if the next move corresponds to the color in the initial state, that player lost
    if state.get_to_move() == color:
        return -1, color
    else:
        return 1, color


def rave_backup(state_key, outcome, color):
    # recursively update values until the key is None (root)
    def _backup(_state_key, _outcome):
        if _state_key:
            tree[_state_key]["count"] += 1
            tree[_state_key]["value"] += _outcome
            _backup(tree[_state_key]["parent"], -_outcome)  # negamax formulation, the outcome is negated at each layer
    _backup(state_key, outcome)
    for move_tuple in used_moves:
        if hash(move_tuple) in move_tree:
            for s in move_tree[hash(move_tuple)]:
                if s in tree:
                    state = tree[s]
                    if move_tuple[1] == color:
                        state["rave_count"] += 1
                        state["rave"] += outcome
                    else:
                        state["rave_count"] += 1
                        state["rave"] -= outcome

#################################################################


def tree_policy(state, c):  # state is always the root state at first
    def expand(node):  # node is a game state whose we want to generate all children
        key = node.get_key()  # get the hash key of node
        moves = node.generate()  # get all moves from node
        tree[key]["moves"] = moves  # save that node's children were expanded
        for move in moves:
            node.make(move)  # apply the move
            # add the move to the tree, saving the hash key of its parent, unless the node already exist (transposition)
            if not node.get_key() in tree:
                tree[node.get_key()] = {'moves': None, 'parent': key, 'count': 0, 'value': 0}
            node.retract(move)  # retract the move

    if state.is_terminal() or tree[state.get_key()]["count"] == 0:
        return state
    else:
        # if node was not expanded, generate all children
        if not tree[state.get_key()]["moves"]:
            expand(state)
        # no ghost nodes, then pick best child according to UCT and apply tree policy again
        return tree_policy(best_child(state, c), c)


# modifies state permanently
def simulation_policy(state):
    # save whose turn it is in current state
    color = state.get_to_move()
    # simulate until a terminal state
    while not state.is_terminal():
        moves = state.generate()
        move = random.choice(moves)
        state.make(move)  # apply the move
    # if the next move corresponds to the color in the initial state, that player lost
    if state.get_to_move() == color:
        return -1
    else:
        return 1


def backup(state_key, outcome):
    # recursively update values until the key is None (root)
    if state_key:
        tree[state_key]["count"] += 1
        tree[state_key]["value"] += outcome
        backup(tree[state_key]["parent"], -outcome)  # negamax formulation, the outcome is negated at each layer


# modifies state permanently
def best_child(state, c):
    moves = tree[state.get_key()]["moves"]  # generate all moves from current state
    # save the number of times the current state was visited for future. Due to transpositions, sometimes ghost nodes
    # have children, in which case state_count becomes 1
    state_count = tree[state.get_key()]["count"] if tree[state.get_key()]["count"] > 0 else 1
    children = []
    # save all the children in a list with a copy of their state
    for move in moves:
        state.make(move)
        if tree[state.get_key()]["count"] == 0:
            return state
        children.append({"move": move, "values": tree[state.get_key()]})
        state.retract(move)
    # compute the node that has the highest UCT value
    best_node = functools.reduce(lambda a, b: a if -(a["values"]["value"] / a["values"]["count"])
                                                   + c * math.sqrt(math.log(state_count)) / a["values"]["count"] >
                                                   -(b["values"]["value"] / b["values"]["count"])
                                                   + c * math.sqrt(math.log(state_count)) / b["values"][
                                                       "count"] else b,
                                 children)
    state.make(best_node["move"])
    return state


def pick_move(state):
    moves = tree[state.get_key()]["moves"]  # generate all moves from current state
    children = []
    # save all the children in a list with the move that generated them
    for move in moves:
        state.make(move)
        children.append({"move": move, "values": tree[state.get_key()]})
        state.retract(move)
    # compute the node that was visited the most
    best_node = functools.reduce(lambda a, b: a if a["values"]["count"] >
                                                   b["values"]["count"] else b,
                                 children)
    # return the move and its value
    return best_node["move"], best_node["values"]["count"]


def base_mcts(game, check_abort, c):
    # moves is true if the node had children expanded, false otherwise
    # parent contains the hashcode of parent node, count is the number of times the node was visited
    # value is the backed up value of the node
    tree[game.get_key()] = {'moves': None, 'parent': None, 'count': 0, 'value': 0}
    while not check_abort.do_abort():
        selected_state = tree_policy(copy.deepcopy(game), c)  # selection and expansion
        selected_state_key = selected_state.get_key()
        outcome = simulation_policy(selected_state)  # simulation
        backup(selected_state_key, outcome)  # backup
    return pick_move(game)  # returns the move and its value


def advanced_mcts(game, check_abort, c, k):
    # moves is true if the node had children expanded, false otherwise
    # parent contains the hashcode of parent node, count is the number of times the node was visited
    # value is the backed up value of the node
    tree[game.get_key()] = {'moves': None, 'parent': None, 'count': 0, 'value': 0, 'rave_count': 0, 'rave': 0}
    while not check_abort.do_abort():
        selected_state = rave_tree_policy(copy.deepcopy(game), c, k)  # selection and expansion
        selected_state_key = selected_state.get_key()
        outcome, color = rave_simulation_policy(selected_state)  # simulation
        rave_backup(selected_state_key, outcome, color)  # backup
        used_moves.clear()
    return pick_move(game)  # returns the move and its value


def mcts(game, check_abort, params):
    c = params["c"]  # parameter for value of c in UCT formula
    advanced = params["advanced"]  # if true, use improvements
    max_simulations = params["simulations"]  # this can be used to limit simulations (we don't use it)
    return advanced_mcts(game, check_abort, c, params["k"]) if advanced else base_mcts(game, check_abort, c)
