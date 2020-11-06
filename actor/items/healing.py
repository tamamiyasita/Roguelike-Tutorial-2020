from actor.actor import Actor
from actor.damage_pop import Damagepop
from constants import *
from data import *
import random
from util import dice, result_add

class HealingEffect(Actor):
    def __init__(self, x, y, hp_return, engine):
        super().__init__(
            x=x,
            y=y,
            name="healing_potion_effect",
            color=COLORS["white"]
        )
        self.engine = engine
        self.alpha = 150
        self.particle_time = 100
        self.emitter = arcade.Emitter(
            center_xy=(self.center_x, self.center_y),
            emit_controller=arcade.EmitterIntervalWithTime(0.003 * 5, 0.2),
            particle_factory=lambda emitter: arcade.LifetimeParticle(
                filename_or_texture=IMAGE_ID["healing_potion_effect"][0],
                change_xy=arcade.rand_on_circle((0.0, 0.0), 1.2),
                lifetime=0.8,
                scale=random.random()*2,
                alpha=random.randint(25, 115)

            )
        )
        self.alpha = 0
        self.engine.cur_level.effect_sprites.append(self)
        # Damagepop(engine, hp_return, arcade.color.GREEN_YELLOW, engine.player)

    def update(self):
        self.x = self.engine.player.x
        self.y = self.engine.player.y
        self.emitter.center_x = self.engine.player.center_x
        self.emitter.center_y = self.engine.player.center_y

        self.particle_time -= 1
        self.emitter.update()
        if self.particle_time < 0:
            self.engine.cur_level.effect_sprites.remove(self)


class Healing(Actor):
    def __init__(self, engine=None ):
        super().__init__(
            name="healing",

        )

        self.engine = engine
        self.level = 0

        self.max_cooldown_time = 3
        self.cur_cooldown_time = 0

        self.tag = [Tag.item, Tag.used, Tag.active, Tag.skill]

        self.explanatory_text = f"Recover a small amount of hp"
        self.icon = IMAGE_ID["paeonia_icon"]

    @property
    def hp_return(self):

        max_hp = 7 + int(self.engine.player.fighter.INT/2)

        return self.level, max_hp




    def use(self):
        if self.cur_cooldown_time <= 0:
            self.cur_cooldown_time = self.max_cooldown_time+1

            hp_return = dice(*self.hp_return)

            result = self.engine.player.fighter.change_hp(hp_return)
            Healing = HealingEffect(
                self.engine.player.x, self.engine.player.y, hp_return, self.engine)

            return [{"message": f"You have recovered {hp_return} using {self.name}"}, *result]
