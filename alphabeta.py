from utils import Infinity
from utils import NoMove


def id_ab(game, check_abort, params):
    do_abort = False
    best_move = NoMove
    best_value = 0
    depth = 1
    max_iter_depth = params.get('iterdepth')
    if max_iter_depth is None:
        max_iter_depth = 0
    use_eval = params.get('eval')
    if use_eval is None:
        use_eval = False
    while not do_abort:
        value, move, do_abort = ab(game, 0, depth, -Infinity, Infinity, check_abort, use_eval)
        if not do_abort:
            best_move = move
            best_value = value
        depth += 1
        if max_iter_depth > 0 and depth >= max_iter_depth:
            break
    return best_move, best_value


def ab(game, ply, depth, alpha, beta, check_abort, use_eval):
    assert(ply >= 0)
    assert(-Infinity <= alpha <= Infinity)
    assert(-Infinity <= beta <= Infinity)
    assert(alpha < beta)

    def evaluate():
        if use_eval:
            pieces = game.get_pce_count()
            if game.get_to_move() == game.White:
                return pieces[game.White] - pieces[game.Black]
            else:
                return pieces[game.Black] - pieces[game.White]
        else:
            return 0

    if game.is_terminal():
        return -Infinity + 1 + ply, NoMove, False
    elif depth <= 0:
        return evaluate(), NoMove, False
    if check_abort.do_abort():
        return 0, NoMove, True

    do_abort = False
    best_value = -Infinity
    best_move = NoMove
    moves = game.generate(ply == 0)
    for move in moves:
        game.make(move)
        value, _, do_abort = ab(game, ply+1, depth-1, -beta, -alpha, check_abort, use_eval)
        value = -value
        game.retract(move)
        if do_abort:
            break
        if value > best_value:
            best_value = value
            best_move = move
            if value > alpha:
                alpha = value
                if value >= beta:
                    break
    return best_value, best_move, do_abort
