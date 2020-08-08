from constants import *

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

        return direction
