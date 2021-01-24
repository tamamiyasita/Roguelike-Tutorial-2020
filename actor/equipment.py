from collections import Counter
from constants import *
from itertools import chain


class Equipment:
    """装備部位とそこからの追加bonusを返す
       装備の切り替えもここで行う
       bonusはEquippable関数で設定する
    """

    def __init__(self):
        """アイテムスロット、及び装備するタイミングを決めるequip_update_check
        """
        self.item_slot = []


        # 装備変更によるスプライト更新のチェックに使う変数
        self.equip_update_check = False

    def get_dict(self):
        result = [i.__class__.__name__ if i else None for i in self.item_slot] 

        return result

    def restore_from_dict(self, result):

        for item in self.owner.inventory.item_bag:
            if item and item.__class__.__name__ in result:
                self.toggle_equip(item)
                

        self.equip_update_check = True

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
    def skill_level_sum(self):
        """装備スロットをループしてskill levelの合計を返す"""
        bonus = {}
        for parts in self.item_slot:  # crisiumが入る
            # crisiumのskill_add{leaf_blade:1}が入る
            if parts and not isinstance(parts, str) and parts.skill_add:
                bonus = Counter(bonus) + Counter(parts.skill_add)

        return bonus  # {leaf_blade:1}


    @property
    def states_bonus(self):
        """item_slotをループしてstates bonusを合計し返す"""

        bonus = {"max_hp": 0, "max_mp": 0, "STR": 0,
                 "DEX": 0, "INT": 0, "defense": 0, "evasion": 0}
        for parts in self.item_slot:
            if parts and not isinstance(parts, str) and parts.states_bonus:
                bonus = Counter(bonus) + Counter(parts.states_bonus)

        return bonus


    def toggle_equip(self, equip_item):
        """装備アイテムの付け外しを行うメソッド
        """
        flower_position = {0:(21, 1), 1:(22, 18), 2:(10, 27), 3:(-5, 25), 4:(-20, 23)}#花の位置を決める辞書
        results = []

        for item in self.item_slot:
            if item == equip_item:

                del item.master
                self.item_slot.remove(item)
                
                results.extend([{"message": f"dequipped {item.name}"}])
                self.equip_update_check = True
                return results


        if 5 > len(self.item_slot):


            self.item_slot.append(equip_item)
            equip_item.master = self.owner
            pos = len(self.item_slot)
            for i in range(pos):
                self.item_slot[i].item_margin_x = flower_position[i][0]
                self.item_slot[i].item_margin_y = flower_position[i][1]

            results.append({"message": f"equipped {equip_item.name}"})

            self.equip_update_check = True
            return results
