import random


class AI:
    def __init__(self, size=6):
        self.size = size
        self.tried = set()
        self.last_shot = None
        self.last_hit = None

    def choose(self):
        # No shots remaining
        if len(self.tried) == self.size * self.size:
            return None

        # If the previous shot was a hit,
        # prefer nearby untried cells
        if self.last_hit is not None:
            r, c = self.last_hit

            nearby = [
                (r - 1, c),  # up
                (r + 1, c),  # down
                (r, c - 1),  # left
                (r, c + 1)   # right
            ]

            options = [
                pos for pos in nearby
                if 0 <= pos[0] < self.size
                and 0 <= pos[1] < self.size
                and pos not in self.tried
            ]

            if options:
                pos = random.choice(options)
                self.tried.add(pos)
                self.last_shot = pos
                return pos

        # Otherwise choose any untried cell
        options = [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if (r, c) not in self.tried
        ]

        pos = random.choice(options)
        self.tried.add(pos)
        self.last_shot = pos
        return pos

    def report_result(self, hit):
        if hit:
            self.last_hit = self.last_shot
        else:
            self.last_hit = None
