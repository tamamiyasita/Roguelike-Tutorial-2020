import arcade
import random
# from random import randint, choice

# from game_map.door_check import door_check
# from constants import *
# from data import *

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


class BSPTree:
    def __init__(self):
        self.level = []
        self.room = None
        self.MAX_LEAF_SIZE = 5
        self.ROOM_MAX_SIZE = 24
        self.ROOM_MIN_SIZE = 5
        self.room_count = 0

    def generate_level(self, map_width, map_height):
        # 空の2D配列を作成するか、既存の配列をクリアします
        
        self.level = [[1 for y in range(map_height)] for x in range(map_width)]

        self._leafs = []

        root_leaf = Leaf(0, 0, map_width, map_height)
        self._leafs.append(root_leaf)

        split_successfully = True
        
        # 正常に分割できなくなるまで、すべての葉をループします
        while (split_successfully):
            split_successfully = False
            for l in self._leafs:
                if (l.child_1 == None) and (l.child_2 == None):
                    if ((l.width > self.MAX_LEAF_SIZE) or (l.height > self.MAX_LEAF_SIZE) or (random.random() > 0.8)):
                        if (l.split_leaf()):
                            self._leafs.append(l.child_1)
                            self._leafs.append(l.child_2)
                            split_successfully = True
      
        
        root_leaf.create_rooms(self)

        return self.level

    def create_room(self, room):
        # 矩形内の全てのタイルを0に設定する
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.level[x][y] = 0
        # if self.room_count == 0:
        #     px, py = (room.x1+room.x2)//2, (room.y1+room.y2)//2
        #     self.level[px][py] = 5
        # elif self.room_count == 3:
        #     pxx, pyy = room.x1+room.x2//2, room.y1+room.y2//2
        #     self.level[pxx][pyy] = 4
        # self.room_count += 1
        # print(f"{self.room_count} is room {room}")
    
    def create_hall(self, room1, room2):
        # 廊下で2つの部屋をつなぐ
        x1, y1 = room1.center()
        x2, y2 = room2.center()

        # 水平垂直のトンネルをランダムに決定
        if random.randint(0,1) == 1:
            self.create_hor_tunnel(x1, x2, y1)
            self.create_vir_tunnel(y1, y2, x2)

        else:
            self.create_vir_tunnel(y1, y2, x1)
            self.create_hor_tunnel(x1, x2, y2)

    def create_hor_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2)+1):
            self.level[x][y] = 0# ここでTILE_FLOORもしくはarcade.draw

    def create_vir_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2)+1):
            self.level[x][y] = 0# ここでTILE_FLOORもしくはarcade.draw


class Leaf:#BSPツリーアルゴリズムに使用
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.MIN_LEAF_SIZE = 10
        self.child_1 = None
        self.child_2 = None
        self.room = None
        self.hall = None
        self.room_count = 0

    def split_leaf(self):
        # 葉を2つの子に分ける
        if (self.child_1 != None) or (self.child_2 != None):
            return False# この葉はすでに分割されています

        """
        == 分割の方向を決定します ==
        葉の幅が高さより25％以上大きい場合。
		葉を垂直に分割します。
		葉の高さが幅より25以上大きい場合。
		葉を水平に分割します。
		それ以外の場合は、ランダムに方向を選択します。
        """

        split_horizontally = random.choice([True, False])
        if (self.width/self.height >= 1.25):
            split_horizontally = False
        elif (self.height/self.width >= 1.25):
            split_horizontally = True

        if (split_horizontally):
            max = self.height - self.MIN_LEAF_SIZE
        else:
            max = self.width - self.MIN_LEAF_SIZE
        
        if (max <= self.MIN_LEAF_SIZE):
            return False# 葉が小さすぎて分割出来ない
        
        split = random.randint(self.MIN_LEAF_SIZE, max)# 葉を分割する場所を決定する

        if (split_horizontally):
            self.child_1 = Leaf(self.x, self.y, self.width, split)
            self.child_2 = Leaf(self.x, self.y + split, self.width, self.height - split)
        else:
            self.child_1 = Leaf(self.x, self.y, split, self.height)
            self.child_2 = Leaf(self.x + split, self.y, self.width - split, self.height)

        return True

    def create_rooms(self, bsp_tree):
        if (self.child_1) or (self.child_2):
            # ブランチの終わりに到達するまで、子を再帰的に検索します
            if (self.child_1):
                self.child_1.create_rooms(bsp_tree)
            if (self.child_2):
                self.child_2.create_rooms(bsp_tree)
            
            if (self.child_1 and self.child_2):
                bsp_tree.create_hall(self.child_1.get_room(), self.child_2.get_room())

        else:
            # bspツリーの最後のブランチに部屋を作成します
            w = random.randint(bsp_tree.ROOM_MIN_SIZE, min(bsp_tree.ROOM_MAX_SIZE, self.width-1))
            h = random.randint(bsp_tree.ROOM_MIN_SIZE, min(bsp_tree.ROOM_MAX_SIZE, self.height-1))
            x = random.randint(self.x, self.x+(self.width-1)-w)
            y = random.randint(self.y, self.y+(self.height-1)-h)
            self.room = Rect(x, y, w, h)
            bsp_tree.create_room(self.room)

    
    def get_room(self):
        print(self.room_count, "oooooooo")
        self.room_count += 1
        if (self.room):
            return self.room
        
        else:
            if (self.child_1):
                self.room_1 = self.child_1.get_room()

            if (self.child_2):
                self.room_2 = self.child_2.get_room()
            
            if (not self.child_1 and not self.child_2):
                return None

            elif (not self.room_2):
                return self.room_1
            
            elif (not self.room_1):
                return self.room_2
            
            elif (random.random() < 0.5):
                return self.room_1
            else:
                return self.room_2


            

        




# bsp = BSPTree()
# print(bsp.generate_level(25,25))
import pprint

class MG(arcade.Window):
    def __init__(self, width, height, title="bsp"):
        super().__init__(width, height, title)
        self.bsp = BSPTree()
        self.dg_list = self.bsp.generate_level(40,40)
        # pprint.p
        print(self.dg_list)

        arcade.set_background_color((200,200,200))

    def on_draw(self):
        arcade.start_render()
        for x in range(len(self.dg_list[0])):
            for y in range(len(self.dg_list)):
                if self.dg_list[x][y] == 1:
                    arcade.draw_rectangle_filled(x*10, y*10, 9, 9, arcade.color.BLACK)
                if self.dg_list[x][y] == 5:
                    arcade.draw_rectangle_filled(x*10, y*10, 9, 9, arcade.color.RED)
                elif self.dg_list[x][y] == 4:
                    arcade.draw_rectangle_filled(x*10, y*10, 9, 9, arcade.color.GREEN)

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