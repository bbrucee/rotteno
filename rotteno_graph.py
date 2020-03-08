class OrangeNode:
    def __init__(self, freshness, up=None, down=None, right=None, left=None):
        self.freshness = freshness
        self.up = up
        self.down = down
        self.right = right
        self.left = left

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def set_up(self, up):
        self.up = up

    def set_down(self, down):
        self.down = down


class RottenoGrid:
    def __init__(self, x_dim, y_dim, grid=None):
        if grid:
            self.grid = {}
            self.input_grid(grid)
            self.x_dim = len(grid)
            self.y_dim = len(grid[0])
        else:
            self.grid = {}
            self.x_dim = x_dim
            self.y_dim = y_dim

    def __getitem__(self, coord):
        x, y = coord
        if not self._valid_index(x, y):
            raise IndexError
        if (x, y) in self.grid:
            return self.grid[(x, y)]
        else:
            return None

    def _valid_index(self, x, y):
        return 0 <= x < self.x_dim and 0 <= y < self.y_dim

    def insert(self, freshness, x, y):
        if (x, y) in self.grid:
            raise IndexError
        else:
            orange = OrangeNode(freshness)
            if (x - 1, y) in self.grid:
                self.grid[(x - 1, y)].set_right(orange)
                orange.set_left(self.grid[(x - 1, y)])
            if (x + 1, y) in self.grid:
                self.grid[(x + 1, y)].set_left(orange)
                orange.set_right(self.grid[(x + 1, y)])
            if (x, y - 1) in self.grid:
                self.grid[(x, y - 1)].set_up(orange)
                orange.set_down(self.grid[(x, y - 1)])
            if (x, y + 1) in self.grid:
                self.grid[(x, y + 1)].set_down(orange)
                orange.set_up(self.grid[(x, y + 1)])
            self.grid.update({(x, y): orange})

    def output_grid(self):
        grid = [[0 for _ in range(self.y_dim)] for _ in range(self.x_dim)]
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                if (x, y) in self.grid:
                    if self.grid[(x, y)].freshness:
                        grid[x][y] = 1
                    else:
                        grid[x][y] = 2
                else:
                    grid[x][y] = 0
        return grid

    def input_grid(self, grid):
        for i, _ in enumerate(grid):
            for j, _ in enumerate(grid[0]):
                if grid[i][j] == 2:
                    self.insert(False, i, j)
                elif grid[i][j] == 1:
                    self.insert(True, i, j)

    def turns_until_rot_bfs(self):
        queue = []
        for (x, y), orange in self.grid.items():
            if not orange.freshness:
                queue.append((orange, 0))

        while queue:
            orange, d = queue.pop(0)
            for neighbor in [orange.left, orange.right, orange.up, orange.down]:
                if neighbor and neighbor.freshness:
                    neighbor.freshness = False
                    queue.append((neighbor, d+1))

        if any(orange.freshness for _, orange in self.grid.items()):
            return -1

        return d


if __name__ == "__main__":
    test_grid = [[2,1,1],[1,1,0],[0,1,1]]
    grid = RottenoGrid(3, 3)
    grid.insert(False, 0, 0)
    grid.insert(True, 0, 1)
    grid.insert(True, 0, 2)
    grid.insert(True, 1, 0)
    grid.insert(True, 1, 1)
    grid.insert(True, 2, 1)
    grid.insert(True, 2, 2)
    print(grid.output_grid())

    grid_2 = RottenoGrid(0, 0, test_grid)
    print(grid_2.turns_until_rot_bfs())
    print(grid_2.output_grid())
