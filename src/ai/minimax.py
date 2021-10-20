from time import time
from src.constant import ShapeConstant

from src.model import State, Board
from src.utility import is_win, is_full
from src.ai.obj_function import obj_function
from src.ai.gen_neigh import generate_neighbors
from typing import Tuple


class Minimax:
    MAX_DEPTH = 4

    def __init__(self):
        pass

    def is_leaf_node(self, depth: int, board: Board):
        return depth >= self.MAX_DEPTH or is_win(board) or is_full(board)

    def minimax(self, board: Board, depth: int, isMaximizing: bool, alpha: float, beta: float, circleUsed: int, crossUsed: int) -> Tuple[int, str, str]:
        if self.is_leaf_node(depth, board):
            playerValue = int(obj_function(board, self.player))
            enemyValue = int(obj_function(board, self.enemy))
            value = int(playerValue - enemyValue)
            return [value, "", ""]
        if depth % 2 == 1:
            neighbors = generate_neighbors(board, self.enemy, circleUsed, crossUsed)
        else:
            neighbors = generate_neighbors(board, self.player, circleUsed, crossUsed)

        if isMaximizing:
            maxVal = float("-inf")
            maxCol = None
            maxShape = None
            for board, colMove, shapeMove in neighbors:
                ci = circleUsed
                cr = crossUsed
                if shapeMove == ShapeConstant.CIRCLE:
                    ci += 1
                elif shapeMove == ShapeConstant.CROSS:
                    cr += 1
                value, _, _ = self.minimax(board, depth + 1, False, alpha, beta, ci, cr)
                if value > maxVal:
                    maxVal = value
                    maxCol = colMove
                    maxShape = shapeMove
                alpha = max(alpha, maxVal)
                if beta <= alpha:
                    break
            return [maxVal, maxCol, maxShape]
        else:
            minVal = float("+inf")
            minCol = None
            minShape = None
            for board, colMove, shapeMove in neighbors:
                ci = circleUsed
                cr = crossUsed
                if shapeMove == ShapeConstant.CIRCLE:
                    ci += 1
                elif shapeMove == ShapeConstant.CROSS:
                    cr += 1
                value, _, _ = self.minimax(board, depth + 1, True, alpha, beta, ci, cr)
                if value < minVal:
                    minVal = value
                    minCol = colMove
                    minShape = shapeMove
                beta = min(beta, minVal)
                if beta <= alpha:
                    break
            return [minVal, minCol, minShape]

    def find(self, state: State, player_turn: int, thinking_time: float):
        self.thinking_time = time() + thinking_time
        enemyTurn = (player_turn + 1) % 2
        self.player = state.players[player_turn]
        self.enemy = state.players[enemyTurn]
        self.state = state
        alpha = float("-inf")
        beta = float("+inf")
        _, col, shape = self.minimax(state.board, 0, True, alpha, beta, 0, 0)

        return [col, shape]
