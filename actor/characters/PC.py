from actor.actor import Actor
from actor.fighter import Fighter
from data import *
from constants import *
from actor.equipment import Equipment


class Player(Actor):
    def __init__(self, x=0, y=0, inventory=0):
        fighter_component = Fighter(hp=35, str=3, dex=4, int=4,
                                    unarmed_attack=(1, 1, 2),
                                    hit_rate=100,
                                    defense=3,
                                    evasion=5,
                                    level=1
                                    )
        equip_component = Equipment()
        super().__init__(
            # scale=0.5,
            name="player",
            x=x,
            y=y,
            color=COLORS["white"],

            inventory=inventory,
            fighter=fighter_component,
            equipment=equip_component

        )
        self.tag = {Tag.player}

        self.state = state.READY
        self.delay_time = 5
        self.visible_check = False

    def check_experience_level(self, game_engine):
        if isinstance(self.fighter.level, list):
            self.fighter.level = self.fighter.level[0]

        if self.fighter.level < len(EXPERIENCE_PER_LEVEL):
            xp_to_next_level = EXPERIENCE_PER_LEVEL[self.fighter.level - 1]
            if self.fighter.current_xp >= xp_to_next_level:
                self.fighter.level += 1
                self.fighter.ability_points += 1
                game_engine.action_queue.extend([{"message": "Level up!!!"}])
                game_engine.game_state = GAME_STATE.LEVEL_UP_WINDOW

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
                self.delay_time = 5
        if self.state == state.READY and self.left_face:
            self.texture = player[1]
            self.delay_time -= delta_time
            if self.delay_time < 0.7:
                self.texture = pc_delay2[1]
            if self.delay_time <= 0.5:
                self.texture = pc_delay[1]
            if self.delay_time < 0:
                self.delay_time = 5
