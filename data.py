import arcade
from util import get_tile_set

# playerテクスチャ生成
player = arcade.load_texture_pair(r"image/rou6.png")
pc_move = arcade.load_texture_pair(r"image/rou6_m.png")
pc_attack = arcade.load_texture_pair(r"image/rou6_a.png")
pc_delay = arcade.load_texture_pair(r"image/rou6_d.png")
pc_delay2 = arcade.load_texture_pair(r"image/rou6_d2.png")
pc_delay3 = arcade.load_texture_pair(r"image/rou6t.png")

# test_texture
# player = arcade.load_texture_pair(r"t_image/rou6.png")
# pc_move = arcade.load_texture_pair(r"t_image/rou6_m.png")
# pc_attack = arcade.load_texture_pair(r"t_image/rou6_a.png")
# pc_delay = arcade.load_texture_pair(r"t_image/rou6_d.png")
# pc_delay2 = arcade.load_texture_pair(r"t_image/rou6_d2.png")

###enemys###
# crab pairで生成
crab_0 = arcade.load_texture_pair(r"image/crab0.png")
crab_1 = arcade.load_texture_pair(r"image/crab1.png")
crab = [*crab_0, *crab_1]

size = 16  # テクスチャのサイズと位置情報も兼ねる
orcs_tiles_0 = (r"image\Characters\Player0.png")  # orcタイルイメージ
orcs_tiles_1 = (r"image\Characters\Player1.png")  # orcタイルイメージ

humanoid_tiles_0 =(r"image\Characters\Humanoid0.png")
humanoid_tiles_1 =(r"image\Characters\Humanoid1.png")

# orcテクスチャ生成
orc_right_0 = arcade.load_texture(
    orcs_tiles_0, x=0, y=12*size, width=size, height=size, mirrored=True)
orc_left_0 = arcade.load_texture(
    orcs_tiles_0, x=0, y=12*size, width=size, height=size)
orc_right_1 = arcade.load_texture(
    orcs_tiles_1, x=0, y=12*size, width=size, height=size, mirrored=True)
orc_left_1 = arcade.load_texture(
    orcs_tiles_1, x=0, y=12*size, width=size, height=size)
orc = [orc_right_0, orc_left_0, orc_right_1, orc_left_1]

# trollテクスチャ生成
troll_right_0 = arcade.load_texture(
    orcs_tiles_0, x=size*7, y=12*size, width=size, height=size, mirrored=True)
troll_left_0 = arcade.load_texture(
    orcs_tiles_0, x=size*7, y=12*size, width=size, height=size)
troll_right_1 = arcade.load_texture(
    orcs_tiles_1, x=size*7, y=12*size, width=size, height=size, mirrored=True)
troll_left_1 = arcade.load_texture(
    orcs_tiles_1, x=size*7, y=12*size, width=size, height=size)
troll = [troll_right_0, troll_left_0, troll_right_1, troll_left_1]
#######

# npcテクスチャ生成
villager_right_0 = arcade.load_texture(
    humanoid_tiles_0, x=size*1, y=size*3, width=size, height=size, mirrored=True)
villager_left_0 = arcade.load_texture(
    humanoid_tiles_0, x=size*1, y=size*3, width=size, height=size)
villager_right_1 = arcade.load_texture(
    humanoid_tiles_1, x=size*1, y=size*3, width=size, height=size, mirrored=True)
villager_left_1 = arcade.load_texture(
    humanoid_tiles_1, x=size*1, y=size*3, width=size, height=size)
villager = [villager_right_0,villager_left_0, villager_right_1, villager_left_1]

citizen_right_0 = arcade.load_texture(
    humanoid_tiles_0, x=size*3, y=size*4, width=size, height=size, mirrored=True)
citizen_left_0 = arcade.load_texture(
    humanoid_tiles_0, x=size*3, y=size*4, width=size, height=size)
citizen_right_1 = arcade.load_texture(
    humanoid_tiles_1, x=size*3, y=size*4, width=size, height=size, mirrored=True)
citizen_left_1 = arcade.load_texture(
    humanoid_tiles_1, x=size*3, y=size*4, width=size, height=size)
citizen = [citizen_right_0,citizen_left_0, citizen_right_1, citizen_left_1]



g1 = arcade.load_texture_pair(r"image\gb1.png")
g2 = arcade.load_texture_pair(r"image\gb2.png")
gb = [*g1,*g2]


ssr1 = arcade.load_texture_pair(r"image\ssr1.png")
ssr2 = arcade.load_texture_pair(r"image\ssr2.png")
ssr = [*ssr1, *ssr2]

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

