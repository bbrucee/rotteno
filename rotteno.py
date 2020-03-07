import collections

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

    def turns_until_rot_bfs(self):
        import collections

        R, C = len(self.grid), len(self.grid[0])

        # queue - all starting cells with rotting oranges
        queue = collections.deque()
        for r, row in enumerate(self.grid):
            for c, val in enumerate(row):
                if val == 2:
                    queue.append((r, c, 0))

        def neighbors(r, c):
            for nr, nc in ((r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)):
                if 0 <= nr < R and 0 <= nc < C:
                    yield nr, nc

        d = 0
        while queue:
            r, c, d = queue.popleft()
            for nr, nc in neighbors(r, c):
                if self.grid[nr][nc] == 1:
                    self.grid[nr][nc] = 2
                    queue.append((nr, nc, d+1))

        if any(1 in row for row in self.grid):
            return -1

        return d


def random_grid(x_dim, y_dim):
    import random
    p_rotten = .2
    p_fresh = p_rotten + .8
    grid = [[0 for _ in range(x_dim)] for _ in range(y_dim)]
    for j in range(x_dim):
        for i in range(y_dim):
            rand_float = random.uniform(0, 1)
            if rand_float < p_rotten:
                grid[i][j] = 2
            elif p_rotten < rand_float < p_fresh:
                grid[i][j] = 1
            else:
                grid[i][j] = 0
    return grid


if __name__ == "__main__":
    from timeit import Timer
    import matplotlib.pyplot as plt

    def bfs(x, y):
        time = rotteno(random_grid(x, y)).turns_until_rot_bfs()

    def brute_force(x, y):
        time = rotteno(random_grid(x, y)).turns_until_rot()


    N = []
    bfs_times = []
    brute_force_times = []
    for x_dim, y_dim in zip(range(10, 1000, 100), range(10, 1000, 100)):
        N.append(x_dim*y_dim)

        t = Timer(lambda: bfs(x_dim, y_dim))
        time = t.timeit(number=20)
        print(f"BFS for {x_dim} x {y_dim}: {time}")
        bfs_times.append(time)

        t = Timer(lambda: brute_force(x_dim, y_dim))
        time = t.timeit(number=20)
        print(f"Brute Force for {x_dim} x {y_dim}: {time}")
        brute_force_times.append(time)

    plt.plot(N, bfs_times)
    plt.plot(N, brute_force_times)
    plt.legend(["BFS", "Brute Force"])
    plt.title("Rotten Oranges: BFS vs Brute Force Runtimes on Random Square Grids")
    plt.xlabel("Number of cells in the grid")
    plt.ylabel("Time (seconds)")
    plt.show()
