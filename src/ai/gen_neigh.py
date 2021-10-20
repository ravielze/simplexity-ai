from src.constant import ShapeConstant
from src.model import Board, Piece, Player
import copy


def generate_neighbors(board: Board, player: Player):
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
