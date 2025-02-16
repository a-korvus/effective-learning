"""Some tests for checking of custom mineswipper implementation."""

import pytest
from block_01.mineswipeer import GameBoard


def test_invalid_mine_count() -> None:
    """Проверка ограничения на количество мин."""
    board_size = 3
    max_mines = board_size ** 2 - 1

    with pytest.raises(ValueError):
        GameBoard(board_size, max_mines + 1)


def test_correct_mine_count() -> None:
    """Проверка размещения корректного количества мин.

    Соответствие заданного количества мин и фактического размещения на доске.
    """
    board_size = 3
    mines = 5
    actual_mines = 0

    board: GameBoard = GameBoard(board_size, mines)
    for row in board._board:
        for cell in row:
            if cell.mine:
                actual_mines += 1

    assert actual_mines == mines
