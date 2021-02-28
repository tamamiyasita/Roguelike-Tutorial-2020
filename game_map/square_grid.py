class SquareGrid:
    def __init__(self, width, height, walls):
        self.width = width
        self.height = height
        self.walls = [(x,y) for x, y in zip(walls.x, walls.y)]


    def in_bounds(self, id):
        (x, y) = id
        return 1 < x < self.width -1 and 1 < y < self.height -1

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        neighbors = [(x, y+1), (x, y-1), (x+1, y),(x-1, y),(x+1, y+1),(x+1,y-1),(x-1, y+1),(x-1,y-1)]
        if (x + y) % 2 == 0:
            neighbors.reverse()
        result = filter(self.in_bounds, neighbors)
        result = filter(self.passable, result)
        return result

    