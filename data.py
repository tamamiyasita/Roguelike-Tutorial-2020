import arcade
import glob

from util import get_tile_set


# MONSTER
water_vole_0 = arcade.load_texture_pair(r"image/character/monster/water_vole0.png")
water_vole_1 = arcade.load_texture_pair(r"image/character/monster/water_vole1.png")
water_vole =[*water_vole_0, *water_vole_1]

cabbage_snail_0  = arcade.load_texture_pair(r"image/character/monster/cabbage_snail0.png")
cabbage_snail_1 = arcade.load_texture_pair(r"image/character/monster/cabbage_snail1.png")
cabbage_snail =[*cabbage_snail_0, *cabbage_snail_1]

dog_1 = arcade.load_texture_pair(r"image\character\monster\dog1.png")
dog_2 = arcade.load_texture_pair(r"image\character\monster\dog2.png")
dog = [*dog_1, *dog_2]

goblin_shaman_0 = arcade.load_texture_pair(r"image\character\monster\goblin_shaman_0.png")
goblin_shaman_1 = arcade.load_texture_pair(r"image\character\monster\goblin_shaman_1.png")
goblin_shaman = [*goblin_shaman_0, *goblin_shaman_1]

ssr1 = arcade.load_texture_pair(r"image\character\monster\ssr1.png")
ssr2 = arcade.load_texture_pair(r"image\character\monster\ssr2.png")
ssr = [*ssr1, *ssr2]


# FLOWER #
silver_grass = arcade.load_texture_pair(r"image\items\flower\silver_grass.png")
bambooflower = arcade.load_texture(r"image\items\flower\bambooflower.png")
Paeonia = arcade.load_texture(r"image\items\flower\paeonia.png")
sunflower = arcade.load_texture(r"image\items\flower\sunflower.png")
pineapple = arcade.load_texture(r"image/items/flower/pineapple.png")
aconite = arcade.load_texture(r"image/items/flower/aconite.png")
bananaflower = arcade.load_texture(r"image/items/flower/bananaflower.png")
cabbageflower = arcade.load_texture(r"image\items\flower\cabbage_flower.png")
# FLOWER ICON
silver_grass_icon = arcade.load_texture(r"image\icon\silver_grass_icon.png")
bambooflower_icon = arcade.load_texture(r"image\icon\bambooflower_icon.png")
Paeonia_icon = arcade.load_texture(r"image\icon\paeonia_icon.png")
sunflower_icon = arcade.load_texture(r"image\icon\sunflower_icon.png")
pineapple_icon = arcade.load_texture(r"image/icon/pineapple_icon.png")
bananaflower_icon = arcade.load_texture(r"image/icon/bananaflower_icon.png")


# SKILL
grass_cutter = arcade.load_texture_pair(r"image\skill\grass_cutter.png")
grass_cutter_icon = arcade.load_texture(r"image\icon\grass_cutter_icon.png")

bamboo_blade = arcade.load_texture_pair(r"image\skill\bamboo_blade.png")
bamboo_blade_icon = arcade.load_texture(r"image\icon\bamboo_blade_icon.png")

healing = arcade.load_texture_pair(r"image\skill\healing.png")
healing_icon = arcade.load_texture(r"image\icon\healing_icon.png")
healing_potion_effect = arcade.load_texture("image\skill\green_ball.png")

seed_shot = arcade.load_texture_pair(r"image/skill/seed_shot.png")
seed_shot_b = arcade.load_texture(r"image/skill/seed_shot_b.png")
seed_shot_icon = arcade.load_texture(r"image/icon/seed_shot_icon.png")

banana_slip = arcade.load_texture_pair(r"image/skill/banana_slip.png")
banana_slip_icon = arcade.load_texture(r"image/icon/banana_slip_icon.png")
banana_fall = [arcade.load_texture(img) for img in glob.glob(r"image\effect\banana_fall\*")]

