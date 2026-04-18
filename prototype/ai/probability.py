# Standard Library Imports

# Third-Party Application Imports

# Local Application Imports


def compute_probability_grid(screen_grid, grid_size, ship_lengths):
    """
    Returns a new grid with scores
    """

    # create a fresh grid
    score_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    # For each cell of screen grid, try all possible legal ship positions,
    # Given some positions may already be shot (hit/miss)
    # Compute the total possibilities for each unshot
    # This currently doesn't account for some ships already being sunk,
    # Nor does it switch to targeting adjacent cells after a hit
    for length in ship_lengths:
        for j in range(grid_size+1-length):
            for k in range(grid_size):
                valid_hor = True
                valid_vert = True
                for inc in range (length):
                    if screen_grid[k][j+inc]["shot"] == "miss":
                        valid_hor = False
                    if screen_grid[j+inc][k]["shot"] == "miss":
                        valid_vert = False

                if valid_hor:
                    for inc in range (length):
                        if not screen_grid[k][j+inc]["shot"]:
                            score_grid[k][j+inc] += 1
                if valid_vert:
                    for inc in range (length):
                        if not screen_grid[j+inc][k]["shot"]:
                            score_grid[j+inc][k] += 1

    return score_grid

def get_best_move(score_grid, grid_size):
    # Add up the total of all possibilities
    # Find the maximum possibilities value

    max_val = 0
    best_pos = (None, None)

    for row in range(grid_size):
        for column in range(grid_size):
            if score_grid[row][column] > max_val:
                max_val = score_grid[row][column]
                best_pos = (row, column)

    return max_val, best_pos