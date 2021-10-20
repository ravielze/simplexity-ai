from time import time
from src.ai.gen_neigh import generate_neighbors
from src.ai.obj_function import obj_function
from src.utility import is_win, is_full

from src.model import State, Board, Player

from typing import Tuple
import random


class LocalSearch:
    def __init__(self):
        pass

    def localSearch(self, board: Board, player: Player, isEnemy: bool, enemy: Player):
        neighbors = generate_neighbors(board, player, 0, 0)
        random.shuffle(neighbors)

        maxVal = float("-inf")
        maxCol = None
        maxShape = None
        for neighborBoard, colMove, shape in neighbors:
            neighborValue = obj_function(neighborBoard, player)
            enemyVal = 0
            if not isEnemy:
                enemyVal, _, _ = self.localSearch(neighborBoard, enemy, True, player)

            if (neighborValue - enemyVal) >= maxVal:
                maxVal = neighborValue
                maxCol = colMove
                maxShape = shape
            else:
                break
        return [maxVal, maxCol, maxShape]

    def find(self, state: State, player_turn: int, thinking_time: float):
        self.thinking_time = time() + thinking_time
        _, col, shape = self.localSearch(
            state.board,
            state.players[player_turn],
            False,
            state.players[((player_turn + 1) % 2)],
        )

        return [col, shape]