poison_dart = arcade.load_texture_pair(r"image/skill/poison_dart.png")
poison_dart_icon = arcade.load_texture(r"image/icon/poison_dart_icon.png")
poison_start = [arcade.load_texture(img) for img in glob.glob(r"image\effect\poison_start\*")]

pineapple_grenade = arcade.load_texture_pair(r"image/skill/p_grenade.png")
pineapple_grenade_icon = arcade.load_texture(r"image/icon/pineapple_grenade_icon.png")
pineapple_explosion = [arcade.load_texture(img) for img in glob.glob(r"image\effect\pineapple_explosion\*")]

attack_icon = arcade.load_texture(r"image/icon/poison.png")

fire_arrow = arcade.load_texture_pair(r"image/skill/fire_arrow.png")
fire_arrow_icon = arcade.load_texture(r"image/skill/fire_arrow.png")

# STATES_EFFECT_ICON
poison = arcade.load_texture(r"image\icon\poison.png")
stun = arcade.load_texture(r"image\icon\stun.png")




# MAP_OBJECT
up_stairs = arcade.load_texture(r"image\map_obj\up_stairs.png")
down_stairs = arcade.load_texture(r"image\map_obj\down_stairs.png")
block_floor = arcade.load_texture(r"image\map_obj\block_floor.png")
color_tile_1 = arcade.load_texture(r"image\map_obj\color_tile_1.png")


basic_walls = (r"image/map_obj/tiles/basic_walls.png")
basic_walls_tiles = get_tile_set(basic_walls, tile_size=32)
basic_wall = [basic_walls_tiles[w] for w in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]]

color_tile_walls = (r"image/map_obj/tiles/color_tile_walls.png")
color_tile_walls = get_tile_set(color_tile_walls, tile_size=32)
color_tile_walls = [color_tile_walls[w] for w in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]]


door1 = arcade.load_texture(r"image\map_obj\wood_door1.png")
door2 = arcade.load_texture(r"image\map_obj\wood_door2.png")
door = [door1,door2]




# UI
items_point = arcade.load_texture_pair(r"image/ui/items_point.png")
floor_point = arcade.load_texture(r"image/ui/floor_point.png")
wall_point = arcade.load_texture_pair(r"image/ui/wall_point.png")
stairs_down_point = arcade.load_texture_pair(r"image/ui/stairs_down_point.png")
cool_down = arcade.load_texture(r"image\ui\cool_down.png")
pop = arcade.load_texture(r"image\ui\pop.png")
black_board = arcade.load_texture(r"image\icon\black_board.png")

# inventory_ui
inventory_main = arcade.load_texture(r"image\ui\inventory\main_panel.png")
inventory_cursor = arcade.load_texture(r"image\ui\inventory\cursor.png")
inventory_sub = arcade.load_texture(r"image\ui\inventory\sub_panel.png")

# normal_ui
active_panel = arcade.load_texture(r"image\ui\normal\active_panel.png")
passive_panel = arcade.load_texture(r"image\ui\normal\passive_panel.png")
massage_panel = arcade.load_texture(r"image\ui\normal\massage_panel.png")
map_panel = arcade.load_texture(r"image\ui\normal\map_panel.png")
side_panel = arcade.load_texture(r"image\ui\normal\side_panel.png")

# character_screen_ui
chara_main = arcade.load_texture(r"image\ui\character_screen\chara_main.png")
chara_sheet = arcade.load_texture(r"image\ui\character_screen\chara_sheet.png")
chara_cursor = arcade.load_texture(r"image\ui\character_screen\chara_cursor.png")
first_point = arcade.load_texture(r"image\ui\character_screen\first_point.png")



