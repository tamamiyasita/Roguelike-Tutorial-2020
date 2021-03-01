from constants import *

class SquareGrid:
    def __init__(self, width, height, walls):
        self.width = width
        self.height = height
        # self.walls = [(x,y) for x, y in zip(walls.x, walls.y)]
        self.walls = []
        for y in range(height):
            for x in range(width):
                if walls[x][y] == TILE.WALL:
                    self.walls.append((x, y))

            


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


class GridWithWeights(SquareGrid):
    def __init__(self, width, height, walls):
        super().__init__(width, height, walls)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)

from queue import PriorityQueue

def dijkstra_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    # path.append(start)
    # path.reverse()
    return path



from queue import Queue
def breadth_first_search(graph, start, goal):
    frontier = Queue()
    frontier.put(start)
    came_from = dict()
    came_from[start] = None
    path = []

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break
        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current
    
    while current != start:
        path.append(current)
        current = came_from[current]

    return path


