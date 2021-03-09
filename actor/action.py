from util import get_blocking_entity
from constants import *

def dist_action(dxy, owner, engine):
    dx, dy = dxy[0], dxy[1]
    dist_x, dist_y = dxy[0] + owner.x, dxy[1] + owner.y

    # 行き先に何があるかを調べる
    blocking_actor = get_blocking_entity(dist_x, dist_y, [engine.cur_level.wall_sprites,engine.cur_level.map_obj_sprites,engine.cur_level.actor_sprites])
    owner.dx, owner.dy = dx, dy

    if not blocking_actor:# 何もなければ移動
        walk_action(owner)

        




def walk_action(owner):
    if Tag.player in owner.tag:
        owner.state = state.ON_MOVE
        owner.change_x = owner.dx * (MOVE_SPEED)
        owner.change_y = owner.dy * (MOVE_SPEED)




# class WalkAction:
#     def __init__(self):
#         pass



#     def move(self, dxy, target=None, engine=None):
#         # self.attack_delay = 7
#         wall_sprites = engine.cur_level.wall_sprites
#         map_obj_sprites = engine.cur_level.map_obj_sprites
#         actor_sprites = engine.cur_level.actor_sprites

#         self.dx, self.dy = dxy

#         # 振動ダメージエフェクトに使う変数
#         self.attack_target = None
#         self.attack_target_x = None

#         if self.dx == -1:
#             self.left_face = True
#         if self.dx == 1:
#             self.left_face = False

#         destination_x = self.dx + self.x
#         destination_y = self.dy + self.y

#         self.from_x = self.center_x
#         self.from_y = self.center_y


#         # 行き先がBlockされてるか調べる
#         blocking_actor = get_blocking_entity(
#             destination_x, destination_y, [actor_sprites, wall_sprites, map_obj_sprites])

#         def player_move():

#             if blocking_actor and not target:
#                 # playerの攻撃チェック
#                 actor = blocking_actor[0]
#                 if Tag.wall in actor.tag:
#                     return [{"None": True}]

#                 if Tag.door in actor.tag:
#                     self.state = state.DOOR
#                     door_actor = actor
#                     if door_actor.left_face == False:
#                         door_actor.left_face = True
#                         return [{"delay": {"time": 0.3, "action": {"turn_end":self}}}]

#                 if Tag.friendly in actor.tag:
#                     result = [{"talk": actor}]
#                     if Tag.quest in actor.tag:
#                         result.extend([{"turn_end": self}])
#                     return result

#                 elif Tag.enemy in actor.tag and not actor.is_dead:
#                     attack_results = self.fighter.attack(actor)

#                     if attack_results:
#                         self.state = state.ATTACK
#                         self.change_y = self.dy * (MOVE_SPEED -4)
#                         self.change_x = self.dx * (MOVE_SPEED -4)
#                     self.combat_effect = AttackEffect(self, actor)
#                     engine.action_queue.extend(
#                             [{"delay": {"time": 0.2, "action": {"None": self}}}])

#                     return attack_results

#             else:
#                 self.state = state.ON_MOVE
#                 self.change_y = self.dy * (MOVE_SPEED)
#                 self.change_x = self.dx * (MOVE_SPEED)
#         @stop_watch
#         def monster_move(target):

#             if target and self.distance_to(target) <= 1.46:
#                 # monsterの攻撃チェック
#                 attack_results = self.fighter.attack(target)
#                 self.combat_effect = AttackEffect(self, target)

#                 if attack_results:
#                     self.state = state.ATTACK
#                     self.change_y = self.dy * (MOVE_SPEED+5)
#                     self.change_x = self.dx * (MOVE_SPEED+5)

#                 return attack_results

#             elif not get_blocking_entity(destination_x, destination_y, [actor_sprites,wall_sprites]):
#                 # monsterの移動
#                 self.x = destination_x
#                 self.y = destination_y
#                 self.wait += self.speed
#                 self.state = state.TURN_END

#             else:
#                 # A*パスがBlockされたらturn_endを返す
#                 print(f"actor {self.name} blocking pass!")
#                 return [{"turn_end": self}]

#         if self.ai:
#             return monster_move(target)

#         else:
#             return player_move()

#     def update(self, delta_time=1/60):
#         super().update()
#         if self.state == state.ON_MOVE:
#             if abs(self.from_x - self.center_x) >= GRID_SIZE and self.dx or\
#                     abs(self.from_y - self.center_y) >= GRID_SIZE and self.dy:
#                 self.change_x = 0
#                 self.change_y = 0
#                 self.x += self.dx
#                 self.y += self.dy
#                 self.wait += self.speed
#                 self.from_x, self.from_y = self.center_x, self.center_y
#                 self.state = state.TURN_END

  
  
#     def distance_to(self, other):
#         dx = other.x - self.x
#         dy = other.y - self.y
#         return math.sqrt(dx ** 2 + dy ** 2)

#     def move_towards(self, target, engine):

#         actor_sprites = engine.cur_level.actor_sprites

#         dx = target.x - self.x
#         dy = target.y - self.y
#         distance = math.sqrt(dx ** 2 + dy ** 2)

#         dx = int(round(dx / distance))
#         dy = int(round(dy / distance))

#         if not get_blocking_entity(self.x + dx, self.y + dy, [actor_sprites]):
#             move = self.move((dx, dy), target, engine)
#             return move
