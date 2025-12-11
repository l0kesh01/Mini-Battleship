from app.game.game_manager import GameManager
import random

game = GameManager("Player1", "Player2")

print("=== Initial Boards ===")
game.display_boards()

# simulate random play
print("\n=== Game Simulation ===")
for turn in range(30):
    current = game.current_turn
    r, c = random.randint(0, 11), random.randint(0, 11)
    result = game.make_move(current, r, c)
    print(f"{current} fires at ({r}, {c}) -> {result}")

    if game.winner:
        print(f"\n🎉 Winner: {game.winner}")
        break

print("\n=== Final Boards ===")
game.display_boards()
