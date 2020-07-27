import arcade
from actor.actor import Actor
from actor.fighter import Fighter
from data import *
from constants import *

class Player(Actor):
    def __init__(self, x=0, y=0, inventory=0):
        fighter_component = Fighter(hp=35, defense=3, power=5, level=1)
        super().__init__(
            name="player",
            x=x,
            y=y,
            color=arcade.color.WHITE,

            inventory=inventory,
            fighter=fighter_component,

        )

        self.left_face = False
        self.state = state.READY
        self.delay_time = 3.7

    def check_experience_level(self, game_engine):
        if self.fighter.level < len(EXPERIENCE_PER_LEVEL):
            xp_to_next_level = EXPERIENCE_PER_LEVEL[self.fighter.level - 1]
            if self.fighter.current_xp >= xp_to_next_level:
                self.fighter.level += 1
                self.fighter.max_hp += 5
                self.fighter.hp += 5
                self.inventory.capacity += 1
                game_engine.action_queue.extend([{"message":"Level up!!!"}])

    def update_animation(self, delta_time=1 / 60):
        super().update_animation(delta_time)
        if self.state == state.ON_MOVE and not self.left_face:
            self.texture = pc_move[0]
        if self.state == state.ON_MOVE and self.left_face:
            self.texture = pc_move[1]

        if self.state == state.ATTACK and not self.left_face:
            self.texture = pc_attack[0]
        if self.state == state.ATTACK and self.left_face:
            self.texture = pc_attack[1]

        if self.state == state.READY and not self.left_face:
            self.texture = player[0]
            self.delay_time -= delta_time
            if self.delay_time < 0.7:
                self.texture = pc_delay2[0]
            if self.delay_time <= 0.5:
                self.texture = pc_delay[0]
            if self.delay_time < 0:
                self.delay_time = 3.7
        if self.state == state.READY and self.left_face:
            self.texture = player[1]
            self.delay_time -= delta_time
            if self.delay_time < 0.7:
                self.texture = pc_delay2[1]
            if self.delay_time <= 0.5:
                self.texture = pc_delay[1]
            if self.delay_time < 0:
                self.delay_time = 2.7
