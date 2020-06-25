import random

class Ticker:
    def __init__(self):
        self.ticks = 0
        self.schedule = {}

    def schedule_turn(self, interval, obj):
        self.schedule.setdefault(self.ticks + interval, []).append(obj)

    def next_turn(self):
        things_to_do = self.schedule.pop(self.ticks, [])
        for obj in things_to_do:
            obj.do_turn()

class Mst:
    def __init__(self, ticker):
        self.ticker = ticker
        self.speed = 6 + random.randrange(1, 6)  #randomspeed+
        self.ticker.schedule_turn(self.speed, self)

    def do_turn(self):
        print(self, "gets a turn at", self.ticker.ticks)
        self.ticker.schedule_turn(self.speed, self)
        

# ticker = Ticker()
# # print(ticker.schedule)

# mnst = []
# while len(mnst) < 5:
#     mnst.append(Mst(ticker))
# # print(ticker.schedule)

# while ticker.ticks < 51:
#     if ticker.ticks in [10, 20, 30, 40, 50]:
#         print()

#     ticker.ticks += 1
#     ticker.next_turn()
    