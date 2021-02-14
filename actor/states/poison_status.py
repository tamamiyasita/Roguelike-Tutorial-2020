from actor.actor import Actor
from constants import *
from data import *
import random
from util import dice, result_add

class PoisonEffect(Actor):
    def __init__(self, owner, engine):
        super().__init__(
            x=owner.x,
            y=owner.y,
            name="poison",
            color=COLORS["white"]
        )
        self.owner = owner
        self.color = self.color
        self.engine = engine
        self.alpha = 150
        self.particle_time = 30
        self.emitter = arcade.Emitter(
            center_xy=(self.center_x, self.center_y),
            emit_controller=arcade.EmitBurst(20),
            particle_factory=lambda emitter: arcade.LifetimeParticle(
                filename_or_texture=IMAGE_ID["poison"][0],
                change_xy=arcade.rand_in_circle((0.0, 0.0), 1.0),
                lifetime=0.7,
                scale=random.random()*2.8,
                alpha=random.uniform(42, 138)
            )
        )
        self.alpha = 0
        self.engine.tmp_effect_sprites.append(self)

    def update_animation(self, delta_time=1 / 60):
        super().update_animation(delta_time)
        self.owner.color = (60,255,60)
        self.x = self.owner.x
        self.y = self.owner.y
        self.emitter.center_x = self.owner.center_x
        self.emitter.center_y = self.owner.center_y

        self.particle_time -= 1
        self.emitter.update()
        if self.particle_time < 1:
            self.owner.color = self.color
            self.particle_time = 30
            self.engine.tmp_effect_sprites.remove(self)


class PoisonStatus(Actor):
    def __init__(self, count_time=None):
        super().__init__(
            name="poison",
            scale=4.5,

        )

        self.data={"switch":False,
            "count_time":count_time,
            "cooldown":False}
        self.owner = None
        self.power = 3
        self.max_cooldown_time = 4


        self.attr = "poison"


        self.level = 0


        self.tag = [Tag.item, Tag.used, Tag.active, Tag.skill]

        self.explanatory_text = f""
        self.icon = IMAGE_ID["poison"]




    def apply(self, engine):
        self.engine = engine

        if self.owner and self.data["count_time"] >= 0:
            color = self.owner.color

            result = self.owner.fighter.change_hp(self.power)
            self.poison = PoisonEffect(
                self.owner,  self.engine)

            return [{"message": f"{self.owner.name} took {self.power} damage from poison"}, *result]