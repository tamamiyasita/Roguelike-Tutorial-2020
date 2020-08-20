from itertools import chain
from constants import *
from actor.actor import Actor
from enum import Enum, auto

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

    def loop_on(self, engine):

        # while self.active_turn is None:
        while self.turn == Turn.ON:
            self.sprites = {i for i in chain(engine.cur_level.chara_sprites, engine.cur_level.actor_sprites)}

            for sprite in self.sprites:
                if sprite == self.player or sprite.is_visible or sprite.ai and sprite.ai.visible_check:

                    if sprite.wait > 0:
                        sprite.wait -= 1
                        # print(sprite.wait)

            for actor in self.sprites:
                print(actor.wait, " Actor Wait ", actor.name)
                if actor.wait < 1:
                    self.actor = actor
                    self.turn = Turn.OFF
                    break

        if self.turn == Turn.OFF:
                            
            if self.actor == self.player:
                engine.fov_recompute = True
                self.player.state = state.READY
                self.turn = Turn.DELAY
            else:
                self.actor.ai.take_turn(self.player, engine)
                self.turn = Turn.DELAY

        if self.turn == Turn.DELAY:
            if self.actor.state == state.TURN_END:
                self.turn = Turn.ON
            
            if self.actor.state == None:
                self.turn = Turn.ON

            # if self.actor and self.actor != self.player and not self.actor.ai.visible_check:
            #     self.active_turn = None
            
            if self.actor and self.actor.is_dead:
                self.turn = Turn.ON

    def loop_c(self):
        # self.sprites = None
        self.turn = Turn.ON

