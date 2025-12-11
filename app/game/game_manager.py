from app.game.logic import Board

class GameManager:
    def __init__(self, player1: str, player2: str):
        """Initialize a 2-player Battleship game."""
        self.players = [player1, player2]
        self.boards = {
            player1: Board(),
            player2: Board()
        }
        for board in self.boards.values():
            board.auto_place_all_ships()

        self.current_turn = player1
        self.winner = None

    def get_opponent(self, player: str):
        return self.players[1] if self.players[0] == player else self.players[0]

    def make_move(self, player: str, row: int, col: int):
        """Process a move from a player."""
        if self.winner:
            return f"Game over! {self.winner} already won."
        
        if player != self.current_turn:
            return "Not your turn."

        opponent = self.get_opponent(player)
        result = self.boards[opponent].receive_shot(row, col)

        # Switch turn only if miss
        if result.startswith("miss") or result.startswith("already"):
            self.current_turn = opponent

        # Check if opponent has lost
        if self.boards[opponent].all_sunk():
            self.winner = player
            return f"{result} — {player} wins!"

        return result

    def display_boards(self):
        """Print both boards (for testing only)."""
        for p, board in self.boards.items():
            print(f"\n{p}'s Board:")
            board.print_board()
