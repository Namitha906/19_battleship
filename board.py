class Board:
    SIZE = 6

    def __init__(self):
        self.ships = []
        self.shots = set()

    def place_ship(self, cells):
        self.ships.append({
            "cells": set(cells),
            "hits": set()
        })

    def fire(self, pos):
        if pos in self.shots:
            return False

        self.shots.add(pos)

        for ship in self.ships:
            if pos in ship["cells"]:
                ship["hits"].add(pos)
                return True

        return False

    def is_ship_sunk(self, ship):
        return ship["cells"] <= ship["hits"]

    def sunk_ships(self):
        return [
            ship for ship in self.ships
            if self.is_ship_sunk(ship)
        ]

    def remaining_cells(self):
        return sum(
            len(ship["cells"] - ship["hits"])
            for ship in self.ships
        )

    def all_sunk(self):
        return bool(self.ships) and all(
            self.is_ship_sunk(ship)
            for ship in self.ships
        )
