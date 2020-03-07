from rotteno import rotteno
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class RottenoFrameGenerator:
    def __init__(self, input_grid, num_frames):
        self.curr_frame = 0
        self.num_frames = num_frames
        self.rotteno = rotteno(input_grid)

    def __iter__(self):
        return self

    def __next__(self):
        self.curr_frame += 1
        if self.curr_frame < self.num_frames:
            self.advance_frame()
            return self.rotteno.grid
        raise StopIteration

    def advance_frame(self):
        self.rotteno.update_grid()

    def get_grid(self):
        return self.rotteno.grid


def RottenoFrameTest(grid):
    from helper import rotteno_colormap as cmap
    num_minutes = rotteno(grid).turns_until_rot() + 1
    if num_minutes == 0:
        num_minutes = 10
    rotten = RottenoFrameGenerator(grid, num_minutes)
    for idx, img in enumerate(rotten):
        plt.imshow(img, cmap=cmap)
        plt.title(f"{idx} minutes")
        plt.axis('off')
        plt.show()


def RottenGIF(grid, file_name):
    from helper import rotteno_colormap as cmap

    num_minutes = rotteno(grid).turns_until_rot() + 1
    if num_minutes == 0:
        num_minutes = 10
    rotten = RottenoFrameGenerator(grid, num_minutes)

    fig = plt.figure()
    ax = plt.axes()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    im = plt.imshow(grid, interpolation='none', cmap=cmap)

    def animate(idx):
        if idx == 0:
            fig.suptitle(f'Day Zero')
            im.set_array(rotten.get_grid())
            return [im]
        else:
            fig.suptitle(f'Day {idx}')
            rotten.advance_frame()
            im.set_array(rotten.get_grid())
            return [im]

    anim = FuncAnimation(fig, animate, frames=num_minutes, interval=1000)
    anim.save(file_name, dpi=100, writer='ffmpeg')
    # plt.show()


def random_grid(x_dim, y_dim):
    import random
    p_rotten = .2
    p_fresh = p_rotten + .6
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
    import os
    path = os.getcwd() + "\\output"

    x_dim = 25
    y_dim = 25
    grid = random_grid(x_dim, y_dim)
    print("Generating MP4")
    RottenGIF(grid, path + "\\rotteno.mp4")
    print("Generating GIF")
    os.system(f"ffmpeg -y -i {path}\\rotteno.mp4 {path}\\rotteno.gif")

