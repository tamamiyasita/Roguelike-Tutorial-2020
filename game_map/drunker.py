
import arcade
import random
from constants import *
from game_map.door_check import door_check
from game_map.square_grid import SquareGrid, breadth_first_search, GridWithWeights, dijkstra_search, reconstruct_path, a_star_search, heuristic


class DrunkerWalk:
    def __init__(self, map_width, map_height, dungeon_level=1):
        self.tiles = []
        self.map_width = map_width
        self.map_height = map_height
        self.dungeon_level = dungeon_level
        self.enemy_num = 10 * dungeon_level
        self.item_num = 10 * dungeon_level
        self.PLAYER_POINT = None




        self._percent_goal = .4
        self.walk_iterations = 25000 # パーセントゴールに達しなかった場合には切り離す
        self.weighted_toward_center = 0.15
        self.weighted_toward_previous_direction = 0.7

        self.tiles = [[TILE.WALL for y in range(self.map_height)] for x in range(self.map_width)]
        self.actor_tiles = [[TILE.EMPTY for y in range(self.map_height)] for x in range(self.map_width)]
        self.item_tiles = [[TILE.EMPTY for y in range(self.map_height)] for x in range(self.map_width)]

    def generate_tile(self):
        # 空の2次元配列を作成するか，既存の配列をクリアします．
        self.walk_iterations = max(self.walk_iterations, (self.map_width * self.map_height * 10))
 
        self._filled = 0
        self._previous_direction = None

        self.drunker_dx = random.randint(2, self.map_width-2)
        self.drunker_dy = random.randint(2, self.map_height-2)
        self.filled_goal = self.map_width * self.map_height * self._percent_goal
        self.drunker_dy = random.randint(2, self.map_height)
        self.filled_goal = self.map_width * self.map_height * self._percent_goal

        for i in range(self.walk_iterations):
            self.walk(self.map_width, self.map_height)
            if (self._filled >= self.filled_goal):
                break
        self.place_entities()
        return self.tiles

    def place_entities(self):

        while self.enemy_num > 0:
            x = random.randint(1, self.map_width-1)
            y = random.randint(1, self.map_height-1)

            if self.tiles[x][y] == TILE.EMPTY:
                self.actor_tiles[x][y] = self.dungeon_level# TODO 後でレベルの調整
                self.enemy_num -= 1
                if not self.PLAYER_POINT:
                    self.PLAYER_POINT = (x,y)

        while self.item_num > 0:
            x = random.randint(1, self.map_width-1)
            y = random.randint(1, self.map_height-1)
            
                

            if self.tiles[x][y] == TILE.EMPTY:
                self.item_tiles[x][y] = self.dungeon_level# TODO 後でレベルの調整
                self.item_num -= 1
                    



    def walk(self, map_width, map_height):
        dx, dy = 0,0
        direction = 0
        # 方向を選択する
        north = 1.0
        south = 1.0
        east = 1.0
        west = 1.0

        # 辺に対する重み付け
        if self.drunker_dx < map_width * 0.25:
            east += self.weighted_toward_center
        elif self.drunker_dx < map_width * 0.25:
            west += self.weighted_toward_center
        if self.drunker_dy < map_height * 0.25:
            south += self.weighted_toward_center
        elif self.drunker_dy < map_height * 0.25:
            north += self.weighted_toward_center

        # ランダムウォークの前を重くする
        if self._previous_direction == "north":
            north += self.weighted_toward_previous_direction
        if self._previous_direction == "south":
            south += self.weighted_toward_previous_direction
        if self._previous_direction == "east":
            east += self.weighted_toward_previous_direction
        if self._previous_direction == "west":
            west += self.weighted_toward_previous_direction

        # 確率を正規化し、0から1までの範囲を形成する
        total = north+south+east+west
        north /= total
        south /= total
        east /= total
        west /= total

        # 方角を選ぶ
        choice = random.random()
        if 0 <= choice < north:
            dx = 0
            dy = -1
            direction = "north"
        elif north <= choice < (north+south):
            dx = 0
            dy = 1
            direction = "south"
        elif (north+south) <= choice < (north+south+east):
            dx = 1
            dy = 0
            direction = "east"
        else:
            dx = -1
            dy = 0
            direction = "west"

        # 辺の衝突チェック
        if (0 < self.drunker_dx + dx < map_width-1) and (0 < self.drunker_dy + dy < map_height-1):
            self.drunker_dx += dx
            self.drunker_dy += dy
            if self.tiles[self.drunker_dx][self.drunker_dy] == TILE.WALL:
                self.tiles[self.drunker_dx][self.drunker_dy] = TILE.EMPTY
                self._filled += 1
            self._previous_direction = direction




