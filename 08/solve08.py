import numpy as np  

INPUT_FILENAME ="input"

PART = 2

def count_visible_trees(grid: np.array):
    grid_len = len(grid)
    count = 4*(grid_len - 1)
    for i in range(1, grid_len - 1):
        for j in range(1, grid_len - 1):
            obstacles = [
                            max(grid[:,j][0:i]), # top
                            max(grid[:,j][i+1:]), # bottom
                            max(grid[i,:][:j]), # left
                            max(grid[i,:][j+1:]) # right
                        ]
            if grid[i][j] > min(obstacles):
                count += 1
    return count


def get_scenic_score(grid: np.array, tree_coords: tuple):
    i, j = tree_coords
    grid_len = len(grid)
    assert i in range(grid_len) and j in range(grid_len), \
            f"{i},{j} are not valid coordinates on the given grid"
    my_tree = grid[i][j]
    scenic_score = 1
    targets = [
                grid[:,j][0:i][::-1], # top
                grid[:,j][i+1:], # bottom
                grid[i,:][:j][::-1], # left
                grid[i,:][j+1:] # right
            ]
    for target in targets:
        target_score = 0
        for tree in target:
            target_score += 1
            if tree >= my_tree:
                break
        scenic_score = scenic_score*target_score if target_score > 0 else scenic_score
    return scenic_score


if __name__ == "__main__":
    with open(INPUT_FILENAME) as input_f:
        grid = [list(line) for line in input_f.read().splitlines()]

    grid = np.array(grid)

    if(PART == 1):
        num_of_visible_trees = count_visible_trees(grid)

        print(f"The number of visible trees is: {num_of_visible_trees}")
    elif(PART == 2):
        highest_scenic_score = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                scenic_score = get_scenic_score(grid, (i, j))
                if scenic_score > highest_scenic_score:
                    highest_scenic_score = scenic_score
        print(f"The highest possible scenic score is {highest_scenic_score}")
