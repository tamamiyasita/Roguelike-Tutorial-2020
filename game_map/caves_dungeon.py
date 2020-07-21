import random
from map_tool import initialize_tiles, is_blocked
from map_sprite_set import MapobjPlacement


class CavesDungeon:
    def __init__(self, width, height):
        self.old_tiles = initialize_tiles(width, height)
        self.height = len(self.old_tiles[0])
        self.width = len(self.old_tiles)

        self.initialize_grid()
        for step in range(4):
            self.tiles = self.do_simulation_step()

    def initialize_grid(self):
        chance_to_start_alive = 0.4

        for row in range(self.height):
            for column in range(self.width):
                if random.random() <= chance_to_start_alive:
                    self.old_tiles[column][row] = 1

    def count_alive_neighbors(self, x, y):
        alive_count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbor_x = x + i
                neighbor_y = y + j
                if i == 0 and j == 0:
                    continue
                elif neighbor_x < 0 or neighbor_y < 0 or neighbor_y >= self.height or neighbor_x >= self.width:
                    alive_count += 1
                elif self.old_tiles[neighbor_x][neighbor_y] == 1:
                    alive_count += 1
        return alive_count

    def is_blocked(self, x, y):
        return is_blocked(self.tiles, x, y)

    def do_simulation_step(self):
        death_limit = 3
        birth_limit = 4.5
        new_tile = initialize_tiles(self.width, self.height)
        pos_set = 0
        self.player_pos = []

        for x in range(1, self.width-1):
            for y in range(1, self.height-1):
                alive_neighbors = self.count_alive_neighbors(x, y)
                if self.old_tiles[x][y] == 1:
                    if alive_neighbors < death_limit:
                        new_tile[x][y].blocked = False
                        new_tile[x][y].block_sight = False
                        pos_set += 1
                        if pos_set == 60:
                            self.player_pos = [x, y]
                            print(self.player_pos)

                    else:
                        new_tile[x][y].blocked = True
                        new_tile[x][y].block_sight = True
                else:
                    if alive_neighbors > birth_limit:
                        new_tile[x][y].blocked = True
                        new_tile[x][y].block_sight = True
                    else:
                        new_tile[x][y].blocked = False
                        new_tile[x][y].block_sight = False

        return new_tile
