from app.game.logic import Board
import random

board = Board()
board.auto_place_all_ships()
board.print_board()

print("\n-- Shooting phase --")
for _ in range(10):
    r, c = random.randint(0, 11), random.randint(0, 11)
    result = board.receive_shot(r, c)
    print(f"Shot at ({r}, {c}) -> {result}")

print("\nBoard after shots:")
board.print_board()

if board.all_sunk():
    print("\nAll ships destroyed!")
else:
    print("\nSome ships still alive...")