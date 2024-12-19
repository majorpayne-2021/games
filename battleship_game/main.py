from battleship.ship import *
from battleship.board import Board
from battleship.game import *

if __name__ == '__main__':
    # Create board.
    board = Board(5, 10)
    # Populate board with random positions of ships.
    attempts = populate_board_random(board, KoKo(), Cruiser(), Submarine(), Frigate(), AircraftCarrier(), Unicorn())
    print(f"Board populated with ships in {attempts} random attempts.")
    print(f"Board has {board.ships_remaining} ships.")
    board.print_board()
    print()

    # Create the strategy object.
    strategy = Strategy(board)

    # Randomly hunt for ships.
    print("Choosing a random hit strategy.")
    attempts = strategy.random_hunt(print_progress=True)
    print(f"Random hunt took {attempts} attempts to hit all of the ships.")