cirsium = arcade.load_texture_pair(r"image\Cirsium.png")
leaf_blade = arcade.load_texture_pair(r"image\LeafBlade.png")
leaf_blade_icon = arcade.load_texture(r"image\leaf_blade_icon.png")
ebony = arcade.load_texture_pair(r"image\ebony.png")
branch_baton = arcade.load_texture_pair(r"image\BranchBaton.png")
branch_baton_icon = arcade.load_texture(r"image\branch_baton_icon.png")
healing = arcade.load_texture(r"image\healing.png")
Paeonia = arcade.load_texture(r"image\paeonia.png")
poison = arcade.load_texture(r"image\poison.png")

cool_down = arcade.load_texture(r"image\cool_down.png")
###items###
# healing_potionテクスチャセット生成
healing_potion_tile_img = (r"image/Potion.png")
healing_potion_tile = get_tile_set(healing_potion_tile_img, tile_size=16)

scroll_tile_img = (r"image/Scroll.png")
scroll_tile = get_tile_set(scroll_tile_img, tile_size=16)


shield_img = (r"image\Shield.png")
shield_tile = get_tile_set(shield_img, tile_size=16)


ammo_img = (r"image\Items\Ammo.png")
ammo_tile = get_tile_set(ammo_img, tile_size=16)
#######

###effect###
effect_img_1 = (r"image/Effect1.png")  # 83
effect1_tile = get_tile_set(effect_img_1, tile_size=16)

healing_potion_effect = arcade.load_texture("image\green_ball.png")
#######

items_point = arcade.load_texture_pair(r"image/items_point.png")
floor_point = arcade.load_texture(r"image/floor_point.png")
wall_point = arcade.load_texture_pair(r"image/wall_point.png")
stairs_down_point = arcade.load_texture_pair(r"image/stairs_down_point.png")

# floor_img = (r"t_image/Tile.png")  # test_texture
floor_img = (r"image/Tile.png")
floor_tile = get_tile_set(floor_img, tile_size=16)
floor_len = len(floor_tile)
floors = [floor_tile[v] for v in range(floor_len)]
up_stairs = arcade.load_texture(r"image\up_stairs.png")
down_stairs = arcade.load_texture(r"image\down_stairs.png")
stone_floor = arcade.load_texture(r"image\stone_tile.png")

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

# door_img = (r"image/Door0.png")
# door_tile = get_tile_set(door_img, tile_size=16)
# door_len = len(door_tile)
door1 = arcade.load_texture(r"image\wood_door1.png")
door2 = arcade.load_texture(r"image\wood_door2.png")
doors_h = [door1,door2]
door3 = arcade.load_texture(r"image\door3.png")
door4 = arcade.load_texture(r"image\door4.png")
doors_w = [door3,door4]


# actorに渡す画像はリスト型にすること
IMAGE_ID = {"Rou": player,
            "pc_move": pc_move,
            "pc_attack": pc_attack,
            "pc_delay": pc_delay,
            "pc_delay2": pc_delay2,

            "crab": crab,

            "orc": orc,
            "troll": troll,
            "villager":ssr,
            # "citizen":citizen,
            "citizen":gb,

            "short_sword": short_sword,
            "long_sword": long_sword,
            "small_shield": [shield_tile[0]],
            "wood_buckler": [shield_tile[5]],
            "boomerang": [ammo_tile[22]],
            "cirsium": cirsium,
            "ebony":ebony,
            "leaf_blade": leaf_blade,
            "leaf_blade_icon": leaf_blade_icon,
            "branch_baton": branch_baton,
            "branch_baton_icon": branch_baton_icon,
            "paeonia":Paeonia,
            "healing":[healing],
            "poison":[poison],
            "healing_icon":healing,
            "cool_down":cool_down,
            "confusion_scroll": [scroll_tile[15]],
            "lightning_scroll": [scroll_tile[2]],
            "fireball_scroll": [scroll_tile[6]],

            "lightning_effect": [effect1_tile[87]],
            "confusion_effect": [effect1_tile[140]],
            "fireball_effect": [effect1_tile[134]],
            "healing_potion_effect":[healing_potion_effect],

            "floor_point": [floor_point],
            "items_point": items_point,
            "wall_point": wall_point,
            "stairs_down_point": stairs_down_point,

            "floor": floors,
            "stone_floor":[stone_floor],
            # "wall_1": wall_1,
            # "wall_2": wall_2,
            "wall_3": wall_3,
            "up_stairs": [up_stairs],
            "down_stairs": [down_stairs],
            "door_h": doors_h,
            "door_w": doors_h

            }
