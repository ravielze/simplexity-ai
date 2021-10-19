import random
import copy
from time import time

from src.constant import ShapeConstant, ColorConstant
from src.model import State, Board, Piece, Player
from src.utility import is_win, is_full

from typing import Tuple, List

def objective_function(board: Board, player: Player) -> float:
    val = random.uniform(-100.0, 100.0)
    return val

class Minimax:
    MAX_DEPTH = 1
    def __init__(self):
        pass
    def is_leaf_node(self, depth: int, board: Board):
        return depth >= self.MAX_DEPTH or is_win(board) or is_full(board)
    def generate_neighbors(self, board: Board, player: Player) -> list[Tuple[Board, str, str]]:
        col = board.col
        row = board.row
        ans = list()
        for i in range(col):
            for j in range(row - 1, -1, -1):
                if board[j, i].shape == ShapeConstant.BLANK:
                    if player.quota[ShapeConstant.CIRCLE] > 0:
                        newBoard = copy.deepcopy(board)
                        newBoard.set_piece(j, i, Piece(ShapeConstant.CIRCLE, player.color))
                        ans.append([newBoard, i, ShapeConstant.CIRCLE])
                    if player.quota[ShapeConstant.CROSS] > 0:
                        newBoard = copy.deepcopy(board)
                        newBoard.set_piece(j, i, Piece(ShapeConstant.CROSS, player.color))
                        ans.append([newBoard, i, ShapeConstant.CROSS])
                    break
        return ans

    def minimax(self, board: Board, depth: int, isMaximizing: bool, alpha: float, beta: float, prevMove: Tuple[str, str]) -> Tuple[float, str, str]:
        current_turn = (self.turn + depth) % 2
        player = self.state.players[current_turn]
        if self.is_leaf_node(depth, board):
            stateValue = objective_function(board, player)
            prevCol, prevShape = prevMove
            return [stateValue, prevCol, prevShape]
        neighbors = self.generate_neighbors(board, player)

        if isMaximizing:
            maxVal = float("-inf")
            maxCol = None
            maxShape = None
            for board, colMove, shapeMove in neighbors:
                value, col, shape = self.minimax(board, depth + 1, False, alpha, beta, [colMove, shapeMove])
                if value > maxVal:
                    maxVal = value
                    maxCol = col
                    maxShape = shape
                alpha = max(alpha, maxVal)
                if beta <= alpha:
                    break
            return [maxVal, maxCol, maxShape]
        else:
            minVal = float("+inf")
            minCol = None
            minShape = None
            for board, colMove, shapeMove in neighbors:
                value, col, shape = self.minimax(board, depth + 1, True, alpha, beta, [colMove, shapeMove])
                if value < minVal:
                    minVal = value
                    minCol = col
                    minShape = shape
                beta = min(beta, minVal)
                if beta <= alpha:
                    break
            return [minVal, minCol, minShape]

    def find(self, state: State, player_turn: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        maximizing_player_turn = player_turn
        minimizing_player_turn = (player_turn + 1) % 2
        self.turn = maximizing_player_turn
        self.maximizing_color = state.players[maximizing_player_turn].color
        self.maximizing_shape = state.players[maximizing_player_turn].shape
        self.maximizing_color = state.players[minimizing_player_turn].color
        self.maximizing_shape = state.players[minimizing_player_turn].shape
        self.state = state
        alpha = float("-inf")
        beta = float("+inf")
        _, col, shape = self.minimax(state.board, 0, True, alpha, beta, [])

        return [col, shape]

