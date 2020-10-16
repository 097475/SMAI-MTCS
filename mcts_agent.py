import utils
import mcts


#
# Add code as needed, but do not change the interface.
#


class MCTSAgent:
    def __init__(self, params):
        self._params = params
        self._params["c"] = 0.5
        self._params["k"] = 10
        return

    def name(self):
        """ Return agent's name."""
        return "mcts_agent"

    def reset(self):
        """ This function clears your internal data-structures, so the next
        call to play() starts with a fresh state (ie., no history information).
        """
        mcts.reset_tree()

    def play(self, game, check_abort):
        """ Returns the "best" move to play in the current <game>-state, after some deliberation (<check_abort>).
        """
        # algorithm 1, uncomment to use
        move, value = mcts.mcts(game, check_abort, self._params)
        self.reset()
        return move, value
