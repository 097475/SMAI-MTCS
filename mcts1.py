#
# Add code here as needed.
#
import copy
# import breakthrough
import math
import functools

# reset this structure every time
tree = dict()


def reset_tree():
    tree.clear()


def tree_policy(state):  # state is always the root state at first
    def expand(node):  # node is a game state whose we want to generate all children
        key = node.get_key()  # get the hash key of node
        moves = node.generate()  # get all moves from node
        tree[key]["moves"] = True  # save that node's children were expanded
        for move in moves:
            node.make(move)  # apply the move
            # add the move to the tree, saving the hash key of its parent
            tree[node.get_key()] = {'moves': False, 'parent': key, 'count': 0, 'value': 0}
            node.retract(move)  # retract the move

    if state.is_terminal():
        return state
    else:
        # if node was not expanded, generate all children
        if not tree[state.get_key()]["moves"]:
            expand(state)
        # check if there's any ghost node among the current node children
        for m in state.generate():
            state.make(m)  # apply the move
            if tree[state.get_key()]["count"] == 0:  # if there's a ghost node, return it
                return state
            state.retract(m)  # retract the move

        # no ghost nodes, then pick best child according to UCT and apply tree policy again
        return tree_policy(best_child(state))


def simulation_policy(state, color):
    # simulate until a terminal state
    while not state.is_terminal():
        move = state.generate(True)[0]  # shuffle the moves so we can always pick the first move
        state.make(move)  # apply the move
    # if the next move is ours, we have lost
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


def best_child(state):
    c = math.sqrt(2)  # set the exploration constant # TODO: change c
    moves = state.generate()  # generate all moves from current state
    state_count = tree[state.get_key()]["count"]  # save the number of times the current state was visited for future
    children = []
    # save all the children in a list with a copy of their state
    for move in moves:
        state.make(move)
        children.append({"state": copy.deepcopy(state), "values": tree[state.get_key()]})
        state.retract(move)
    # compute the node that has the highest UCT value
    best_node = functools.reduce(lambda a, b: a if a["UCT"] > b["UCT"] else b,
                                 map(lambda x: {"state": x["state"], "UCT": x["values"]["value"] / x["values"]["count"]
                                     + c * math.sqrt(2 * math.log(state_count)) / x["values"]["count"]}, children))
    return best_node["state"]


def pick_move(state):
    moves = state.generate()  # generate all moves from current state
    children = []
    # save all the children in a list with the move that generated them
    for move in moves:
        state.make(move)
        children.append({"move": move, "values": tree[state.get_key()]})
        state.retract(move)
    # compute the node that was visited the most
    best_node = functools.reduce(lambda a, b: a if a["count"] > b["count"] else b,
                                 map(lambda x: {"move": x["move"], "count": x["values"]["count"]}, children))
    # return the move and its value
    return best_node["move"], best_node["count"]


def mtcs(game, check_abort):
    color = game.get_to_move() # save your own color
    # moves is true if the node had children expanded, false otherwise
    # parent contains the hashcode of parent node, count is the number of times the node was visited
    # value is the backed up value of the node
    tree[game.get_key()] = {'moves': False, 'parent': None, 'count': 0, 'value': 0}
    sims = 0
    while not check_abort.do_abort():
        selected_state = tree_policy(copy.deepcopy(game))  # selection and expansion
        outcome = simulation_policy(copy.deepcopy(selected_state), color)  # simulation
        backup(selected_state.get_key(), outcome)  # backup
        sims = sims + 1
        # print(sims)
    # print(tree)
    return pick_move(game)  # returns the move and its value


'''
if __name__ == '__main__':
    g = breakthrough.Breakthrough(6, 6)
    g.setup()
    g_copy = copy.deepcopy(g)
    print(mtcs(g_copy))
'''
