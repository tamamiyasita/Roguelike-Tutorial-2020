from random import choice
import arcade
from constants import *
from util import grid_to_pixel, skill_activate, skill_deactivate

KEYMAP_UP = [arcade.key.UP, arcade.key.W, arcade.key.NUM_8]
KEYMAP_DOWN = [arcade.key.DOWN, arcade.key.S, arcade.key.NUM_2]
KEYMAP_LEFT = [arcade.key.LEFT, arcade.key.A, arcade.key.NUM_4]
KEYMAP_RIGHT = [arcade.key.RIGHT, arcade.key.D, arcade.key.NUM_6]
KEYMAP_UP_LEFT = [arcade.key.Q, arcade.key.NUM_7, arcade.key.HOME]
KEYMAP_UP_RIGHT = [arcade.key.E, arcade.key.NUM_9, arcade.key.PAGEUP]
KEYMAP_DOWN_LEFT = [arcade.key.Z, arcade.key.NUM_1, arcade.key.END]
KEYMAP_DOWN_RIGHT = [arcade.key.X, arcade.key.NUM_3, arcade.key.PAGEDOWN]

KEYMAP_FIRE = [arcade.key.F]
KEYMAP_REST = [arcade.key.R]
KEYMAP_PICKUP = [arcade.key.G, arcade.key.NUM_5]
KEYMAP_SELECT_ITEM_1 = [arcade.key.KEY_1]
KEYMAP_SELECT_ITEM_2 = [arcade.key.KEY_2]
KEYMAP_SELECT_ITEM_3 = [arcade.key.KEY_3]
KEYMAP_SELECT_ITEM_4 = [arcade.key.KEY_4]
KEYMAP_SELECT_ITEM_5 = [arcade.key.KEY_5]
KEYMAP_SELECT_ITEM_6 = [arcade.key.KEY_6]
KEYMAP_SELECT_ITEM_7 = [arcade.key.KEY_7]
KEYMAP_SELECT_ITEM_8 = [arcade.key.KEY_8]
KEYMAP_SELECT_ITEM_9 = [arcade.key.KEY_9]
KEYMAP_SELECT_ITEM_0 = [arcade.key.KEY_0]
KEYMAP_USE_ITEM = [arcade.key.U]
KEYMAP_EQUIP_ITEM = [arcade.key.E]
KEYMAP_DROP_ITEM = [arcade.key.H]
KEYMAP_CHARACTER_SCREEN = [arcade.key.C]
KEYMAP_INVENTORY = [arcade.key.I]
KEYMAP_USE_STAIRS = [arcade.key.ENTER]
KEYMAP_CANCEL = [arcade.key.ESCAPE]
KEYMAP_DOOR = [arcade.key.K]
KEYMAP_GRID_SELECT = [arcade.key.L]


def choices_key(key):
    """会話画面の選択に使う"""
    choice_point = 0

    if key in KEYMAP_UP:
        choice_point += 1
        return choice_point
    elif key in KEYMAP_DOWN:
        choice_point -= 1
        return choice_point
    elif key == arcade.key.ENTER:
        return "select"


def grid_select_key(key, select_UI):
    """アイテム仕様時のカーソル移動に使用する"""

    if key in KEYMAP_UP:
        select_UI.grid_select[1] += 1
    
    elif key in KEYMAP_DOWN:
        select_UI.grid_select[1] -= 1
        
    elif key in KEYMAP_LEFT:
        select_UI.grid_select[0] -= 1
        
    elif key in KEYMAP_RIGHT:
        select_UI.grid_select[0] += 1
    
    elif key == arcade.key.ENTER:
        select_UI.engine.grid_click(select_UI.dx, select_UI.dy)
        select_UI.grid_press = None
        select_UI.dx, select_UI.dy = 0,0
        select_UI.grid_select = [0,0]
        select_UI.x, select_UI.y = 0,0
        select_UI.engine.game_state = GAME_STATE.NORMAL

    elif key == arcade.key.ESCAPE:
        select_UI.grid_press = None
        select_UI.dx, select_UI.dy = 0,0
        select_UI.grid_select = [0,0]
        select_UI.x, select_UI.y = 0,0
        select_UI.engine.game_state = GAME_STATE.NORMAL


    elif key == arcade.key.TAB:
        select_UI.grid_select = [0, 0]
        select_UI.number += 1




def character_screen_key(key, engine):
    """キャラクタースクリーンで使うキー"""
    skill_list = list(engine.player.fighter.skill_list)

    if key in KEYMAP_CANCEL:
        engine.selected_item = 0
        engine.game_state = GAME_STATE.NORMAL

    if key in KEYMAP_UP:
        engine.selected_item -= 1
        if engine.selected_item < 0:
            engine.selected_item = len(skill_list)-1

    if key in KEYMAP_DOWN:
        engine.selected_item += 1
        if len(skill_list)-1 < engine.selected_item:
            engine.selected_item = 0

    if key in KEYMAP_USE_STAIRS:
        skill = skill_list[engine.selected_item]
        if engine.player.fighter.data["weapon"] is not None and Tag.weapon in skill.tag and skill.name != engine.player.fighter.data["weapon"].name:
            print("main_weapon skillは一つだけしか起動出来ない")
        elif engine.player.fighter.data["weapon"] is None and Tag.weapon in skill.tag:
            skill_activate(engine, engine.player, skill)
        elif engine.player.fighter.data["weapon"] is not None and engine.player.fighter.data["weapon"] == skill:
            skill_deactivate(engine.player, skill)
            
        elif skill.data["switch"] == False:
            skill_activate(engine, engine.player, skill)

        elif skill.data["switch"] == True:
            skill_deactivate(engine.player, skill)
        

        

