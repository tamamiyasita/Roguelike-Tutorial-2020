import arcade
import heapq
from constants import *
from game_map.bsp import BSPTree


max_distance = 2000

def compute_distance_map(cost_map, starts):
    map_height = len(cost_map)
    map_width = len(cost_map[0])
    dist_map = [[max_distance for x in range(map_width)] for y in range(map_height)]

    
    pq = []
    for pos_start in starts:
        heapq.heappush(pq, (0, pos_start))# スタート位置(目標位置になる)はゼロとなる

    while pq:
        dist, pos = heapq.heappop(pq)

        # distが訪問済みならパス
        if dist_map[pos[1]][pos[0]] <= dist:
            continue

        # dist_mapに位置コストdistを代入、これがパスとなる
        dist_map[pos[1]][pos[0]] = dist

        # 近隣のタイルを調べ壁ならスキップ床なら値を比べてpqに入れるか決める
        for d_pos in [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            pos_new = (pos[0] + d_pos[0], pos[1] + d_pos[1])# 周りを調べる
            if pos_new[0] < 0 or pos_new[0] >= map_width:# 調べる範囲がマップサイズに収まってなければスキップさせる
                continue
            if pos_new[1] < 0 or pos_new[1] >= map_height:# 同上
                continue
            dist_new = dist + cost_map[pos_new[1]][pos_new[0]] # 現在地のコストにコストマップの近隣の位置コスト(1か2000)を加える
            if dist_new >= dist_map[pos_new[1]][pos_new[0]]: # その値がdistマップの近隣の位置のコストより高ければスキップ
                continue
            heapq.heappush(pq, (dist_new, pos_new)) # pqに近隣の位置(x, y)とコスト値dist_newを加える

    return dist_map

impassable_cost = 2000
passable_cost = 1

def tile_cost(tile):
    if tile == TILE.WALL:
        return impassable_cost
    else:
        return passable_cost

def cost_map_init(sprites):
    return [[tile_cost(i) for i in row] for row in sprites]



class MG(arcade.Window):
    def __init__(self, width, height, title="bsp"):
        super().__init__(width, height, title)
        
        
        self.tiles = [[TILE.WALL for y in range(40)] for x in range(40)]
        self._bsp = BSPTree(map_height=40, map_width=40)
        self.bsp = self._bsp.generate_tile()

        arcade.set_background_color((200,200,200))
        self.cost_map = cost_map_init(self.bsp)
        self.dist_map = compute_distance_map(self.cost_map,[(self._bsp.PLAYER_POINT)])
        print(self.dist_map)



    def on_draw(self):
        arcade.start_render()
        for x in range(len(self.cost_map)):
            for y in range(len(self.cost_map)):
                if self.cost_map[x][y] >= 2000:
                    arcade.draw_rectangle_filled(x*10, y*10, 9, 9, arcade.color.BABY_POWDER)
                else:
                    num = self.dist_map[x][y]
                    arcade.draw_rectangle_filled(x*10, y*10, 9, 9, (num*9, num*5, num*2))

                
        #         if self.cost_map[x][y] == TILE.EMPTY or type(self.dg_list[x][y]) == int:
        #             arcade.draw_rectangle_filled(x*10, y*10, 9, 9, arcade.color.BLACK)
        #         # if type(self.item_list[x][y]) == int:
        #         #     arcade.draw_rectangle_filled(x*10, y*10, 9, 9, arcade.color.GREEN)
        #         if (x,y) in self.path:
        #             arcade.draw_point(x*10, y*10, arcade.color.RED, 3) 
        #         if type(self.actor_list[x][y]) == int:
        #             arcade.draw_rectangle_filled(x*10, y*10, 9, 9, arcade.color.YELLOW)
        #         if self.dg_list[x][y] == TILE.STAIRS_DOWN:
        #             arcade.draw_rectangle_filled(x*10, y*10, 9, 9, arcade.color.BALL_BLUE)
        #         if (x, y) == self.bsp.room_center_list[-1]:
        #             arcade.draw_rectangle_filled(x*10, y*10, 9, 9, arcade.color.BALL_BLUE)
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


    
