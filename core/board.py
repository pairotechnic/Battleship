def create_ocean_grid():
    grid = []
    for row in range(10):
        grid.append([])
        for col in range(10):
            grid[row].append([0, 0, 0])
    return grid


def create_screen_grid():
    grid = []
    for row in range(10):
        grid.append([])
        for col in range(10):
            grid[row].append([0, 0])
    return grid


def create_ship_info():
    ships = []
    for i in range(5):
        ships.append([0]*5)
    return ships