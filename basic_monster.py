import arcade


class Basic_monster:
    def __init__(self):
        self.owner = None

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        monster = self.owner
        if monster.is_visible:

            if monster.distance_to
