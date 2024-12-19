import numpy as np


class Ship:
    def __init__(self, name, length, width) -> None:
        # The name of the ship.
        self.name = name
        # The marker to represent the ship on the board.
        self.marker = self.name[0]
        # The width and length of the ship.
        self.width = width
        self.length = length

    def create(self, coords: list):
        # Stack the list of coordinates into a 2D array.
        self.shape_coords = np.vstack(coords).T
        # Separate the row and column coordinates.
        self.shape_row_coords = self.shape_coords[0, :]
        self.shape_col_coords = self.shape_coords[1, :]

        # Now that the ship was created, allocate its size.
        self.size = len(self.shape_row_coords)
        # Initialize the number of hits to 0.
        self.hits = 0
        self.is_sunk = False
    
    def print_ship(self):
        # Create an empty grid of cells with a data type of str.
        # Serves debugging, visualisation purposes only.
        grid = np.empty((self.length, self.width), dtype=str)
        # Populate the grid with spaces.
        grid[:] = ' '
        # Populate the specific grid coordinates with the ship's marker.
        for r, c in zip(self.shape_row_coords, self.shape_col_coords):
            grid[r, c] = self.marker

        """Print the ship's grid representation."""
        # Print column labels
        print(' ', end=' ')
        for col in range(self.width):
            print(' ', col, end=' ')
        print()

        # Print intermediate borders
        print('  ' + '+---' * self.width + '+')
        
        # Print row labels and cell values
        for i, row in enumerate(grid):
            print(i, end=' ')
            for cell in row:
                print(f'| {cell}', end=' ')
            print('|')

            # Print intermediate borders
            print('  ' + '+---' * self.width + '+')

    def __repr__(self) -> str:
        return f"Ship name: {self.name}, Width: {self.width}, Length: {self.length}"
    
    
class KoKo(Ship):
    """Convenience class for KoKo ship.
    
    The ship shape is:
        K K
    """
    def __init__(self) -> None:
        super().__init__('KoKo', 1, 2)

        coords = np.vstack([[0, 0], [0, 1]])
        self.create(coords)


class Cruiser(Ship):
    """Convenience class for Cruiser ship.
    
    The ship shape is:
        C C
        C C
    """
    def __init__(self) -> None:
        super().__init__('Cruiser', 2, 2)

        coords = [[0, 0], [0, 1], [1, 0], [1, 1]]
        self.create(coords)


class Submarine(Ship):
    """Convenience class for Submarine ship.
    
    The ship shape is:
        S S S
    """
    def __init__(self) -> None:
        super().__init__('Submarine', 1, 3)

        coords = [[0, 0], [0, 1], [0, 2]]
        self.create(coords)


class Frigate(Ship):
    """Convenience class for Frigate ship.
    
    The ship shape is:
        F F F F
    """
    def __init__(self) -> None:
        super().__init__('Frigate', 1, 4)

        coords = [[0, 0], [0, 1], [0, 2], [0, 3]]
        self.create(coords)


class AircraftCarrier(Ship):
    """Convenience class for Aircraft Carrier ship.
    
    The ship shape is:
        A A A
        A A A
    """
    def __init__(self) -> None:
        super().__init__('Aircraft Carrier', 2, 3)

        coords = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2]]
        self.create(coords)


class Unicorn(Ship):
    """Convenience class for Unicorn ship.
    
    The ship shape is:
          U
        U U U
          U
    """
    def __init__(self) -> None:
        super().__init__('Unicorn', 3, 3)

        coords = [[0, 1], [1, 0], [1, 1], [1, 2], [2, 1]]
        self.create(coords)