import random


class Ticker:
    def __init__(self):
        self.ticks = 0
        self.schedule = {}

    def schedule_turn(self, interval, actor):
        self.schedule.setdefault(self.ticks + interval, []).append(actor)

    def next_turn(self):
        things_to_do = self.schedule.pop(self.ticks, [])
        for actor in things_to_do:
            actor.do_turn()
