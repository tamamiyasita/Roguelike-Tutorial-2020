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

    def elapsed_time(self, actor, queue, engine):
        """スキルクールダウンとステータス効果時間のカウントダウンを行う"""
        if actor.fighter.skill_list:
            for skill in actor.fighter.skill_list:
                if hasattr(skill, "max_cooldown_time"):
                    if skill.data["cooldown"] == False:
                        skill.data["cooldown"] = True

                    elif skill.data["cooldown"]:
                        skill.data["count_time"] -= 1

                        if 0 >= skill.data["count_time"]:
                            skill.data["cooldown"] = False
                else:
                    continue
                

        if actor.fighter.states:
            for states in actor.fighter.states:
                if 0 < states.data["count_time"]:
                    states.data["count_time"] -= 1     
                    queue.extend(states.apply(engine))

                print(states.data["count_time"], states)
                

    def loop_on(self, engine):
        """actor間のメインループ制御"""
        queue = engine.action_queue

        while self.turn == Turn.ON:
            self.sprites = {i for i in chain(engine.cur_level.chara_sprites, engine.cur_level.actor_sprites)}

            # waitが0になったactorに行動権を与えてループ終了
            for actor in self.sprites:
                if actor.is_dead:
                    continue
                if actor.wait < 1:
                    self.actor = actor
                    self.turn = Turn.OFF
                    break
            for sprite in self.sprites:
                # playerもしくは他のactorの時はvisibleの場合のみwaitを減らす
                if sprite == self.player or sprite.is_visible or sprite.ai and sprite.ai.visible_check:

                    if sprite.wait > 0:
                        sprite.wait -= 1



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
                self.elapsed_time(self.actor, queue, engine)
                self.turn = Turn.ON

    