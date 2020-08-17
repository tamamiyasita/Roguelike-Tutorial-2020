from itertools import chain
from constants import *
from actor.actor import Actor

class TurnLoop:
    def __init__(self, player) -> None:
        self.active_turn = None
        self.actor = None
        self.sprites = None
        self.player = player

    def loop_on(self, engine):
        self.sprites = [i for i in chain(engine.cur_level.chara_sprites, engine.cur_level.actor_sprites)]


        while self.active_turn is None:

            for sprite in self.sprites:
                if sprite == self.player or sprite.is_visible or sprite.ai and sprite.ai.visible_check:

                    if sprite.wait > 0:
                        sprite.wait -= 1
                        print(sprite.wait)

            for actor in self.sprites:
                if actor.wait <= 1:
                    self.active_turn = actor
                    break


        if self.active_turn == self.player:
            self.actor = self.active_turn
            self.active_turn = True
            engine.fov_recompute = True
            self.player.state = state.READY
        
        if isinstance(self.active_turn, Actor):# and self.active_turn != self.player:
            self.actor = self.active_turn
            self.active_turn = True
            self.actor.ai.take_turn(self.player, engine)
        
        if self.actor and self.actor.state == state.TURN_END or self.actor.state == None:
            self.active_turn = None

        # if self.actor and self.actor != self.player and not self.actor.ai.visible_check:
        #     self.active_turn = None
        
        if self.actor and self.actor.is_dead:
            self.active_turn =None

    def loop_c(self):
        self.active_turn = None
        self.sprites = None