class MG(arcade.Window):
    def __init__(self, width, height, title="bsp"):
        super().__init__(width, height, title)
        
        
        self.rand_walk = DrunkerWalk(map_width=40, map_height=40)
        self.dg_list = self.rand_walk.generate_tile()
        self.actor_list = self.rand_walk.actor_tiles
        self.item_list = self.rand_walk.item_tiles
        # self.graph = self.rand_walk.graph
                
        # print(self.dg_list)

        arcade.set_background_color((200,200,200))

        # graph = SquareGrid(40, 40, self.dg_list)
        # self.path = breadth_first_search(graph, (5,5), (50,50))
        # self.path2 = [(x*10, y*10) for x, y in self.path]



        # cost_pos = []
        # for y in range(40):
        #     for x in range(40):
        #         if type(self.actor_list[x][y]) == int:
        #             cost_pos.append((x,y))
        # cp = [(x, y) for x in range(40) for y in range(40) if type(self.actor_list[x][y]) == int] 
        # print(cost_pos, "cost_pos")
        # print(cp, "cp")

        # start = self.rand_walk.PLAYER_POINT
        # goal = self.rand_walk.room_center_list[-1]


        # graph = GridWithWeights(40, 40, walls=self.dg_list, cost_tile=cp)

        # # search = dijkstra_search(graph, start, goal)
        # search = a_star_search(graph, start, goal)
        # self.path = reconstruct_path(search[0], start=start, goal=goal)
        # self.path2 = [(x*10, y*10) for x, y in self.path]





        # from queue import Queue
        # start = 5,5
        # goal = 15,15
        # frontier = Queue()
        # frontier.put(start)
        # came_from = dict()
        # came_from[start] = None
        # self.path  = []
        

        # while not frontier.empty():
        #     current = frontier.get()
        #     for next in self.rand_walk.neighbors(current):
        #         if next not in came_from:
        #             frontier.put(next)
        #             came_from[next] = current
        #     if current == goal:
        #         break

        # while current != start:
        #     self.path.append(current)
        #     current = came_from[current]

        # print(f"{self.path=}")
                    




    def on_draw(self):
        arcade.start_render()
        for x in range(len(self.dg_list[0])):
            for y in range(len(self.dg_list)):
                if self.dg_list[x][y] == TILE.STAIRS_UP:
                    arcade.draw_rectangle_filled(x*10, y*10, 9, 9, arcade.color.RED)
                if self.dg_list[x][y] == TILE.EMPTY or type(self.dg_list[x][y]) == int:
                    arcade.draw_rectangle_filled(x*10, y*10, 9, 9, arcade.color.BLACK)
                if type(self.item_list[x][y]) == int:
                    arcade.draw_rectangle_filled(x*10, y*10, 9, 9, arcade.color.GREEN)
                # if (x,y) in self.path:
                #     arcade.draw_point(x*10, y*10, arcade.color.RED, 3) 
                if type(self.actor_list[x][y]) == int:
                    arcade.draw_rectangle_filled(x*10, y*10, 9, 9, arcade.color.YELLOW)
                # if self.dg_list[x][y] == TILE.STAIRS_DOWN:
                #     arcade.draw_rectangle_filled(x*10, y*10, 9, 9, arcade.color.BALL_BLUE)
                # if (x, y) == self.bsp.room_center_list[-1]:
                #     arcade.draw_rectangle_filled(x*10, y*10, 9, 9, arcade.color.BALL_BLUE)
        # arcade.draw_line_strip(self.path2, arcade.color.ANDROID_GREEN,3)


    def on_update(self, delta_time):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

def main():
    gam = MG(600, 600)
    arcade.run()

if __name__ == "__main__":
    main()




