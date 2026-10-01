from board import Board
from ai import AI


class Battleship:
    def __init__(self):
        self.player = Board()
        self.enemy = Board()
        self.ai = AI()
        self._setup()

    def _setup(self):
        # Player fleet
        self.player.place_ship({(1, 1), (1, 2), (1, 3)})
        self.player.place_ship({(4, 1), (4, 2)})

        # Enemy fleet
        self.enemy.place_ship({(2, 2), (2, 3), (2, 4)})
        self.enemy.place_ship({(4, 4), (5, 4)})

    def show(self):
        print("\nYour shots are coordinates like 2,3.")
        print("Ship cells remaining:", self.enemy.remaining_cells())

    def run(self):
        print("Battleship")

        while True:
            self.show()

            raw = input("> ").strip().lower()

            if raw == "q":
                return

            # Convert user's 1-based coordinates to internal 0-based coordinates
            try:
                r, c = map(int, raw.split(","))
                pos = (r - 1, c - 1)
            except ValueError:
                print("Use row,col.")
                continue

            # Check whether coordinate is inside the board
            if not (0 <= pos[0] < Board.SIZE and 0 <= pos[1] < Board.SIZE):
                print("Outside board.")
                continue

            # Prevent repeated player shots
            if pos in self.enemy.shots:
                print("Already fired there.")
                continue

            # Player fires at enemy
            previous_sunk = len(self.enemy.sunk_ships())

            hit = self.enemy.fire(pos)

            print("HIT!" if hit else "MISS!")

            # Check whether a particular enemy ship was sunk
            if hit:
                current_sunk = len(self.enemy.sunk_ships())

                if current_sunk > previous_sunk:
                    print("You sank a ship.")

            # Check whether entire enemy fleet is sunk
            if self.enemy.all_sunk():
                print("You sank the fleet.")
                return

            # AI turn
            ai_pos = self.ai.choose()

            # Handle situation where AI has no remaining cells
            if ai_pos is None:
                print("AI has no remaining shots.")
                return

            print(
                "AI fired at",
                f"{ai_pos[0] + 1},{ai_pos[1] + 1}"
            )

            # AI fires at player's board
            previous_sunk = len(self.player.sunk_ships())

            ai_hit = self.player.fire(ai_pos)

            if ai_hit:
                print("AI scored a hit.")
            else:
                print("AI missed.")

            # Tell AI whether its shot was a hit or miss
            self.ai.report_result(ai_hit)

            # Check whether AI sank one of the player's ships
            if ai_hit:
                current_sunk = len(self.player.sunk_ships())

                if current_sunk > previous_sunk:
                    print("AI sank a ship.")

            # Check whether AI sank entire player fleet
            if self.player.all_sunk():
                print("AI sank your fleet.")
                return