IMAGE_ID = {
            # MONSTER
            "water_vole": water_vole,
            "cabbage_snail": cabbage_snail,
            "dog":dog,
            "goblin_shaman":goblin_shaman,



            # FLOWER & SKILL & ICON & SKILL_EFFECT
            "silver_grass": silver_grass,
            "silver_grass_icon": silver_grass_icon,
            "grass_cutter": grass_cutter,
            "grass_cutter_icon": grass_cutter_icon,

            "bambooflower":bambooflower,
            "bambooflower_icon":bambooflower_icon,
            "bamboo_blade_icon":bamboo_blade_icon,
            "bamboo_blade":bamboo_blade,

            "sunflower":sunflower,
            "sunflower_icon":sunflower_icon,
            "seed_shot":seed_shot,
            "seed_shot_b":seed_shot_b,
            "seed_shot_icon":seed_shot_icon,

            "paeonia":Paeonia,
            "paeonia_icon":Paeonia_icon,
            "healing_icon":healing_icon,
            "healing":healing,
            "healing_potion_effect":healing_potion_effect,

            "aconite":aconite,
            "poison_dart":poison_dart,
            "poison_start":poison_start,
            "poison_dart_icon":poison_dart_icon,

            "pineapple":pineapple,
            "pineapple_icon":pineapple_icon,
            "p_grenade":pineapple_grenade,
            "pineapple_explosion":pineapple_explosion,
            "p_grenade_icon":pineapple_grenade_icon,

            "bananaflower":bananaflower,
            "bananaflower_icon":bananaflower_icon,
            "banana_slip":banana_slip,
            "banana_slip_icon":banana_slip_icon,
            "banana_fall":banana_fall,
            
            "cabbageflower":cabbageflower,

            "attack": attack_icon,
            "attack_icon": attack_icon,

            "fire_arrow":fire_arrow,
            "fire_arrow_icon":fire_arrow_icon,



            # STATES EFFECT
            "poison":poison,
            "stun":stun,



            # MAP OBJ
            "floor_point": floor_point,
            "items_point": items_point,
            "wall_point": wall_point,
            "stairs_down_point": stairs_down_point,

            "color_tile_1": color_tile_1,
            "block_floor":block_floor,

            "color_tile_walls":color_tile_walls,
            "basic_wall": basic_wall,
            "up_stairs": up_stairs,
            "down_stairs": down_stairs,
            "door_h": door,
            "door_w": door,



            #UI
            "chara_main":chara_main,
            "chara_sheet":chara_sheet,
            "chara_cursor":chara_cursor,
            "first_point":first_point,

            "active_panel":active_panel,
            "passive_panel":passive_panel,
            "massage_panel":massage_panel,
            "map_panel":map_panel,
            "side_panel":side_panel,

            "inventory_main":inventory_main,
            "inventory_sub":inventory_sub,
            "inventory_cursor":inventory_cursor,
            "pop":pop,
            "cool_down":cool_down,
            "black_board":black_board

            }


# playerテクスチャ生成
player = arcade.load_texture_pair(r"image/character/rou/rou6.png")
pc_move = arcade.load_texture_pair(r"image/character/rou/rou6_move.png")
pc_attack = arcade.load_texture_pair(r"image/character/rou/rou6_attack.png")
pc_delay1 = arcade.load_texture_pair(r"image/character/rou/rou6_delay1.png")
pc_delay2 = arcade.load_texture_pair(r"image/character/rou/rou6_delay2.png")
pc_door_open = arcade.load_texture_pair(r"image/character/rou/rou6_door_open.png")
pc_gun = arcade.load_texture_pair(r"image/character/rou/rou6_gun.png")
pc_throw = arcade.load_texture_pair(r"image/character/rou/rou6_throw.png")
pc_defense = arcade.load_texture_pair(r"image/character/rou/rou6_defense.png")
pc_smile = arcade.load_texture_pair(r"image/character/rou/rou6_smile.png")
pc_auto_move = [arcade.load_texture_pair(img) for img in glob.glob(r"image\rou\auto_move\*")]

PC_ID = {"Rou": player,
        "pc_move": pc_move,
        "pc_attack": pc_attack,
        "pc_delay1": pc_delay1,
        "pc_delay2": pc_delay2,
        "pc_door_open": pc_door_open,
        "pc_gun":pc_gun,
        "pc_throw":pc_throw,
        "pc_defense":pc_defense,
        "pc_smile":pc_smile,
        "pc_auto_move":pc_auto_move
            }