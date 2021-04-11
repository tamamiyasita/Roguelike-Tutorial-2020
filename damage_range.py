import arcade
from constants import *
from util import grid_to_pixel



def damage_range(skill, engine, xy, range):
    x, y = xy
    results = []
    for xy in range:
        apply_damage(skill, engine, xy[0]+x, xy[1]+y, results)
    print("Click!", x, y)

    print(results, "results")
    return results

def square_shape(size):
    coord_list = []
    width = size
    height = size

    for x in range(-width, width+1):
        for y in range(-height, height+1):
            coord_list.append((x, y))

    return coord_list



# def get_coords_from_shape(damage_range, shooter, target, skill, engine, size=None):
#     results = []
#     delay_time = 10 / skill.shot_speed

#     if damage_range == "single":
#         if not target:
#             engine.action_queue.extend([{"message": "not enemy"}])
#             engine.game_state = GAME_STATE.NORMAL
#             engine.player.state = state.READY
#         else:
#             damage = target[0].fighter.skill_process(skill)
#             engine.action_queue.extend([*damage,{"delay": {"time": delay_time, "action": {"turn_end": shooter}}}])

#     if damage_range == "circle":
#         square_shape(size)

    
def apply_damage(skill, engine, x, y, results):
    position = grid_to_pixel(x, y)
    # print(f"{pixel_x}{pixel_y} apply pixel_x_y")
    sprites = arcade.get_sprites_at_point(
        position, engine.cur_level.actor_sprites)

    for sprite in sprites:
        if sprite.fighter and not sprite.is_dead:
            result = sprite.fighter.skill_process(skill)
            if result:
                results.extend(result)


