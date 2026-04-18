def create_ocean_grid():
    grid = []
    for row in range(10):
        grid.append([])
        for col in range(10):
            grid[row].append({
                "has_ship": False,
                "shot": None,       # None | "miss" | "hit"
                "preview": None     # None | "valid" | "invalid"
            })
    return grid


def create_screen_grid():
    grid = []
    for row in range(10):
        grid.append([])
        for col in range(10):
            grid[row].append({
                "shot": None,   # None | "miss" | "hit"
            })
    return grid


def create_ship_info():
    ships = []
    for i in range(5):
        ships.append({
            "row": 0,
            "col": 0,
            "orientation": 0,
            "length": 0,
            "hits": 0
        })
    return ships