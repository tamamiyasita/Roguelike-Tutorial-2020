from util import get_blocking_entity
from constants import *

from attack_effect import AttackEffect


def dist_action(dxy, owner, engine):
    result = []
    dx, dy = dxy[0], dxy[1]
    dist_x, dist_y = dxy[0] + owner.x, dxy[1] + owner.y

    # 行き先に何があるかを調べる
    blocking_actor = get_blocking_entity(dist_x, dist_y, [engine.cur_level.wall_sprites,engine.cur_level.map_obj_sprites,engine.cur_level.actor_sprites])
    owner.dx, owner.dy = dx, dy
    if owner.dx == -1:
        owner.left_face = True
    elif owner.dx == 1:
        owner.left_face = False

    if not blocking_actor:# 何もなければ移動
        walk_action(owner)
    
    elif Tag.door in blocking_actor.tag:
        result.extend(door_action(owner, blocking_actor))

    elif Tag.enemy in blocking_actor.tag:
            result.extend(attack_action(blocking_actor, owner))

    elif Tag.friendly in blocking_actor.tag:
            result.extend(talk_action(blocking_actor, owner))

    return result


def attack_action(enemy, owner):
    if not enemy.is_dead:
        results = owner.fighter.attack(enemy)

        if results:
            owner.combat_effect = AttackEffect(owner, enemy)
            results.extend([{"delay": {"time": 0.1, "action": {"None": owner}}}])

        return results

def talk_action(actor, owner):
    result = [{"talk": actor}]
    if Tag.quest in actor.tag:
        result.extend([{"turn_end": owner}])
    return result

        
def door_action(owner, door):
    result = []
    if Tag.use_door in owner.tag:
        owner.state = state.DOOR
        if door.left_face == False:
            door.left_face = True
            result.extend([{"delay": {"time": 0.2, "action": {"turn_end":owner}}}])
    else:
        result.extend([{"delay": {"time": 0.2, "action": {"turn_end":owner}}}])
    return result


def walk_action(owner):
    if Tag.player in owner.tag:
        owner.state = state.ON_MOVE
        owner.change_x = owner.dx * (MOVE_SPEED)
        owner.change_y = owner.dy * (MOVE_SPEED)
    else:
        owner.x += owner.dx
        owner.y += owner.dy

