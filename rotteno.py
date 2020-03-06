class rotteno:
    def __init__(self, grid):
        self.grid = grid
        self.time = None

    def get_counts(self):
        count_0 = sum([row.count(0) for row in self.grid])
        count_1 = sum([row.count(1) for row in self.grid])
        count_2 = sum([row.count(2) for row in self.grid])
        return count_0, count_1, count_2

    def update_grid(self):
        output_grid = [x[:] for x in self.grid]
        for i, _ in enumerate(self.grid):
            for j, _ in enumerate(self.grid[0]):
                if self.grid[i][j] == 2:
                    if i < len(self.grid) - 1:
                        if self.grid[i + 1][j] == 1:
                            output_grid[i + 1][j] = 2
                    if i > 0:
                        if self.grid[i - 1][j] == 1:
                            output_grid[i - 1][j] = 2
                    if j < len(self.grid[0]) - 1:
                        if self.grid[i][j + 1] == 1:
                            output_grid[i][j + 1] = 2
                    if j > 0:
                        if self.grid[i][j - 1] == 1:
                            output_grid[i][j - 1] = 2
        self.grid = output_grid

    def turns_until_rot(self):
        prev_counts = None
        minute = 0
        while self.get_counts()[1] != 0:
            if prev_counts is None:
                prev_counts = self.get_counts()
            elif prev_counts == self.get_counts():
                return -1
            else:
                prev_counts = self.get_counts()

            self.update_grid()
            minute += 1

        return minute
