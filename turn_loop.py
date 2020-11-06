from itertools import chain
from constants import *
from actor.actor import Actor
from enum import Enum, auto
import logging

# log = logging.getLogger(__name__)


class Turn(Enum):
    ON = auto()
    OFF = auto()
    DELAY = auto()


class TurnLoop:
    def __init__(self, player) -> None:
        self.actor = None
        self.sprites = None
        self.player = player
        self.turn = Turn.ON

    def cooldown_charge(self, actor):
        if hasattr(actor, "fighter") and actor.fighter.active_skill:
            for skill in actor.fighter.active_skill:
                if 0 < skill.cur_cooldown_time:
                    print(skill.cur_cooldown_time, skill)
                    skill.cur_cooldown_time -= 1


    def loop_on(self, engine):
        """actor間のメインループ制御"""

        while self.turn == Turn.ON:
            self.sprites = {i for i in chain(
                engine.cur_level.chara_sprites, engine.cur_level.actor_sprites)}

            for sprite in self.sprites:
                # playerもしくは他のactorの時はvisibleの場合のみwaitを減らす
                if sprite == self.player or sprite.is_visible or sprite.ai and sprite.ai.visible_check:

                    if sprite.wait > 0:
                        sprite.wait -= 1

            # waitが0になったactorに行動権を与えてループ終了
            for actor in self.sprites:
                if actor.is_dead:
                    continue
                if actor.wait < 1 and actor.state:
                    self.actor = actor
                    self.turn = Turn.OFF
                    break

        if self.turn == Turn.OFF:


            if self.actor == self.player:
                self.player.state = state.READY
                self.turn = Turn.DELAY
                engine.fov_recompute = True
            elif Tag.enemy in self.actor.tag:
                result = self.actor.ai.take_turn(self.player, engine)
                if result:
                    engine.action_queue.extend(result)
                self.turn = Turn.DELAY
            elif Tag.friendly in self.actor.tag:
                result = self.actor.ai.take_turn(engine)
                if result:
                    engine.action_queue.extend(result)
                self.turn = Turn.DELAY

            
        elif self.turn == Turn.DELAY:
            # log.debug(
            #     f"{self.actor.name=}, {self.actor.wait=}, {self.actor.state=}, {self.actor.is_dead=}")
            if self.actor.state is state.TURN_END or self.actor.state is None or self.actor.is_dead:
                self.turn = Turn.ON
                self.cooldown_charge(self.actor)

    