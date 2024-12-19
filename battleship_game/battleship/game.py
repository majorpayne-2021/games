from battleship.ship import Ship
from battleship.board import Cell, Board

import random


def populate_board_random(board: Board, *ships: list[Ship], max_attempts=100) -> int:
    """Populate the board with ships.
    
    Parameters
    ----------
    board : Board
        The board to populate with ships.
    max_attempts : int, optional
        The maximum number of attempts to place a ship, by default 100.
    ships : list[Ship]
        The ships to place on the board.

    Returns
    -------
    attempts : int
        The number of attempts it took to place all ships.
    """
    for ship in ships:
        attempts = 0
        while (attempts < max_attempts):
            row = random.randint(0, board.rows - 1)
            col = random.randint(0, board.cols - 1)
            orientation = random.choice(['H', 'V'])

            if board.add_ship(row, col, orientation, ship):
                break
            else:
                attempts += 1

            if attempts > max_attempts:
                raise RuntimeError(f"Unable to place ship {ship.name} on board. Try increasing the number of iterations or expanding the board.")

    return attempts


class Strategy:
    def __init__(self, board: Board):
        self.board = board

    def random_hunt(self, print_progress=False) -> int:
        """Choose a random cell in the board and determine whether it was a hit or miss.
        
        Returns
        -------
        int
            The number of attempts it took to find a ship.
        """
        attempts = 0

        while True:
            attempts += 1
            print(f"\nAttempt #{attempts}:")

            # Choose a random row and column.
            row = random.randint(0, self.board.rows - 1)
            col = random.randint(0, self.board.cols - 1)

            self.board.fire(row, col)

            if print_progress:
                self.board.print_board()

            if self.board.ships_remaining == 0:
                print("\nAll ships have been sunk!\n")
                break

        return attempts