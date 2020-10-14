from mcts import mcts
import copy


class State():
    def __init__(self, state):
        self.state = state
        self.color = state.get_to_move()

    def getCurrentPlayer(self):
        return self.state.get_to_move()

    def getPossibleActions(self):
        return [Action(a) for a in self.state.generate()]

    def takeAction(self, action):
        newState = copy.deepcopy(self)
        newState.state.make(action.move)
        return newState

    def isTerminal(self):
        return self.state.is_terminal()

    def getReward(self):
        if self.state.get_to_move() == self.color:
            return -1
        else:
            return 1


class Action():
    def __init__(self, move):
        self.move = move

    def __str__(self):
        return str(self.move)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return self.move[0] == other.move[0] and self.move[1] == other.move[1] and self.move[2] == other.move[2]
        else:
            return self.move[0] == other[0] and self.move[1] == other[1] and self.move[2] == other[2]

    def __hash__(self):
        return hash((self.move[0], self.move[1], self.move[2]))


def solve(game):
    initialState = State(game)
    _mcts = mcts(iterationLimit=1000)
    bestAction = _mcts.search(initialState=initialState)
    return bestAction.move, 0
