from PIL.ImageOps import scale
from actor.actor import Actor
from actor.damage_pop import Damagepop
from constants import *
from data import *
import random
from util import dice

class RegenerationEffect(Actor):
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
        Damagepop(engine, hp_return, arcade.color.GREEN_YELLOW, engine.player)

    def update(self):
        self.x = self.engine.player.x
        self.y = self.engine.player.y
        self.emitter.center_x = self.engine.player.center_x
        self.emitter.center_y = self.engine.player.center_y

        self.particle_time -= 1
        self.emitter.update()
        if self.particle_time < 0:
            self.engine.cur_level.effect_sprites.remove(self)


class Regeneration(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            x=x,
            y=y,
            name="regeneration",
            # not_visible_color=COLORS["black"],

        )
        self.level = 0

        self.max_cooldown_time = 3
        self.cur_cooldown_time = 0

        self.tag = [Tag.item, Tag.used, Tag.active, Tag.skill]

        self.explanatory_text = f"Regeneration testtesttest and test"
        self.icon = IMAGE_ID["paeonia_icon"]



    def recovery_amount(self, player_fighter):
        pc_int = player_fighter.INT
        recovery_min = 2 + int(pc_int/2.5)
        recovery_max = 7 + int(pc_int/2)
        return (recovery_min, recovery_max)




    def use(self, game_engine):
        if self.cur_cooldown_time <= 0:
            self.cur_cooldown_time = self.max_cooldown_time
            player_fighter = game_engine.player.fighter
            min_hp, max_hp = self.recovery_amount(player_fighter)

            self.hp_return = dice(self.level, min_hp, max_hp)

            player_fighter.hp += self.hp_return
            if player_fighter.hp > player_fighter.max_hp:
                player_fighter.hp = player_fighter.max_hp
            Healing = RegenerationEffect(
                game_engine.player.x, game_engine.player.y, self.hp_return, game_engine)

            return [{"message": f"You used the {self.name}"}]
