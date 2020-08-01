import arcade
from util import get_tile_set

# playerテクスチャ生成
player = arcade.load_texture_pair(r"image/rou6.png")
pc_move = arcade.load_texture_pair(r"image/rou6_m.png")
pc_attack = arcade.load_texture_pair(r"image/rou6_a.png")
pc_delay = arcade.load_texture_pair(r"image/rou6_d.png")
pc_delay2 = arcade.load_texture_pair(r"image/rou6_d2.png")

###enemys###
size = 16  # テクスチャのサイズと位置情報も兼ねる
orcs_tiles = (r"image/demi_human1.png")  # orcタイルイメージ


# crab pairで生成
crab = arcade.load_texture_pair(r"image/crab.png")

# orcテクスチャ生成
orc_left = arcade.load_texture(
    orcs_tiles, x=0, y=size, width=size, height=size)
orc_right = arcade.load_texture(
    orcs_tiles, x=0, y=size, width=size, height=size, mirrored=True)
orc = [orc_right, orc_left]

# trollクスチャ生成
troll_left = arcade.load_texture(
    orcs_tiles, x=size*7, y=size, width=size, height=size)
troll_right = arcade.load_texture(
    orcs_tiles, x=size*7, y=size, width=size, height=size, mirrored=True)
troll = [troll_right, troll_left]
#######

# short wepponテクスチャ生成
short_weppon_tiles =(r"image/ShortWep.png")

short_sword_left = arcade.load_texture(short_weppon_tiles, x=0, y=0, width=size, height=size)
short_sword_right = arcade.load_texture(short_weppon_tiles, x=0, y=0, width=size, height=size, mirrored=True)
short_sword = [short_sword_right, short_sword_left]
######

# mid wepponテクスチャ生成
med_weppon_tiles =(r"image/MedWep.png")
long_sword_left = arcade.load_texture(med_weppon_tiles, x=0, y=0, width=size, height=size)
long_sword_right = arcade.load_texture(med_weppon_tiles, x=0, y=0, width=size, height=size, mirrored=True)
long_sword = [long_sword_right, long_sword_left]
###items###
# healing_potionテクスチャセット生成
healing_potion_tile_img = (r"image/HealingPotion.png")
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

floor_img = (r"image/Tile.png")
floor_tile = get_tile_set(floor_img, tile_size=32)
floor_len = len(floor_tile)
floors = [floor_tile[v] for v in range(floor_len)]

stairs = floors

walls_1 = (r"image/wall1.png")
walls_1_tiles = get_tile_set(walls_1, tile_size=16)
wall_1 = {k: walls_1_tiles[v] for k, v in zip(
    range(16), [6, 6, 11, 11, 10, 10, 1, 12, 4, 5, 2, 5, 0, 5, 1, 8])}
walls_2 = (r"image/wall2.png")
walls_2_tiles = get_tile_set(walls_2, tile_size=16)
wall_2 = {k: walls_2_tiles[v] for k, v in zip(
    range(16), [6, 6, 11, 11, 10, 10, 1, 12, 4, 5, 2, 5, 0, 5, 1, 8])}
walls_3 = (r"image/wall3.png")
walls_3_tiles = get_tile_set(walls_3, tile_size=16)
# wall_C = {k: walls_3_tiles[v] for k, v in zip(
# range(16), [6, 6, 11, 11, 10, 10, 1, 12, 4, 5, 2, 5, 0, 5, 1, 8])}
wall_3 = [walls_3_tiles[w]
          for w in [6, 6, 11, 11, 10, 10, 1, 12, 4, 5, 2, 5, 0, 5, 1, 8]]

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
            "small_shield":[shield_tile[0]],
            "wood_buckler":[shield_tile[5]],

            "healing_potion": healing_potion_tile,
            "confusion_scroll": [scroll_tile[15]],
            "lightning_scroll": [scroll_tile[2]],
            "fireball_scroll": [scroll_tile[6]],

            "lightning_effect": [effect1_tile[87]],
            "confusion_effect": [effect1_tile[140]],
            "fireball_effect": [effect1_tile[134]],

            "floor": floors,
            "wall_1": wall_1,
            "wall_2": wall_2,
            "wall_3": wall_3,
            "stairs": stairs

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
