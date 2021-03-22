import math
from collections import Counter
from constants import *
from itertools import chain
from actor.actor_set import *

class Equipment:
    """装備部位とそこからの追加bonusを返す
       装備の切り替えもここで行う
       bonusはEquippable関数で設定する
    """

    def __init__(self):
        """アイテムスロット、及び装備するタイミングを決めるequip_update_check
        """
        self.flower_slot = arcade.SpriteList()
        self.skill_list = []# arcade.SpriteList()

        self.states_bonus = {"max_hp": 0,"STR": 0,"DEX": 0, "INT": 0,
                             "defense": 0, "evasion": 0, "attack_speed":0}
        self.description_bonus={"brilliant":0, "glow":0, "fragrance":0, "sharp":0, "robust":0, "supple":0, "medicinal":0}
        self.affinity_bonus = {"physical": 0, "fire": 0, "ice": 0, "lightning":0, "acid": 0, "poison": 0, "mind": 0}
        self.resist_bonus = {"physical": 0, "fire": 0, "ice": 0, "lightning":0, "acid": 0, "poison": 0, "mind": 0}
        
        self.flower_position = {i:(40*math.cos(math.radians(s)), 40*math.sin(math.radians(s))) for i, s in enumerate([30,60,90,120,150])}
        self.flower_position2 = {i:(60*math.cos(math.radians(s)), 60*math.sin(math.radians(s))) for i, s in enumerate([40,70,100,130,150])}



    def get_dict(self):
        result = {i.__class__.__name__:i.get_dict() for i in self.flower_slot}

        return result

    def restore_from_dict(self, result):
        for i, s in result.items():
            for item in self.owner.inventory.item_bag:
                if item and item.__class__.__name__ == i:
                    item.restore_from_dict(s)
                    self.toggle_equip(item)
                


    # 階層を移動する時に使う関数
    def item_sprite_check(self, sprites):
            # 花スプライトをスプライトリストに入れて表示する
            for item in self.flower_slot:
                if item and item not in sprites and not isinstance(item, str):
                    sprites.append(item)
                

    def equip_position_reset(self):
        # 装備アイテムの表示位置をリセットする
            for equip in self.flower_slot:
                if equip:
                    equip.x = self.owner.x
                    equip.y = self.owner.y

    def item_exp_add(self, exp):
        # 花にexpを与える
        for item in self.flower_slot:
            if hasattr(item, "current_xp"):
                item.current_xp += exp

    def skill_list_update(self):
        self.skill_list = set()
        # Skillの生成チェック
        skill_gen = [item.flower_skill for item in self.flower_slot]

        self.skill_list = skill_gen


    def affinity_bonus_update(self):
        """flower_slotをループしてaffinity bonusを合計し返す"""

        color = {"orange":"physical", "red":"fire", "white":"ice", "blue":"lightning", "yellow":"acid", "purple":"poison", "pink":"mind"}

        bonus = {"physical": 0, "fire": 0, "ice": 0, "lightning":0, "acid": 0, "poison": 0, "mind": 0}

        for parts in self.flower_slot:
            if parts and not isinstance(parts, str) and parts.flower_color:
                c = parts.flower_color
                bonus[color[c]] += 1

        self.affinity_bonus = bonus
    
    def description_bonus_update(self):
        """flower_slotをループしてdescription bonusを合計し返す"""

        bonus={"brilliant":0, "glow":0, "fragrance":0, "sharp":0, "robust":0, "supple":0, "medicinal":0}

        for parts in self.flower_slot:
            if parts and not isinstance(parts, str) and parts.description:
                bonus = Counter(bonus) + Counter(parts.description)

        self.description_bonus = bonus

    def resist_bonus_update(self):
        """flower_slotをループしてresist bonusを合計し返す"""

        bonus = {"physical": 0, "fire": 0, "ice": 0, "lightning":0, "acid": 0, "poison": 0, "mind": 0}

        for parts in self.flower_slot:
            if parts and not isinstance(parts, str) and parts.resist_bonus:
                bonus = Counter(bonus) + Counter(parts.resist_bonus)

        self.resist_bonus = bonus

    def states_bonus_update(self):
        """flower_slotをループしてstates bonusを合計し返す"""

        bonus = {"max_hp": 0, "max_mp": 0, "STR": 0,
                 "DEX": 0, "INT": 0, "defense": 0, "evasion": 0}
        for parts in self.flower_slot:
            if parts and not isinstance(parts, str) and parts.states_bonus:
                bonus = Counter(bonus) + Counter(parts.states_bonus)

        self.states_bonus = bonus


    def toggle_equip(self, equip_item):
        """装備アイテムの付け外しを行うメソッド
        """


        results = []

        for item in self.flower_slot:
            if item == equip_item:

                del item.master
                item.remove_from_sprite_lists()
                
                results.extend([{"message": f"dequipped {item.name}"}])

                self.states_bonus_update()
                self.skill_list_update()
                self.resist_bonus_update()
                self.affinity_bonus_update()
                self.description_bonus_update()

                
                return results


        if 10 > len(self.flower_slot):


            self.flower_slot.append(equip_item)
            equip_item.master = self.owner
            equip_item.flower_skill.master = self.owner
            pos = len(self.flower_slot)
            if pos < 6:
                for i in range(0, pos):
                    self.flower_slot[i].item_margin_x = self.flower_position[i][0]
                    self.flower_slot[i].item_margin_y = self.flower_position[i][1]
            if pos >= 6:
                for j in range(5, pos):
                    self.flower_slot[j].item_margin_x = self.flower_position2[j-5][0]
                    self.flower_slot[j].item_margin_y = self.flower_position2[j-5][1]

            results.append({"message": f"equipped {equip_item.name}"})

            self.states_bonus_update()
            self.skill_list_update()
            self.resist_bonus_update()
            self.affinity_bonus_update()
            self.description_bonus_update()

            return results
