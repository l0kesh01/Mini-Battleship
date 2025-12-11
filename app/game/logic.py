import random

# --- Configuration ---
BOARD_SIZE = 12

# Ship definitions: name -> (length, width, count)
SHIP_SPECS = {
    "Carrier": (4, 2, 1),      # 4x2 rectangle
    "Battleship": (5, 1, 1),
    "Cruiser": (3, 1, 1),
    "Submarine": (3, 1, 1),
    "Destroyer": (2, 1, 2)
}


class Board:
    def __init__(self):
        # Create an empty 12x12 board filled with water (~)
        self.grid = [["~" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.ships = []

    def print_board(self):
        """Prints the board nicely for debugging."""
        print("    " + " ".join(f"{i:2}" for i in range(BOARD_SIZE)))
        for i, row in enumerate(self.grid):
            print(f"{i:2}  " + " ".join(row))

    def can_place(self, coords):
        """Check if a ship can be placed at given coordinates (no overlap and within bounds)."""
        return all(
            0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.grid[r][c] == "~"
            for r, c in coords
        )

    def place_ship(self, name, length, width=1):
        """Place a ship randomly (length x width) without overlapping."""
        placed = False
        attempts = 0
        while not placed and attempts < 500:
            attempts += 1
            orientation = random.choice(["H", "V"])
            if orientation == "H":
                row = random.randint(0, BOARD_SIZE - width)
                col = random.randint(0, BOARD_SIZE - length)
                coords = [(row + w, col + l) for w in range(width) for l in range(length)]
            else:  # Vertical orientation
                row = random.randint(0, BOARD_SIZE - length)
                col = random.randint(0, BOARD_SIZE - width)
                coords = [(row + l, col + w) for l in range(length) for w in range(width)]

            if self.can_place(coords):
                for r, c in coords:
                    self.grid[r][c] = "O"
                self.ships.append({"name": name, "coords": coords})
                placed = True

        if not placed:
            raise RuntimeError(f"Could not place {name} after {attempts} attempts")

    def auto_place_all_ships(self):
        """Automatically places all ships on the board."""
        for name, (length, width, count) in SHIP_SPECS.items():
            for i in range(count):
                ship_name = f"{name}#{i+1}" if count > 1 else name
                self.place_ship(ship_name, length, width)
    def receive_shot(self, row: int, col: int):
        """
        Process a shot fired at (row, col).
        Returns:
            "hit" if a ship was hit,
            "miss" if no ship was there,
            "sunk <ship_name>" if a ship is sunk,
            "already" if the cell was already targeted.
        """
        # --- Check if coordinates are valid ---
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return "invalid"

        current = self.grid[row][col]

        # --- Already targeted ---
        if current in ("X", "M"):
            return "already"

        # --- Hit detection ---
        if current == "O":
            self.grid[row][col] = "X"  # mark hit

            # find which ship was hit
            for ship in self.ships:
                if (row, col) in ship["coords"]:
                    ship["coords"].remove((row, col))
                    if not ship["coords"]:  # ship fully destroyed
                        return f"sunk {ship['name']}"
                    return "hit"

        # --- Miss ---
        self.grid[row][col] = "M"
        return "miss"

    def all_sunk(self):
        """Check if all ships have been sunk."""
        return all(len(ship["coords"]) == 0 for ship in self.ships)

