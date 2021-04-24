import arcade
import random
import math
from functools import wraps
import time

from constants import *

def stop_watch(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start
        print(f"{func.__name__}は{elapsed_time}秒かかりました")
        return result
    return wrapper

class CellularAutomata:
    def __init__(self):
        self.level = []

        self.iterations = 5550
        self.neighbors = 4 # cellに隣接する壁の数
        self.wall_probability = 0.455 #セルが壁になる初期確率。.35から.55の間であることが推奨されます

        self.ROOM_MIN_SIZE = 4 #cellの総数のサイズ
        self.ROOM_MAX_SIZE = 15 # ’’

        self.smooth_edges = True
        self.smoothing = 1

    @stop_watch
    def generate_level(self, map_width, map_height):
        # 空の2D配列を作成するか、既存の配列をクリアします
        self.caves = []

        self.level = [[1 for y in range(map_height)] for x in range(map_width)]

        self.random_fillmap(map_width, map_height)

        self.create_caves(map_width, map_height)

        self.get_caves(map_width, map_height)

        self.connot_caves(map_width, map_height)

        self.clean_up_map(map_width, map_height)

        return self.level

    def random_fillmap(self, map_width, map_height):
        for y in range(1, map_height-1):
            for x in range(1, map_width-1):
                if random.random() >= self.wall_probability:
                    self.level[x][y] = 0

    def create_caves(self, map_width, map_height):
        for i in range(0, self.iterations):
            tile_x = random.randint(1, map_width-2)
            tile_y = random.randint(1, map_height-2)
            
            # セルの隣接する壁> self.neighborsの場合は、1に設定します。
            if self.get_adjacent_walls(tile_x, tile_y) > self.neighbors:
                self.level[tile_x][tile_y] = 1

            elif self.get_adjacent_walls(tile_x, tile_y) < self.neighbors:
                self.level[tile_x][tile_y] = 0

        self.clean_up_map(map_width, map_height)


    def clean_up_map(self, map_width, map_height):
        if (self.smooth_edges):
            for i in range(0, 5):
                # 各セルを個別に見て、滑らかさを確認します
                for x in range(1, map_width-1):
                    for y in range(1, map_height-1):
                        if (self.level[x][y] == 1) and (self.get_adjacent_walls_simple(x, y) <= self.smoothing):
                            self.level[x][y] = 0


    def create_tunnel(self, point_1, point_2, current_cave, map_width, map_height):
        # randomwalkをpoint_1からpoint_2に実行する
        drunker_dx = point_2[0]
        drunker_dy = point_2[1]

        while (drunker_dx, drunker_dy) not in current_cave:
            north = 1.0
            south = 1.0
            east = 1.0
            west = 1.0

            weight = 1

            # ランダムウォークをエッジに対して重み付けします
            if drunker_dx < point_1[0]:
                east += weight
            elif drunker_dx > point_1[0]:
                west += weight
            if drunker_dy < point_1[1]:
                south += weight
            elif drunker_dy > point_1[1]:
                north += weight

            # 確率を正規化して、0から1の範囲を形成します
            total = north+south+east+west
            north /= total
            south /= total
            east /= total
            west /= total

            # choose the direction
            choice = random.random()
            if 0 <= choice < north:
                dx = 0
                dy = -1

            elif north <= choice < (north+south):
                dx = 0
                dy = 1

            elif (north+south) <= choice < (north+south+east):
                dx = 1
                dy = 0

            else:
                dx = -1
                dy = 0

            # =walk=
            # edgesの衝突をチェックする
            if (0 < drunker_dx+dx < map_width-1) and (0 < drunker_dy+dy < map_height-1):
                drunker_dx += dx
                drunker_dy += dy
                if self.level[drunker_dx][drunker_dy] == 1:
                    self.level[drunker_dx][drunker_dy] = 0

    def get_adjacent_walls_simple(self, x, y):
        wall_counter = 0
        if (self.level[x][y-1] == 1):
            wall_counter += 1
        if (self.level[x][y+1] == 1):
            wall_counter += 1
        if (self.level[x-1][y] == 1):
            wall_counter += 1
        if (self.level[x+1][y] == 1):
            wall_counter += 1

        return wall_counter

    # 8方向の壁をチェックする
    def get_adjacent_walls(self, tile_x, tile_y):
        # pass
        wall_counter = 0
        for x in range(tile_x-1, tile_x+2):
            for y in range(tile_y-1, tile_y+2):
                if (self.level[x][y] ==1):
                    if (x != tile_x) or (y != tile_y):
                        wall_counter += 1
        return wall_counter

    def get_caves(self, map_width, map_height):
        for x in range(0, map_width):
            for y in range(0, map_height):
                if self.level[x][y] == 0:
                    self.flood_fill(x, y)

            for set in self.caves:
                for tile in set:
                    self.level[tile[0]][tile[1]] = 0

    def flood_fill(self, x, y):
        #レベルの独立した領域をフラッドで埋め、最小サイズよりも小さい領域は破棄し
		#最小限のサイズよりも小さいリージョンを捨てて, 残りの領域のリファレンスを作成します。
        cave = set()
        tile = (x, y)
        to_be_filled = set([tile])
        while to_be_filled:
            tile = to_be_filled.pop()

            if tile not in cave:
                cave.add(tile)

                self.level[tile[0]][tile[1]] = 1

                # 隣接するセルをチェックする
                x = tile[0]
                y = tile[1]
                north = (x, y-1)
                south = (x, y+1)
                east = (x+1, y)
                west = (x-1, y)

                for dist in [north, south, east, west]:
                    if self.level[dist[0]][dist[1]] == 0:
                        if dist not in to_be_filled and dist not in cave:
                            to_be_filled.add(dist)
        if len(cave) >= self.ROOM_MIN_SIZE:
            self.caves.append(cave)

    def connot_caves(self, map_width, map_height):
        # 現在のcaveに最も近いcaveを探す
        for cur_cave in self.caves:
            for point_1 in cur_cave:# cave1から要素を取得します
                break
            else:
                return None
            point_2 = None
            distance = None
            for next_cave in self.caves:
                if next_cave != cur_cave and not self.check_connectivity(cur_cave, next_cave):
                    # nextCaveからランダムなポイントを選択します
                    for next_point in next_cave:# cave1から要素を取得します
                        break
                    # ポイント1と新旧のポイント2の距離を比較します
                    new_distance = self.distance_formula(point_1, next_point)
                    if distance == None or (new_distance < distance):
                        point_2 = next_point
                        distance = new_distance
            
            if point_2:# すべてのトンネルが接続されている場合、point2 == None
                print(point_2, "point_2")
                self.create_tunnel(point_1, point_2, cur_cave, map_width, map_height)

    def distance_formula(self, point_1, point_2):
        d = math.sqrt((point_2[0]-point_1[0])**2 + (point_2[1]-point_1[1])**2)
        return d

    def check_connectivity(self, cave_1, cave_2):
        # 洞窟1を浸水させた後、洞窟2のある地点をチェックして浸水させる
        connected_region = set()
        for start in cave_1:
            break# cave1から要素を取得します
        else:
            return None

        to_be_filled = set([start])
        while to_be_filled:
            tile = to_be_filled.pop()

            if tile not in connected_region:
                connected_region.add(tile)
                # 隣接するセルを確認する
                x = tile[0]
                y = tile[1]
                north = (x, y-1)
                south = (x, y+1)
                east = (x+1, y)
                west = (x-1, y)

                for dist in [north, south, east, west]:
                    if self.level[dist[0]][dist[1]] == 0:
                        if dist not in to_be_filled and dist not in connected_region:
                            to_be_filled.add(dist)
        for end in cave_2:#cave2から要素を取得します
            break

        if end in connected_region:
            return True
        else:
            return False

# cell = CellularAutomata().generate_level(map_height=40, map_width=40)


class MG(arcade.Window):
    def __init__(self, width, height, title="cell"):
        super().__init__(width, height, title)
        
        
        self._cell = CellularAutomata()
        self.cell = self._cell.generate_level(map_height=40, map_width=40)
        self.tiles = [[TILE.WALL for y in range(40)] for x in range(40)]


        arcade.set_background_color((200,200,200))




    def on_draw(self):
        arcade.start_render()
        for x in range(len(self.tiles)):
            for y in range(len(self.tiles)):
                if self.cell[x][y] == 1:
                    arcade.draw_rectangle_filled(x*10, y*10, 9, 9, arcade.color.BABY_POWDER)

                
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


            
