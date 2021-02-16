import arcade
from constants import *
from util import grid_to_pixel



def circle_range(skill, engine, x, y):
    print("Click!", x, y)
    results = []
    apply_damage(skill, engine,x, y, results)

    apply_damage(skill, engine,x-1, y-1, results)
    apply_damage(skill, engine,x, y-1, results)
    apply_damage(skill, engine,x+1, y-1, results)

    apply_damage(skill, engine,x-1, y, results)
    apply_damage(skill, engine,x+1, y, results)

    apply_damage(skill, engine,x-1, y+1, results)
    apply_damage(skill, engine,x, y+1, results)
    apply_damage(skill, engine,x + 1, y + 1, results)

    print(results, "results")
    return results
def apply_damage(skill, engine, grid_x, grid_y, results):
    pixel_x, pixel_y = grid_to_pixel(grid_x, grid_y)
    print(f"{pixel_x}{pixel_y} apply pixel_x_y")
    sprites = arcade.get_sprites_at_point(
        (pixel_x, pixel_y), engine.cur_level.actor_sprites)

    for sprite in sprites:
        if sprite.fighter and not sprite.is_dead:
            result = sprite.fighter.skill_process(skill)
            if result:
                results.extend(result)


