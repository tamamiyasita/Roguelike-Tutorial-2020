# doorと同じ処理でtalkにqueueを投げる
from actor.actor import Actor
from data import *
from constants import *

class Villager(Actor):
    def __init__(self, x=0, y=0):
        ai_component = random_move