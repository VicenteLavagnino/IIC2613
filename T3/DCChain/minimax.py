import math
from Game.Board import is_winner, get_all_moves

def minimax(circles, JUGADORES, JUGADOR_FIJO , id, table_size,depth, max_player, alphabeta, eval_func ,alpha = -math.inf, beta = math.inf):
    if depth == 0 or is_winner(circles, JUGADORES) == True:
        ## NO MODIFICAR
        return eval_func(circles, JUGADOR_FIJO), None
    
    ## MAX
    if max_player:
        ## NO MODIFICAR
        maxEval = float('-inf')
        best_move = None
        for move, pos in get_all_moves(circles, JUGADORES, JUGADORES[id], table_size):
            evaluation = minimax(move, JUGADORES, JUGADOR_FIJO , not id, table_size, depth-1, False, alphabeta, eval_func , alpha, beta)[0]
            if maxEval < evaluation:
                maxEval = evaluation
                best_move = pos

            if alphabeta:
              ## MODIFICAR
              # IMPLEMENTAR ALPHA BETA PRUNING

              alpha = max(alpha, maxEval)

              if beta <= alpha:
                break

        return maxEval, best_move
    else:
        ## MIN
        ## NO MODIFICAR
        minEval = float('inf')
        best_move = None
        for move, pos in get_all_moves(circles, JUGADORES, JUGADORES[id], table_size):
            evaluation = minimax(move, JUGADORES, JUGADOR_FIJO, not id, table_size, depth-1, True, alphabeta, eval_func, alpha, beta)[0]

            if minEval > evaluation:
                minEval = evaluation
                best_move = pos

            if alphabeta:
              ## MODIFICAR
              # IMPLEMENTAR ALPHA BETA PRUNING
              beta = min(beta, minEval)
              if beta <= alpha:
                break


              continue
        
        return minEval, best_move