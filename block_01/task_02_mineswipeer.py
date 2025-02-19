"""A simple Python script to generate a Minesweeper game board."""

import random


class Cell:
    """A cell in the Minesweeper game board."""

    def __init__(
        self,
        around_mines: int,
        mine: bool,
        fl_open: bool = False,
    ) -> None:
        """Initialize a Cell on the Minesweeper game board.

        Args:
            around_mines (int): Number of mines around the cell.
            mine (bool): If the cell contains a mine.
            fl_open (bool, optional): If the cell is open. Defaults to False.
        """
        self._around_mines = around_mines
        self._mine = mine
        self._fl_open = fl_open

    @property
    def around_mines(self) -> int:
        """Get the number of mines around the cell.

        Returns:
            int: Number of mines around the cell.
        """
        return self._around_mines

    @around_mines.setter
    def around_mines(self, val: int) -> None:
        """Set the number of mines around the cell."""
        if not isinstance(val, int):
            raise TypeError("Must be an integer")
        self._around_mines = val

    @property
    def mine(self) -> bool:
        """Check if the cell contains a mine.

        Returns:
            bool: True if the cell contains a mine, False otherwise.
        """
        return self._mine

    @mine.setter
    def mine(self, val: bool) -> None:
        """Set the cell to contain a mine."""
        self._mine = val

    @property
    def is_open(self) -> bool:
        """Check if the cell is open.

        Returns:
            bool: True if the cell is open, False otherwise.
        """
        return self._fl_open


class GameBoard:
    """A Minesweeper game board."""

    def __init__(self, size: int, mines: int) -> None:
        """
        Initialize a GameBoard with a given size and number of mines.

        The board is represented as a two-dimensional list of Cell objects.
        Mines are placed randomly on the board. The number of mines in adjacent
        cells is calculated for each non-mine cell.

        Args:
            size (int): The width and height of the square game board.
            mines (int): The total number of mines to place on the board.

        Raises:
            ValueError: If the number of mines is
            greater than or equal to the total cells.
        """
        if mines >= size**2:
            raise ValueError("Too many mines")

        self._size = size
        self._mines = mines
        self._board: list[list[Cell]] = [
            [Cell(0, False) for _ in range(size)] for _ in range(size)
        ]
        self._place_mines()
        self._calculate_adjacent_mines()

    def _place_mines(self) -> None:
        """Randomly place mines on the board.

        Uses `random.sample` to ensure unique position for each mine.
        """
        positions: list[int] = random.sample(
            range(self._size**2),
            self._mines,
        )
        for pos in positions:
            row: int = pos // self._size
            col: int = pos % self._size
            selected_cell: Cell = self._board[row][col]
            selected_cell.mine = True

    def _calculate_adjacent_mines(self) -> None:
        """Calculate and set the number of adjacent mines for each cell.

        For each non-mine cell, check all valid neighbors and count the mines.
        """
        for row in range(self._size):
            for col in range(self._size):
                current_cell: Cell = self._board[row][col]
                if current_cell.mine:
                    continue

                count: int = 0
                for n_row, n_col in self._neighbors(row, col):
                    if self._board[n_row][n_col].mine:
                        count += 1

                current_cell.around_mines = count

    def _neighbors(self, row: int, col: int) -> list[tuple[int, int]]:
        """Get valid neighbor coordinates for a cell at (row, col).

        Neighbors are the eight adjacent cells (including diagonals).

        Args:
            row (int): Row index of the cell.
            col (int): Column index of the cell.

        Returns:
            list[tuple[int, int]]: list of (row, col) tuples
            for valid neighbors.
        """
        neighbors: list[tuple[int, int]] = []

        for i in range(max(0, row - 1), min(self._size, row + 2)):
            for j in range(max(0, col - 1), min(self._size, col + 2)):
                if (i, j) != (row, col):
                    neighbors.append((i, j))

        return neighbors

    def show(self) -> None:
        """
        Display the game board in the console.

        Closed cells are displayed as '#' and open cells display
        either the number of adjacent mines or '*' if the cell is a mine.
        """
        for row in self._board:
            row_display: list[str] = []
            for cell in row:
                if not cell.is_open:
                    row_display.append("#")
                elif cell.mine:
                    row_display.append("*")
                else:
                    row_display.append(str(cell.around_mines))
            print(" ".join(row_display))


if __name__ == "__main__":
    board_game = GameBoard(10, 12)
    board_game.show()
