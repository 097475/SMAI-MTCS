import utils
import mcts1
import mtcs2
import mcts3


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
        mcts1.reset_tree()

    def play(self, game, check_abort):
        """ Returns the "best" move to play in the current <game>-state, after some deliberation (<check_abort>).
        """
        # algorithm 1, uncomment to use
        return mcts1.mtcs(game, check_abort)

        #algorithm 2, uncomment to use
        """
        solver = mtcs2.MCTS()
        root = mtcs2.Node(game, None)
        n = 0
        for i in range(1000):
            solver.do_rollout(root)
            n = n+1
            print(n)
        move = solver.choose(root).move
        return move, 0
        """

        #algorithm 3, uncomment to use
        #return mcts3.solve(game)
