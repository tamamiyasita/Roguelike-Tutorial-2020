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
        self.equip_slot = {
            "head": None,
            "main_hand": None,
            "off_hand": None,
            "ranged_weapon": None,
        }
        self.item_slot = {
            "flower1": None,
            "flower2": None,
            "flower3": None,
        }

        # 装備変更によるスプライト更新のチェックに使う変数
        self.equip_update_check = False

    def get_dict(self):
        result = [i.__class__.__name__ if i else None for i in self.item_slot.values()] 
        print(result)


        return result

    def restore_from_dict(self, result):

        for item in self.owner.inventory.item_bag:
            if item and item.__class__.__name__ in result:
                self.toggle_equip(item)

        print(self.item_slot)

        self.equip_update_check = True

    def sprite_check(self, sprites):
            # 遠隔武器以外がスロットに入っていたら装備スプライトをスプライトリストに入れて表示する
            for equip in chain(self.equip_slot.values(),self.item_slot.values()):
                if equip and not isinstance(equip, str) and equip not in sprites and not equip.slot == "ranged_weapon":
                    sprites.append(equip)

            # 装備解除しスプライトがスロットから無くなればスプライトリストからも削除
            for sprite in sprites:
                if sprite not in self.equip_slot.values() and sprite not in self.item_slot.values():
                    sprites.remove(sprite)

    def equip_position_reset(self):
        # 装備アイテムの表示位置をリセットする
            for equip in chain(self.equip_slot.values(),self.item_slot.values()):
                if equip:
                    equip.x = self.owner.x
                    equip.y = self.owner.y



    @property
    def skill_level_sum(self):
        """装備スロットをループしてskill levelの合計を返す"""

        bonus = {}
        for parts in self.item_slot.values():  # crisiumが入る
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

            if self.owner.fighter.skill_list:
                # 装備変更に伴うskill check
                skill_list = self.owner.fighter.skill_list
                self.skill_equip_on(skill_list)
                self.skill_equip_off(skill_list)

            print(self.item_slot, self.equip_slot)
            print(self.owner.fighter.skill_list)

    def skill_equip_on(self, skill_list):
        """skill levelが1以上なら装備skillをslotに入れる"""
        for s in skill_list:
            if Tag.equip in s.tag and s.level > 0 and self.equip_slot[s.slot] != s:
                self.equip_slot[s.slot] = s
                self.equip_slot[s.slot].master = self.owner
                self.equip_update_check = True

    def skill_equip_off(self, skill_list):
        """skill levelが1以下なら装備解除しslotから外す"""
        for s in skill_list:
            if Tag.equip in s.tag and s.level < 1 and self.equip_slot[s.slot] == s:
                del self.equip_slot[s.slot].master
                self.equip_slot[s.slot] = None
                self.equip_update_check = True

    @property
    def states_bonus(self):
        """item_slotをループしてstates bonusを合計し返す"""

        bonus = {"max_hp": 0, "max_mp": 0, "STR": 0,
                 "DEX": 0, "INT": 0, "defense": 0, "evasion": 0}
        for parts in self.item_slot.values():
            if parts and not isinstance(parts, str) and parts.states_bonus:
                bonus = Counter(bonus) + Counter(parts.states_bonus)

        return bonus

    @property
    def melee_weapon_damage(self):
        if self.equip_slot["main_hand"]:
            return self.equip_slot["main_hand"].attack_damage
        else:
            return None

    @property
    def ranged_weapon_damage(self):
        if self.equip_slot["ranged_weapon"]:
            return self.equip_slot["ranged_weapon"].attack_damage
        else:
            return None

    @property
    def weapon_hit_rate(self):
        if self.equip_slot["main_hand"]:
            return self.equip_slot["main_hand"].hit_rate
        else:
            return None

    @property
    def ranged_hit_rate(self):
        if self.equip_slot["ranged_weapon"]:
            return self.equip_slot["ranged_weapon"].hit_rate
        else:
            return None

    def toggle_equip(self, equip_item):
        """装備アイテムの付け外しを行うメソッド
        """
        results = []

        for key, item in self.item_slot.items():
            if item == equip_item:

                del self.item_slot[key].master
                self.item_slot[key] = None
                results.append({"message": f"dequipped {item.name}"})

                self.equip_update_check = True
                return results

        for key, item in self.item_slot.items():
            if item is None:

                self.item_slot[key] = equip_item
                self.item_slot[key].master = self.owner

                results.append({"message": f"equipped {equip_item.name}"})

                self.equip_update_check = True
                return results
