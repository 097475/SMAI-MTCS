import argparse
import copy
import breakthrough
import ab_agent
import mcts_agent
import utils
from timeit import default_timer as timer

def play_a_game(game, A, output):
    game.setup()
    if output:
        print(game)
    n = 0
    A[0].reset()
    A[1].reset()
    while not game.is_terminal():
        move, value = A[n % 2].play(copy.deepcopy(game), utils.CheckAbort(time))
        assert(move != utils.NoMove)
        game.make(move)
        if output:
            print(move, value)
            print(game)
        n += 1
    if game.get_to_move() == game.White:
        ScoreColor['Black'] += 1
        ScoreAgent[A[1].name()] += 1
    else:
        ScoreColor['White'] += 1
        ScoreAgent[A[0].name()] += 1

# The main program.
# Set up and parse command-line arguments.

ap = argparse.ArgumentParser()
ap.add_argument("-b", "--board", default=6, help="Boardsize (nxn).", type=int)
ap.add_argument("-g", "--games", default=1, help="Number of games to play (with each color).", type=int)
ap.add_argument("-t", "--time", default=0.5, help="Max deliberation time.", type=float)
ap.add_argument("-d", "--debug", default=False, help="Increase output verbosity.", action="store_true")
ap.add_argument("-i", "--iterdepth", default=4, help="Max iteration-depth for AB.", type=int)
ap.add_argument("-s", "--simulations", default=0, help="Max number of MCTS simulations.", type=int)
ap.add_argument("-e", "--eval", default=False, help="Use evaluation function in AB.", action="store_true")
ap.add_argument("-a", "--advanced", default=False, help="Use advanced MCTS variant.", action="store_true")

args = vars(ap.parse_args())
print(args)
board_size = args['board']
time = args['time']
num_games = args['games']
output = args['debug']
use_eval = args['eval']
ab_agent_param = {'iterdepth':args['iterdepth'], 'eval':args['eval']}
mc_agent_param = {'simulations':args['simulations'], 'advanced':args['advanced']}

game = breakthrough.Breakthrough(board_size, board_size)
print(game)
agents = [ab_agent.ABAgent(ab_agent_param), mcts_agent.MCTSAgent(mc_agent_param)]

ScoreColor = {'White': 0, 'Black': 0}
ScoreAgent = {agents[0].name(): 0, agents[1].name(): 0}

start_time = timer()
for n in range(num_games):
    play_a_game(game, agents, output)
    play_a_game(game, agents[::-1], output)
    print(ScoreAgent)
print("Time:", timer() - start_time)
print('Match result')
print(ScoreColor)
print(ScoreAgent)
