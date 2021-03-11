import arcade
import heapq
from constants import *
from game_map.bsp import BSPTree

class DijkstraMap:
    def __init__(self, game_map, target):
        """game_mapとstartで初期化する、その後は必要に応じて
        self.compute_distance_mapで目標位置を更新する"""

        self.game_map = game_map
        self.target = [(target.x, target.y) for target in target]

        self.cost_map = None
        self.dist_map = None


        self.cost_map_init(self.game_map)
        self.map_height = len(self.cost_map)
        self.map_width = len(self.cost_map[0])

        self.compute_distance_map()

        self.neighbors = [(-1, -1), (0, -1), (1, -1), (-1, 0),
                          (1, 0), (-1, 1), (0, 1), (1, 1)]

    def tile_cost(self, tile):
        if tile == TILE.WALL:
            return 2000
        else:
            return 1

    def cost_map_init(self, game_map):
        self.cost_map = [[self.tile_cost(i) for i in row] for row in game_map]

    def map_range_inner(self, x, y):
        # マップサイズの範囲内かどうか判定する
        return 1 <= x < self.map_width and 1 <= y < self.map_height

    def get_low_number(self, x, y):
        point = 2000
        dist = None
        current_num = self.dist_map[x][y]
        for dx, dy in self.neighbors:
            tx, ty = x+dx, y+dy 
            if self.map_range_inner(tx, ty) and self.dist_map[tx][ty] < current_num:
                if point > self.dist_map[tx][ty]:
                    point = self.dist_map[tx][ty]
                    dist = tx,ty
        return dist
                    



    def compute_distance_map(self, targets=None, blocks=None):
        # if args == None:# 位置更新に使う
        if targets:# actorオブジェクトならx,yをタプルで入れる
            self.target = [(target.x, target.y) for target in targets]



        dist_map = [[2000 for x in range(self.map_width)] for y in range(self.map_height)]

        if blocks:
            self.cost_map_init(self.game_map)
            for block in blocks:
                self.cost_map[block.x][block.y] = 8

        
        pq = []
        for pos_start in self.target:
            heapq.heappush(pq, (0, pos_start))# スタート位置(目標位置になる)はゼロとなる

        while pq:
            dist, pos = heapq.heappop(pq)

            # distが訪問済みならパス
            if dist_map[pos[0]][pos[1]] <= dist:
                continue

            # dist_mapに位置コストdistを代入、これがパスとなる
            dist_map[pos[0]][pos[1]] = dist

            # 近隣のタイルを調べ壁ならスキップ床なら値を比べてpqに入れるか決める
            for d_pos in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                pos_new = (pos[0] + d_pos[0], pos[1] + d_pos[1])# 周りを調べる
                if not self.map_range_inner(x=pos_new[0], y=pos_new[1]):# 調べる範囲がマップサイズに収まってなければスキップさせる
                    continue

                dist_new = dist + self.cost_map[pos_new[0]][pos_new[1]] # 現在地のコストにコストマップの近隣の位置コスト(1か2000)を加える
                if dist_new >= dist_map[pos_new[0]][pos_new[1]]: # その値がdistマップの近隣の位置のコストより高ければスキップ
                    continue
                heapq.heappush(pq, (dist_new, pos_new)) # pqに近隣の位置(x, y)とコスト値dist_newを加える


        self.dist_map = dist_map


class MG(arcade.Window):
    def __init__(self, width, height, title="bsp"):
        super().__init__(width, height, title)
        
        
        self.tiles = [[TILE.WALL for y in range(40)] for x in range(40)]
        self._bsp = BSPTree(map_height=40, map_width=40)
        self.bsp = self._bsp.generate_tile()

        arcade.set_background_color((200,200,200))
        self.target_player_map = DijkstraMap(self.bsp, self._bsp.PLAYER_POINT)
        self.target_player_map.compute_distance_map((10,10),(20,35))


        g = self._bsp.PLAYER_POINT[0]+3, self._bsp.PLAYER_POINT[1]+3
        get_1 = self.target_player_map.get_low_number(*g)
        f = self._bsp.PLAYER_POINT[0]+2, self._bsp.PLAYER_POINT[1]+2
        get_2 = self.target_player_map.get_low_number(*f)
        p = self._bsp.PLAYER_POINT[0]+1, self._bsp.PLAYER_POINT[1]+1
        get_3 = self.target_player_map.get_low_number(*p)
        print(self._bsp.PLAYER_POINT, get_1, get_2, get_3)



    def on_draw(self):
        arcade.start_render()
        for x in range(len(self.tiles)):
            for y in range(len(self.tiles)):
                if self.target_player_map.dist_map[x][y] >= 2000:
                    arcade.draw_rectangle_filled(x*10, y*10, 9, 9, arcade.color.BABY_POWDER)
                else:
                    num = self.target_player_map.dist_map[x][y]
                    arcade.draw_rectangle_filled(x*10, y*10, 9, 9, (num*9, num*5, num*2))
                

                
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


    
