import numpy as np
import random
import json 
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


#creates the 101 by 101 maze

class Block:
  def __init__(self):
    self.blocked = False   #false if unblocked
    self.closed = False    #false if not closed


def exists(a, b):
  if(0 <= a <= 100 and 0 <= b <= 100):
    return True
  else: 
    return False


def dfs(x, y, newgrid):
    stack = [(x,y)]
    newgrid[x][y].closed = True

    while stack:
        x, y = stack.pop()
        m = random.randint(0,3) 
        direction = [(1,0), (0,1), (-1,0), (0,-1)]
        x1, y1 = direction[m]
        neighbor_x, neighbor_y = x+x1, y+y1
    
        if(exists(neighbor_x, neighbor_y) and newgrid[neighbor_x][ neighbor_y].closed==False):
            next = newgrid[neighbor_x][ neighbor_y]
            z = random.random()
            if z<0.3:
                next.blocked = True
            else:
                stack.append((neighbor_x, neighbor_y))


def print_it(newgrid):
    for row in newgrid:
        print(" ".join(['X' if cell.blocked else 'O' for cell in row]))


def visualize_grid(grid, highlight_coords=None, highlight_color='purple', delay=50):
    num_rows, num_cols = grid.shape

    # Create empty array to store grid values
    grid_values = np.empty((num_rows, num_cols))
    
    for i in range(num_rows):
        for j in range(num_cols):
            # If a cell is blocked, assign 0; else assign 1.
            if grid[i][j].blocked:
                grid_values[i, j] = 0
            else:
                grid_values[i, j] = 1

    #plot it
    fig, ax = plt.subplots(figsize=(8, 8))

    #make the coords in the bottom right integers
    def format_coord(x, y):
        col = int(x + 0.5)
        row = int(y + 0.5)
        if 0 <= col < num_cols and 0 <= row < num_rows:
            return f"row={row}, col={col}"
        else:
            return f"row={row}, col={col}"

    ax.format_coord = format_coord # set the format_coord function

    im = ax.imshow(grid_values, cmap='gray', interpolation='nearest', origin='upper')
    scatter = ax.scatter([], [], color=highlight_color, s=30)

    def update(frame):
        if highlight_coords and frame < len(highlight_coords):
            row, col = highlight_coords[frame]
            scatter.set_offsets([[col, row]])
        return scatter,

    ani = FuncAnimation(fig, update, frames=len(highlight_coords) if highlight_coords else 0, interval=delay, blit=True)

    plt.title("Grid World")
    plt.show()

def save_grid(grid, filename):
    grid_values = np.empty((grid.shape[0], grid.shape[1]))
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i][j].blocked:
                grid_values[i, j] = 0
            else:
                grid_values[i, j] = 1

    with open(filename, 'w') as f:
        json.dump(grid_values.tolist(), f)

def generate_gridworld(size=101):
    newgrid = np.array([[Block()for _ in range(size)] for _ in range(size)], dtype= object)
    x = random.randint(0, size-1)
    y = random.randint(0, size-1)
    stack = []
    dfs(x, y, newgrid)
    for i in range(size):
        for j in range(size):
            if newgrid[i][j].closed==False:
                dfs(i, j, newgrid)

    return newgrid

def load_grid(filename):
    #load grid from file, returns a 2D list of Block objects
    with open(filename, 'r') as f:
        grid_values = json.load(f)
    size = len(grid_values)
    grid = [[Block() for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            grid[i][j].visited = True
            grid[i][j].blocked = (grid_values[i][j] == 0)

    return grid

def generate_50_gridworlds():
    gridworlds = []
    for i in range(50):
        newgrid = generate_gridworld()
        gridworlds.append(newgrid)

    return gridworlds

if __name__ == "__main__":
    #example gridworld to test the visualization
    newgrid = generate_gridworld()
    print_it(newgrid)
    visualize_grid(newgrid)

    gridworlds = generate_50_gridworlds()

    #save the 50 gridworlds to files
    # make path if it doesn't exist
    if not os.path.exists("gridworlds"):
        os.makedirs("gridworlds")
    for i in range(len(gridworlds)):
        
        save_grid(gridworlds[i], "gridworlds/gridworld" + str(i) + ".json")
