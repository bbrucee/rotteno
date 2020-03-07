class OrangeNode:
    def __init__(self, freshness, x, y, up=None, down=None, right=None, left=None):
        self.val = freshness
        self.up = up
        self.down = down
        self.right = right
        self.left = left


class RottenoGrid:
    def __init__(self, x_dim, y_dim):
        self.grid_dict = {}
        self.x_dim = x_dim
        self.y_dim = y_dim

    def insert(self, freshness, x, y):
        # TODO

    def output_grid(self):
        # TODO
        grid

        return grid


