import arcade
from constants import GAME_STATE, state

KEYMAP_UP = [arcade.key.UP, arcade.key.W, arcade.key.NUM_8]
KEYMAP_DOWN = [arcade.key.DOWN, arcade.key.S, arcade.key.NUM_2]
KEYMAP_LEFT = [arcade.key.LEFT, arcade.key.A, arcade.key.NUM_4]
KEYMAP_RIGHT = [arcade.key.RIGHT, arcade.key.D, arcade.key.NUM_6]
KEYMAP_UP_LEFT = [arcade.key.Q, arcade.key.NUM_7, arcade.key.HOME]
KEYMAP_UP_RIGHT = [arcade.key.E, arcade.key.NUM_9, arcade.key.PAGEUP]
KEYMAP_DOWN_LEFT = [arcade.key.Z, arcade.key.NUM_1, arcade.key.END]
KEYMAP_DOWN_RIGHT = [arcade.key.X, arcade.key.NUM_3, arcade.key.PAGEDOWN]
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
KEYMAP_EQUIP_ITEM = [arcade.key.J]
KEYMAP_DROP_ITEM = [arcade.key.H]
KEYMAP_CHARACTER_SCREEN = [arcade.key.C]
KEYMAP_USE_STAIRS = [arcade.key.ENTER]
KEYMAP_CANCEL = [arcade.key.ESCAPE]
KEYMAP_CLOSE_DOOR = [arcade.key.L]


def keymap(key, engine):

    if key in KEYMAP_CHARACTER_SCREEN:
        engine.game_state = GAME_STATE.CHARACTER_SCREEN

    elif key in KEYMAP_CANCEL:
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
            engine.player.state = state.TURN_END

        elif key in KEYMAP_PICKUP:
            engine.action_queue.extend([{"pickup": True}])
        elif key in KEYMAP_SELECT_ITEM_1:
            engine.action_queue.extend([{"select_item": 1}])
        elif key in KEYMAP_SELECT_ITEM_2:
            engine.action_queue.extend([{"select_item": 2}])
        elif key in KEYMAP_SELECT_ITEM_3:
            engine.action_queue.extend([{"select_item": 3}])
        elif key in KEYMAP_SELECT_ITEM_4:
            engine.action_queue.extend([{"select_item": 4}])
        elif key in KEYMAP_SELECT_ITEM_5:
            engine.action_queue.extend([{"select_item": 5}])
        elif key in KEYMAP_SELECT_ITEM_6:
            engine.action_queue.extend([{"select_item": 6}])
        elif key in KEYMAP_SELECT_ITEM_7:
            engine.action_queue.extend([{"select_item": 7}])
        elif key in KEYMAP_SELECT_ITEM_8:
            engine.action_queue.extend([{"select_item": 8}])
        elif key in KEYMAP_SELECT_ITEM_9:
            engine.action_queue.extend([{"select_item": 9}])
        elif key in KEYMAP_SELECT_ITEM_0:
            engine.action_queue.extend([{"select_item": 0}])
        elif key in KEYMAP_USE_ITEM:
            engine.action_queue.extend([{"use_item": True}])
        elif key in KEYMAP_EQUIP_ITEM:
            engine.action_queue.extend([{"equip_item": True}])
        elif key in KEYMAP_DROP_ITEM:
            engine.action_queue.extend([{"drop_item": True}])
        elif key in KEYMAP_USE_STAIRS:
            engine.action_queue.extend([{"use_stairs": True}])
        elif key in KEYMAP_CLOSE_DOOR:
            engine.action_queue.extend([{"close_door": True}])

        return direction

    elif engine.player.state == state.DOOR and engine.game_state == GAME_STATE.NORMAL:
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
        return direction