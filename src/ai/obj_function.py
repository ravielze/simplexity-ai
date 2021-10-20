from typing import Tuple

from src.model import Piece, Board, State, Player
from src.constant import ShapeConstant, GameConstant
from src.utility import is_out


# Pemetaan streak: poin
POINT_MAPPING = {
    1: 0,
    2: 2,
    3: 6,
    4: 500
}


def count_streak_point(board: Board, row: int, col: int, player: Player) -> int:
    # Fungsi untuk menghitung jumlah poin semua streak yang mungkin dari bidak
    # pada posisi row, col pada arah kiri atas(1,-1), atas(1,0), kanan atas(1,1), dan kanan(0,1)
    piece = board[row, col]

    # Kasus tidak ada bidak pada posisi row, col
    if piece.shape == ShapeConstant.BLANK:
        return -1

    # main_streak_way merupakan posisi yang akan dicek oleh current bidak
    main_streak_way = [(-1, -1), (0, 1), (-1, 1), (-1, 0)]

    # total value
    total_value = 0

    # Cek berdasarkan color atau shape
    for prior in GameConstant.WIN_PRIOR:
        value = 0
        if (prior == "SHAPE" and piece.shape != player.shape):
            continue
        if (prior == "COLOR" and piece.color != player.color):
            continue
        for row_ax, col_ax in main_streak_way:
            # streak : total streak skrg
            streak = 1
            row_ = row + row_ax
            col_ = col + col_ax
            for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                # Kasus jika bidak di luar board
                if is_out(board, row_, col_):
                    break

                # Pengecekan streak berhenti atau tidak
                shape_condition = (
                    prior == GameConstant.SHAPE
                    and piece.shape != board[row_, col_].shape
                )
                color_condition = (
                    prior == GameConstant.COLOR
                    and piece.color != board[row_, col_].color
                )

                # Kasus streak berhenti / tidak ada streak
                if shape_condition or color_condition:
                    break

                # Kasus jika ada streak
                else:
                    # Saat ketemu streak 2, cek bidak pada arah berlawanan
                    if streak == 1:
                        row_ax2 = row_ax * -1
                        col_ax2 = col_ax * -1
                        row_2 = row + row_ax2
                        col_2 = col + col_ax2

                        # Pengecekan apakah pada arah berlawanan di luar board atau tidak terdapat bidak pada arah berlawanan
                        if not(is_out(board, row_2, col_2)):
                            # Bidak pada arah berlawanan
                            piece_opp_direction = board[row_2, col_2]
                            if piece_opp_direction.shape != ShapeConstant.BLANK:
                                # Pengecekan apakah shape atau color arah berlawanan sama atau tidak
                                shape_condition2 = (
                                    prior == GameConstant.SHAPE
                                    and piece.shape == board[row_2, col_2].shape
                                )
                                color_condition2 = (
                                    prior == GameConstant.COLOR
                                    and piece.color == board[row_2, col_2].color
                                )

                                # Kasus shape atau color bidak pada arah berlawanan sama,
                                # sehingga streak sudah pernah dicek sebelumnya
                                if shape_condition2 or color_condition2:
                                    break

                    row_ += row_ax
                    col_ += col_ax
                    streak += 1

            # Terjemahkan poin dari streak
            value = POINT_MAPPING[streak]
            total_value += value
    # Return value
    return total_value


# Perhitungan obj_value (dengan memperhatikan menguntungkan musuh atau tidak):
# a = obj_function(state, player1)
# b = obj_function(state, player2)
# obj_value = a - b
def obj_function(board: Board, player: Player) -> int:
    column_candidate = list(range(7))
    row = 5
    obj_value = 0
    while row >= 0:
        column_candidate_duplicate = column_candidate.copy()
        for col in column_candidate:
            streak_points = count_streak_point(board, row, col, player)

            # Kasus jika pada row, col tidak terdapat piece (bidak)
            if streak_points == -1:
                column_candidate_duplicate.remove(col)
            # Kasus jika pada row, col terdapat piece (bidak)
            else:
                obj_value += streak_points
        column_candidate = column_candidate_duplicate
        row -= 1
    return obj_value
