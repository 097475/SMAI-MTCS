import utils
import mcts

#
# Add code as needed, but do not change the interface.
#


class MCTSAgent:

    def __init__(self):
        ...
        return

    def name(self):
        """ Return agent's name."""
        return "mcts_agent"

    def reset(self):
        """ This function clears your internal data-structures, so the next
        call to play() starts with a fresh state (ie., no history information).
        """
        ...
        return

    def play(self, game, check_abort):
        """ Returns the "best" move to play in the current <game>-state, after some deliberation (<check_abort>).
        """
        moves = game.generate(True)
        if moves:
            return moves[0], 0
        else:
            return utils.NoMove, 0
