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

        self.equip_slot = []

        # 装備変更によるスプライト更新のチェックに使う変数
        self.equip_update_check = False

    def get_dict(self):
        result = [i.__class__.__name__ if i else None for i in self.item_slot] 
        print(result)


        return result

    def restore_from_dict(self, result):

        for item in self.owner.inventory.item_bag:
            if item and item.__class__.__name__ in result:
                self.toggle_equip(item)

        print(self.item_slot)

        self.equip_update_check = True

    def sprite_check(self, sprites):
            # 装備スプライトをスプライトリストに入れて表示する
            for equip in chain(self.equip_slot,self.item_slot):
                if equip and not isinstance(equip, str) and equip not in sprites and Tag.image_off not in equip.tag:
                    sprites.append(equip)

            # 装備解除しスプライトがスロットから無くなればスプライトリストからも削除
            for sprite in sprites:
                if sprite not in self.equip_slot and sprite not in self.item_slot:
                    sprites.remove(sprite)

    def equip_position_reset(self):
        # 装備アイテムの表示位置をリセットする
            for equip in chain(self.equip_slot,self.item_slot):
                if equip:
                    equip.x = self.owner.x
                    equip.y = self.owner.y



    @property
    def skill_level_sum(self):
        """装備スロットをループしてskill levelの合計を返す"""

        bonus = {}
        for parts in self.item_slot:  # crisiumが入る
            # crisiumのskill_add{leaf_blade:1}が入る
            if parts and not isinstance(parts, str) and parts.skill_add:
                bonus = Counter(bonus) + Counter(parts.skill_add)

        return bonus  # {leaf_blade:1}

    def update(self, sprites):
        """装備スプライトの表示はここで行う"""
        if self.equip_update_check:

            self.sprite_check(sprites)


            # 装備更新完了通知
            self.equip_update_check = False

            # 装備変更に伴うskill check
            self.owner.fighter.passive_skill_activate()

            print(self.owner.fighter.skill_list)


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
        results = []

        for i, item in enumerate(self.item_slot):
            if item == equip_item:

                del item.master
                self.item_slot.remove(item)
                results.append({"message": f"dequipped {item.name}"})

                self.equip_update_check = True
                return results

        # for i, item in enumerate(self.item_slot):
        #     if item:
        if 5 > len(self.item_slot):


            self.item_slot.append(equip_item)
            equip_item.master = self.owner

            results.append({"message": f"equipped {equip_item.name}"})

            self.equip_update_check = True
            return results
