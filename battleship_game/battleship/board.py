from battleship.ship import Ship

import numpy as np


class Cell:
    def __init__(self, ship: Ship = None) -> None:
        self.ship = ship
        self._miss = False
        self._hit = False

        try:
            self.marker = ship.marker
        except AttributeError:
            self.marker = ' '

    # Create new property attribute for miss
    @property
    def miss(self) -> bool:
        return self._miss
    
    # Setter for hit
    @miss.setter
    def miss(self, value: bool) -> None:
        self._miss = value
        if value:
            self.marker = '-'

    # Create new property attribute for hit
    @property
    def hit(self) -> bool:
        return self._hit
    
    # Setter for miss
    @hit.setter
    def hit(self, value: bool) -> None:
        self._hit = value
        if value:
            self.marker = 'X'

    def __repr__(self) -> str:
        return self.marker


class Board(np.ndarray):
    def __new__(self, rows, cols):
        """Create a new board of size (rows, cols) and initialize the empty numpy array instance as the current class."""
        obj = np.empty((rows, cols), dtype=Cell).view(self)
        return obj

    def __init__(self, rows, cols) -> None:
        # Initialize the number of rows and columns.
        self.rows = rows
        self.cols = cols

        # Initialize the list of ships.
        self.ships = []
        # Initialize the number of ships remaining on the board.
        self.ships_remaining = 0

        # Initialize the board with empty cells of type Cell.
        for r in range(rows):
            for c in range(cols):
                self[r, c] = Cell()

    def add_ship(self, row: int, col: int, orientation: str, ship: Ship) -> bool:
        """Add a ship to the board at coordinate (i, j).
        
        Parameters
        ----------
        row : int
            The row index of the ship's head.
        col : int
            The column index of the ship's head.
        orientation : str
            The orientation of the ship. 'H' for horizontal, 'V' for vertical.
        ship : Ship
            The ship to be added to the board.

        Returns
        -------
        bool
            True if the ship was successfully added to the board, False otherwise.
        """
        try:
            if orientation == 'H':
                row_coords = ship.shape_row_coords
                col_coords = ship.shape_col_coords
            elif orientation == 'V':
                row_coords = ship.shape_col_coords
                col_coords = ship.shape_row_coords

            # First pass through the coordinates ensures that the ship can be placed.
            for r, c in zip(row_coords, col_coords):
                if self[row + r, col + c].ship is not None:
                    return False
        except IndexError:
            # Outside of board bounds.
            return False
        else:
            # Second pass through the coordinates adds the ship to the board.
            for r, c in zip(row_coords, col_coords):
                self[row + r, col + c] = Cell(ship)
            
            # Add the ship with its global coordinates to the list.
            self.ships.append((ship, np.vstack((row_coords + row, col_coords + col)).T))
            # Increment the number of ships remaining on the board.
            self.ships_remaining += 1

            return True
        
    def fire(self, row: int, col: int) -> bool:
        """Fire at a cell on the board.
        
        Parameters
        ----------
        row : int
            The row index of the cell to fire at.
        col : int
            The column index of the cell to fire at.

        Returns
        -------
        bool
            True if the cell was a hit, False if it was a miss.
        """
        print(f"Shooting at coordinates (row, col) = ({row}, {col}).")

        cell = self[row, col]

        if cell.ship is None:
            print("Miss!")
            self[row, col].miss = True

            return False
        elif cell.hit:
            print(f"Ship '{cell.ship.name}' already hit at the given coordinates!")
            return False
        elif cell.ship.is_sunk:
            print(f"Ship '{cell.ship.name}' already sunk!")

            return False
        else:
            print(f"Ship '{cell.ship.name}' hit!", end=' ')
            cell.ship.hits += 1
            self[row, col].hit = True

            # Update the status of the ships on the board.
            self._update_ship_status()

            if cell.ship.is_sunk:
                print(f"The ship has been sunk!")
                print(f"There are {self.ships_remaining} ships remaining.")
            else:
                print(f"The ship has {cell.ship.size - cell.ship.hits} more hit(s) remaining.")

            return True
        
    def _update_ship_status(self):
        """Update the state of the ships on the board."""
        # Check if any of the ships have been sunk.
        for ship, _ in self.ships:
            # Skip the ship if it has already been sunk.
            if ship.is_sunk:
                continue
            # If the number of hits is equal to the size of the ship, the ship has been sunk.
            elif ship.hits == ship.size:
                # Update the ship's status.
                ship.is_sunk = True
                # Update the number of ships remaining on the board.
                self.ships_remaining -= 1

    def print_board(self):
        """Print the board to the console."""
        if self.rows > 10 or self.cols > 10:
            return
            # raise NotImplementedError("Boards larger than 10x10 are not supported.")

        # Print column labels
        print(' ', end=' ')
        for col in range(self.cols):
            print(' ', col, end=' ')
        print()

        # Print intermediate borders
        print('  ' + '+---' * self.cols + '+')
        
        # Print row labels and cell values
        for i, row in enumerate(self):
            print(i, end=' ')
            for cell in row:
                print(f'| {cell}', end=' ')
            print('|')

            # Print intermediate borders
            print('  ' + '+---' * self.cols + '+')
