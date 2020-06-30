from util import get_blocking_entity
from constants import *


class Node():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def spot_is_blocked(x, y, sprite_lists):
    if x < 0 or y < 0 or x >= MAP_WIDTH or y >= MAP_HEIGHT:
        return True

    for sprite_list in sprite_lists:
        if get_blocking_entity(x, y, sprite_list):
            return True
    return False


def astar(sprite_lists, start, end):
    """指定位置の開始と終了点をタプルのリストとして返す"""

    # 開始ノードと終了ノードを作成する
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # openとclosed両方のリストを初期化する
    open_list = []
    closed_list = []

    # 開始ノードを追加する
    open_list.append(start_node)

    loop_count = 0
    # 終わりが見つかるまでループする
    while len(open_list) > 0:
        loop_count += 1
        if loop_count > 50:
            print("BREAK!")
            return None

        # 現在のノードを取得する
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # open_listからpopしclosed_listに追加
        open_list.pop(current_index)
        closed_list.append(current_node)

        # 目標を見つけた
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # 逆のpathを返す

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # 隣接するタイル

            # ノードの位置を取得
            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # 範囲内である事を確認する if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(
            # maze[len(maze) - 1]) - 1) or node_position[1] < 0: continue

            # 歩ける地形か確認する
            if spot_is_blocked(node_position[0], node_position[1], sprite_lists):
                continue

            # 新規ノードを作成して追加する
            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:

            # child is the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # create the f, g, h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) **
                       2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)
