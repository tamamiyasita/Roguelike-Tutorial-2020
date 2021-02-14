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
        self.item_slot = arcade.SpriteList()
        self.skill_list = set()# arcade.SpriteList()

        self.states_bonus = {"max_hp": 0, "max_mp": 0, "STR": 0,
                 "DEX": 0, "INT": 0, "defense": 0, "evasion": 0}

        
        self.flower_position = {i:(40*math.cos(math.radians(s)), 40*math.sin(math.radians(s))) for i, s in enumerate([30,60,90,120,150])}
        self.flower_position2 = {i:(60*math.cos(math.radians(s)), 60*math.sin(math.radians(s))) for i, s in enumerate([40,70,100,130,150])}



    def get_dict(self):
        result = [i.__class__.__name__ if i else None for i in self.item_slot] 

        return result

    def restore_from_dict(self, result):

        for item in self.owner.inventory.item_bag:
            if item and item.__class__.__name__ in result:
                self.toggle_equip(item)
                


    # 階層を移動する時に使う関数
    def item_sprite_check(self, sprites):
            # 花スプライトをスプライトリストに入れて表示する
            for item in self.item_slot:
                if item and item not in sprites and not isinstance(item, str):
                    sprites.append(item)
                

    def equip_position_reset(self):
        # 装備アイテムの表示位置をリセットする
            for equip in self.item_slot:
                if equip:
                    equip.x = self.owner.x
                    equip.y = self.owner.y

    def item_exp_add(self, exp):
        # 花にexpを与える
        for item in self.item_slot:
            if hasattr(item, "current_xp"):
                item.current_xp += exp

    @property
    def skill_generate_list(self):
        self.skill_list = set()
        # Skillの生成チェック
        skill_gen = [item.skill_generate for item in self.item_slot]

        for skill_name in skill_gen:
            skill = self.owner.fighter.base_skill_dict.get(skill_name)

            self.skill_list.add(skill)


        return self.skill_list


    
    def skill_level_sum_update(self):
        """装備スロットをループしてskill levelの合計を返す"""
        bonus = {}
        for parts in self.item_slot:  # crisiumが入る
            # crisiumのskill_add{grass_cutter:1}が入る
            for name, add in parts.skill_add.items():
                bonus = Counter(bonus) + Counter({name:add})

        for skill in self.skill_generate_list:
            if skill.name in bonus:
                skill.level = bonus[skill.name]

        self.skill_list = {skill for skill in self.skill_list if skill.name in bonus.keys()}

        # return self.skill_list


    
    def states_bonus_update(self):
        """item_slotをループしてstates bonusを合計し返す"""

        bonus = {"max_hp": 0, "max_mp": 0, "STR": 0,
                 "DEX": 0, "INT": 0, "defense": 0, "evasion": 0}
        for parts in self.item_slot:
            if parts and not isinstance(parts, str) and parts.states_bonus:
                bonus = Counter(bonus) + Counter(parts.states_bonus)

        self.states_bonus = bonus


    def toggle_equip(self, equip_item):
        """装備アイテムの付け外しを行うメソッド
        """


        results = []

        for item in self.item_slot:
            if item == equip_item:

                del item.master
                item.remove_from_sprite_lists()
                
                results.extend([{"message": f"dequipped {item.name}"}])

                self.states_bonus_update()
                self.skill_level_sum_update()
                
                return results


        if 10 > len(self.item_slot):


            self.item_slot.append(equip_item)
            equip_item.master = self.owner
            pos = len(self.item_slot)
            if pos < 6:
                for i in range(0, pos):
                    self.item_slot[i].item_margin_x = self.flower_position[i][0]
                    self.item_slot[i].item_margin_y = self.flower_position[i][1]
            if pos >= 6:
                for j in range(5, pos):
                    self.item_slot[j].item_margin_x = self.flower_position2[j-5][0]
                    self.item_slot[j].item_margin_y = self.flower_position2[j-5][1]

            results.append({"message": f"equipped {equip_item.name}"})

            self.states_bonus_update()
            self.skill_level_sum_update()

            return results