def inventory_key(key, engine):
    """インベントリを開いたときのキー"""

    if key in KEYMAP_CANCEL:
        engine.selected_item = 0
        engine.game_state = GAME_STATE.NORMAL

    if key in KEYMAP_UP:
        engine.selected_item -= 1
        if engine.selected_item < 0:
            engine.selected_item = engine.player.inventory.capacity-1

    elif key in KEYMAP_DOWN:
        engine.selected_item += 1
        if engine.player.inventory.capacity-1 < engine.selected_item:
            engine.selected_item = 0



    elif key in KEYMAP_USE_ITEM:
        engine.action_queue.extend([{"use_item": True}])
    elif key in KEYMAP_EQUIP_ITEM:
        engine.action_queue.extend([{"equip_item": True}])
    elif key in KEYMAP_DROP_ITEM:
        engine.action_queue.extend([{"drop_item": True}])



def keymap(key, engine):

    if key in KEYMAP_CHARACTER_SCREEN:
        engine.game_state = GAME_STATE.CHARACTER_SCREEN
        
    elif key in KEYMAP_INVENTORY:
        engine.game_state = GAME_STATE.INVENTORY

    elif key in KEYMAP_CANCEL and engine.game_state != GAME_STATE.LEVEL_UP_WINDOW:
        engine.game_state = GAME_STATE.NORMAL

    elif engine.player.state == state.READY and engine.game_state == GAME_STATE.NORMAL:
        direction = None
        if key in KEYMAP_UP:
            direction = (0, 1)
        elif key in KEYMAP_DOWN:
            direction = (0, -1)
        elif key in KEYMAP_LEFT:
            direction = (-1, 0)
        elif key in KEYMAP_RIGHT:
            direction = (1, 0)
        elif key in KEYMAP_UP_LEFT:
            direction = (-1, 1)
        elif key in KEYMAP_DOWN_LEFT:
            direction = (-1, -1)
        elif key in KEYMAP_UP_RIGHT:
            direction = (1, 1)
        elif key in KEYMAP_DOWN_RIGHT:
            direction = (1, -1)
        elif key in KEYMAP_REST:
            engine.action_queue.extend([{"turn_end": engine.player}])

        elif key in KEYMAP_FIRE:
            engine.action_queue.extend([{"fire": engine.player}])

        elif key in KEYMAP_PICKUP:
            engine.action_queue.extend([{"pickup": True}])
        elif key in KEYMAP_SELECT_ITEM_1:
            engine.action_queue.extend([{"use_skill": 1, "user":engine.player}])
        elif key in KEYMAP_SELECT_ITEM_2:
            engine.action_queue.extend([{"use_skill": 2, "user":engine.player}])
        elif key in KEYMAP_SELECT_ITEM_3:
            engine.action_queue.extend([{"use_skill": 3, "user":engine.player}])
        elif key in KEYMAP_SELECT_ITEM_4:
            engine.action_queue.extend([{"use_skill": 4, "user":engine.player}])
        elif key in KEYMAP_SELECT_ITEM_5:
            engine.action_queue.extend([{"use_skill": 5, "user":engine.player}])
        elif key in KEYMAP_SELECT_ITEM_6:
            engine.action_queue.extend([{"use_skill": 6, "user":engine.player}])
        elif key in KEYMAP_SELECT_ITEM_7:
            engine.action_queue.extend([{"use_skill": 7, "user":engine.player}])
        elif key in KEYMAP_SELECT_ITEM_8:
            engine.action_queue.extend([{"use_skill": 8, "user":engine.player}])
        elif key in KEYMAP_SELECT_ITEM_9:
            engine.action_queue.extend([{"use_skill": 9, "user":engine.player}])

        elif key in KEYMAP_USE_ITEM:
            engine.action_queue.extend([{"use_item": True}])
        elif key in KEYMAP_EQUIP_ITEM:
            engine.action_queue.extend([{"equip_item": True}])
        elif key in KEYMAP_DROP_ITEM:
            engine.action_queue.extend([{"drop_item": True}])
        elif key in KEYMAP_USE_STAIRS:
            engine.action_queue.extend([{"use_stairs": True}])
        elif key in KEYMAP_DOOR:
            engine.action_queue.extend([{"close_door": True}])
        elif key in KEYMAP_GRID_SELECT:
            # engine.action_queue.extend([{"grid_select": True}])
            engine.game_state = GAME_STATE.LOOK

        return direction

    elif engine.player.state == state.DOOR:
        direction = None
        if key in KEYMAP_UP:
            direction = (0, 1)
        elif key in KEYMAP_DOWN:
            direction = (0, -1)
        elif key in KEYMAP_LEFT:
            direction = (-1, 0)
        elif key in KEYMAP_RIGHT:
            direction = (1, 0)
        elif key in KEYMAP_UP_LEFT:
            direction = (-1, 1)
        elif key in KEYMAP_DOWN_LEFT:
            direction = (-1, -1)
        elif key in KEYMAP_UP_RIGHT:
            direction = (1, 1)
        elif key in KEYMAP_DOWN_RIGHT:
            direction = (1, -1)
        elif key in KEYMAP_CANCEL:
            engine.player.state = state.READY

        return direction
