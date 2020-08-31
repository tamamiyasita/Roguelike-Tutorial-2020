import arcade
from util import get_tile_set

# playerテクスチャ生成
player = arcade.load_texture_pair(r"image/rou6.png")
pc_move = arcade.load_texture_pair(r"image/rou6_m.png")
pc_attack = arcade.load_texture_pair(r"image/rou6_a.png")
pc_delay = arcade.load_texture_pair(r"image/rou6_d.png")
pc_delay2 = arcade.load_texture_pair(r"image/rou6_d2.png")

# test_texture
# player = arcade.load_texture_pair(r"t_image/rou6.png")
# pc_move = arcade.load_texture_pair(r"t_image/rou6_m.png")
# pc_attack = arcade.load_texture_pair(r"t_image/rou6_a.png")
# pc_delay = arcade.load_texture_pair(r"t_image/rou6_d.png")
# pc_delay2 = arcade.load_texture_pair(r"t_image/rou6_d2.png")

###enemys###
size = 16  # テクスチャのサイズと位置情報も兼ねる
orcs_tiles = (r"image/demi_human1.png")  # orcタイルイメージ


# crab pairで生成
crab = arcade.load_texture_pair(r"image/crab.png")

# orcテクスチャ生成
orc_left = arcade.load_texture(
    orcs_tiles, x=0, y=12*size, width=size, height=size)
orc_right = arcade.load_texture(
    orcs_tiles, x=0, y=12*size, width=size, height=size, mirrored=True)
orc = [orc_right, orc_left]

# trollクスチャ生成
troll_left = arcade.load_texture(
    orcs_tiles, x=size*7, y=12*size, width=size, height=size)
troll_right = arcade.load_texture(
    orcs_tiles, x=size*7, y=12*size, width=size, height=size, mirrored=True)
troll = [troll_right, troll_left]
#######

# short weaponテクスチャ生成
short_weapon_tiles = (r"image/ShortWep.png")

short_sword_left = arcade.load_texture(
    short_weapon_tiles, x=0, y=0, width=size, height=size)
short_sword_right = arcade.load_texture(
    short_weapon_tiles, x=0, y=0, width=size, height=size, mirrored=True)
short_sword = [short_sword_right, short_sword_left]
######

# mid weaponテクスチャ生成
med_weapon_tiles = (r"image/MedWep.png")
long_sword_left = arcade.load_texture(
    med_weapon_tiles, x=0, y=0, width=size, height=size)
long_sword_right = arcade.load_texture(
    med_weapon_tiles, x=0, y=0, width=size, height=size, mirrored=True)
long_sword = [long_sword_right, long_sword_left]
###items###
# healing_potionテクスチャセット生成
healing_potion_tile_img = (r"image/Potion.png")
healing_potion_tile = get_tile_set(healing_potion_tile_img, tile_size=16)

scroll_tile_img = (r"image/Scroll.png")
scroll_tile = get_tile_set(scroll_tile_img, tile_size=16)


shield_img = (r"image\Shield.png")
shield_tile = get_tile_set(shield_img, tile_size=16)
#######

###effect###
effect_img_1 = (r"image/Effect1.png")  # 83
effect1_tile = get_tile_set(effect_img_1, tile_size=16)
#######

items_point = arcade.load_texture_pair(r"image/items_point.png")
floor_point = arcade.load_texture_pair(r"image/floor_point.png")
# floor_img = (r"t_image/Tile.png")  # test_texture
floor_img = (r"image/Tile.png")
floor_tile = get_tile_set(floor_img, tile_size=32)
floor_len = len(floor_tile)
floors = [floor_tile[v] for v in range(floor_len)]

stairs = floors

wall_point = arcade.load_texture_pair(r"image/wall_point.png")
# walls_1 = (r"image/wall1.png")
# walls_1_tiles = get_tile_set(walls_1, tile_size=16)
# wall_1 = {k: walls_1_tiles[v] for k, v in zip(
#     range(16), [6, 6, 11, 11, 10, 10, 1, 12, 4, 5, 2, 5, 0, 5, 1, 8])}
# walls_2 = (r"image/wall2.png")
# walls_2_tiles = get_tile_set(walls_2, tile_size=16)
# wall_2 = {k: walls_2_tiles[v] for k, v in zip(
#     range(16), [6, 6, 11, 11, 10, 10, 1, 12, 4, 5, 2, 5, 0, 5, 1, 8])}
walls_3 = (r"image/wall3.png")
# walls_3 = (r"t_image/wall3.png")  # test_texture
walls_3_tiles = get_tile_set(walls_3, tile_size=16)

wall_3 = [walls_3_tiles[w]
          for w in [6, 6, 11, 11, 10, 10, 1, 12, 4, 5, 2, 5, 0, 5, 1, 8]]

door_img = (r"image/Door0.png")
door_tile = get_tile_set(door_img, tile_size=32)
door_len = len(door_tile)
doors = [door_tile[v] for v in range(door_len)]


# actorに渡す画像はリスト型にすること
IMAGE_ID = {"player": player,
            "pc_move": pc_move,
            "pc_attack": pc_attack,
            "pc_delay": pc_delay,
            "pc_delay2": pc_delay2,

            "crab": crab,

            "orc": orc,
            "troll": troll,

            "short_sword": short_sword,
            "long_sword": long_sword,
            "small_shield": [shield_tile[0]],
            "wood_buckler": [shield_tile[5]],

            "healing_potion": healing_potion_tile,
            "confusion_scroll": [scroll_tile[15]],
            "lightning_scroll": [scroll_tile[2]],
            "fireball_scroll": [scroll_tile[6]],

            "lightning_effect": [effect1_tile[87]],
            "confusion_effect": [effect1_tile[140]],
            "fireball_effect": [effect1_tile[134]],

            "floor_point": floor_point,
            "items_point": items_point,
            "floor": floors,
            "wall_point": wall_point,
            # "wall_1": wall_1,
            # "wall_2": wall_2,
            "wall_3": wall_3,
            "stairs": stairs,
            "door": doors

            }


class Testimg(arcade.Window):
    def __init__(self):
        size = 16
        super().__init__(100, 100)
        img = arcade.load_texture(
            floors, x=0, y=size, width=size, height=size)
        arcade.start_render()
        arcade.draw_texture_rectangle(50, 50, 16, 16, img)


def main():
    test = Testimg()

    arcade.run()


if __name__ == "__main__":
    main()
