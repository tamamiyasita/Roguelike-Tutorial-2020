from itertools import chain
from constants import *

class TurnLoop:
    def __init__(self, player) -> None:
        self.active_turn = None
        self.actor = None
        self.sprite_list = None
        self.player = player

    def loop_on(self, chara_list=None, actor_list=None):

        while self.active_turn is None:

            if len([self.sprite_list]) <= 1:
                self.sprite_list = (i for i in chain(chara_list, actor_list))

            for sprite in self.sprite_list:
                if sprite.wait > 0:
                    sprite.wait -= 1
                else:
                    self.active_turn = sprite
                    break

        if self.active_turn == self.player:
            self.actor = self.active_turn
            self.active_turn = True
            self.player.state = state.READY
        
        elif self.active_turn.ai:
            self.actor = self.active_turn
            self.active_turn = True
            self.actor.take_turn()
        
        if self.actor and self.actor.state == state.TURN_END:
            self.active_turn = None
        
        if self.actor.is_dead:
            self.active_turn =None

