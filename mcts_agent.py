import utils
from mcts import *
import mtcs2


#
# Add code as needed, but do not change the interface.
#


class MCTSAgent:

    def name(self):
        """ Return agent's name."""
        return "mcts_agent"

    def reset(self):
        """ This function clears your internal data-structures, so the next
        call to play() starts with a fresh state (ie., no history information).
        """
        reset_tree()

    def play(self, game, check_abort):
        """ Returns the "best" move to play in the current <game>-state, after some deliberation (<check_abort>).
        """
        return mtcs(game, check_abort)
        '''
        solver = mtcs2.MCTS()
        root = mtcs2.Node(game, None)
        n = 0
        while not check_abort.do_abort():
            solver.do_rollout(root)
            n = n+1
        print(n)
        move = solver.choose(root).move
        return move, 0
        '''
