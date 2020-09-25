import arcade
from arcade import Point, Vector
from arcade.utils import _Vec2
import random
import pyglet

FLASH_TEXTURE = arcade.make_soft_circle_texture(80, (40,40,40))

def make_flash(prev_emitter):
    """花火が爆発した時に短い閃光を表示する"""
    return arcade.Emitter(
        center_xy=prev_emitter.get_pos(),
        emit_controller=arcade.EmitBurst(3),
        particle_factory=lambda emitter: arcade.FadeParticle(
            filename_or_texture=FLASH_TEXTURE,
            change_xy=arcade.rand_in_circle((0.0, 0.0), 3.5),
            lifetime=0.15
        )
    )
def clamp(a, low, high):
    if a > high:
        return high
    elif a < low:
        return low
    else:
        return a


class AnimatedAlphaParticle(arcade.LifetimeParticle):
    """3つの異なるアルファレベルの間でアニメーションするカスタムパーティクル"""

    def __init__(
        self,
        filename_or_texture = arcade.FilenameOrTexture,
        change_xy = Vector,
        start_alpha: int = 0,
        duration1: float = 1.0,
        mid_alpha: int = 255,
        duration2: float = 1.0,
        end_alpha: int = 0,
        center_xy: Point =(0.0, 0.0),
        angle: float = 0,
        change_angle: float = 0,
        scale: float = 1.0,
        mutation_callback=None,
    ):
        super().__init__(filename_or_texture, change_xy, duration1 + duration2, center_xy,
                         angle, change_angle, scale, start_alpha, mutation_callback)
        self.start_alpha = start_alpha
        self.in_duration = duration1
        self.mid_alpha = mid_alpha
        self.out_duration = duration2
        self.end_alpha = end_alpha
    
    def update(self):
        super().update()
        if self.lifetime_elapsed <= self.in_duration:
            u = self.lifetime_elapsed / self.in_duration
            self.alpha = clamp(arcade.lerp(self.start_alpha, self.mid_alpha, u), 0, 255)
        else:
            u = (self.lifetime_elapsed - self.in_duration) / self.out_duration
            self.alpha = clamp(arcade.lerp(self.mid_alpha, self.end_alpha, u), 0, 255)


class Fireworks:
    def __init__(self):
        self.emitters = []
        #self.launch_firework(0)

    def launch_firework(self, delta_time):
        launchers = (
            self.launch_random_firework,
            self.launch_ringed_firework,
            self.launch_sparkle_firework
        )
        random.choice(launchers)(delta_time)
        pyglet.clock.schedule_once(self.launch_firework, random.uniform(1.5, 2.5))

    def launch_random_firework(self, _delta_taime):
        """ランダムな色で爆発するシンプルな花火"""
        



# def firework_spark_mutator(particle: arcade.FadeParticle):
#     # 重力
#     particle.change_x += -0.03

#     particle.change_x *= 0.92
#     particle.change_y *= 0.92