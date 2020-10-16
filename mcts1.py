#
# Add code here as needed.
#
import copy
# import breakthrough
import math
import functools
import numpy as np

# reset this structure every time
tree = dict()


def reset_tree():
    tree.clear()


def tree_policy(state):  # state is always the root state at first
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

    if state.is_terminal():
        return state
    else:
        # if node was not expanded, generate all children
        if not tree[state.get_key()]["moves"]:
            expand(state)
        # check if there's any ghost node among the current node children
        for m in tree[state.get_key()]["moves"]:
            state.make(m)  # apply the move
            if tree[state.get_key()]["count"] == 0:  # if there's a ghost node, return it
                return state
            state.retract(m)  # retract the move

        # no ghost nodes, then pick best child according to UCT and apply tree policy again
        return tree_policy(best_child(state))


# modifies state permanently
def simulation_policy(state):
    # save whose turn it is in current state
    color = state.get_to_move()
    # simulate until a terminal state
    while not state.is_terminal():
        moves = state.generate()
        idx = np.random.choice(len(moves))
        move = moves[idx]  # shuffle the moves so we can always pick the first move
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
def best_child(state):
    c = math.sqrt(2)  # set the exploration constant # TODO: change c
    moves = tree[state.get_key()]["moves"]  # generate all moves from current state
    # save the number of times the current state was visited for future. Due to transpositions, sometimes ghost nodes
    # have children, in which case state_count becomes 1
    state_count = tree[state.get_key()]["count"] if tree[state.get_key()]["count"] > 0 else 1
    children = []
    # save all the children in a list with a copy of their state
    for move in moves:
        state.make(move)
        children.append({"move": move, "values": tree[state.get_key()]})
        state.retract(move)
    # compute the node that has the highest UCT value
    best_node = functools.reduce(lambda a, b: a if -(a["values"]["value"] / a["values"]["count"])
                                                   + c * math.sqrt(2 * math.log(state_count)) / a["values"]["count"] >
                                                   -(b["values"]["value"] / b["values"]["count"])
                                                   + c * math.sqrt(2 * math.log(state_count)) / b["values"][
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


def mtcs(game, check_abort):
    # moves is true if the node had children expanded, false otherwise
    # parent contains the hashcode of parent node, count is the number of times the node was visited
    # value is the backed up value of the node
    tree[game.get_key()] = {'moves': None, 'parent': None, 'count': 0, 'value': 0}
    sims = 0
    while not check_abort.do_abort():
        selected_state = tree_policy(copy.deepcopy(game))  # selection and expansion
        selected_state_key = selected_state.get_key()
        outcome = simulation_policy(selected_state)  # simulation
        backup(selected_state_key, outcome)  # backup
        sims = sims + 1
    print(sims)
    #print(tree)
    return pick_move(game)  # returns the move and its value


'''
if __name__ == '__main__':
    g = breakthrough.Breakthrough(6, 6)
    g.setup()
    g_copy = copy.deepcopy(g)
    print(mtcs(g_copy))
'''
