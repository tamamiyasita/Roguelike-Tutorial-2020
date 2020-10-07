from collections import Counter
from constants import *
from actor.items.leaf_blade import LeafBlade


class Equipment:
    """装備部位とそこからの追加bonusを返す
       装備の切り替えもここで行う
       bonusはEquippable関数で設定する
    """

    def __init__(self):
        """アイテムスロット、及び装備するタイミングを決めるequip_update_check
        """
        self.item_slot = {
            "head": None,
            "main_hand": None,
            "off_hand": None,
            "ranged_weapon": None,
        }

        # 装備変更によるスプライト更新のチェックに使う変数
        self.equip_update_check = False

    def get_dict(self):
        result = {}
        for item_key, item in self.item_slot.items():
            if item is None:
                result[item_key] = None
            else:
                result[item_key] = item.name

        return result

    def restore_from_dict(self, result):
        self.item_slot = result
        for item in self.owner.inventory.item_bag:
            if item and item.name in self.item_slot.values():
                self.item_slot[item.slot] = item
                item.master = self.owner
                self.equip_update_check = True

    @property
    def skill_level_sum(self):
        """スキルボーナスの計算"""

        bonus = {}
        for parts in self.item_slot.values():# crisiumが入る
            if parts and parts.skill_add:# crisiumのskill_add{leaf_blade:1}が入る
                bonus = Counter(bonus) + Counter(parts.skill_add)
                # if bonus is None:
                #     bonus = 0
        print(bonus, "bonus sum")
        return bonus # {leaf_blade:1}

    def update(self, sprites):
        """装備スプライトの表示はここで行う"""
        if self.equip_update_check:

            # 遠隔武器以外がスロットに入っていたら装備スプライトをスプライトリストに入れて表示する
            for item in self.item_slot.values():
                if item and item not in sprites and not item.slot == "ranged_weapon":
                    sprites.append(item)

            # 装備解除しスプライトがスロットから無くなればスプライトリストからも削除
            for sprite in sprites:
                if sprite not in self.item_slot.values():
                    sprites.remove(sprite)


            # 装備更新完了通知
            self.equip_update_check = False

            if self.owner.fighter.skill_list:
                skill_list = self.owner.fighter.skill_list
                self.skill_equip_on(skill_list)
                self.skill_equip_off(skill_list)
            print(self.item_slot)
            print(self.owner.fighter.skill_list)

    def skill_equip_on(self, skill_list):
        for s in skill_list:
            if Tag.equip in s.tag and s.level > 0 and self.item_slot[s.slot] != s:
                self.item_slot[s.slot] = s
                self.item_slot[s.slot].master = self.owner
                self.equip_update_check = True

    def skill_equip_off(self, skill_list):
        for s in skill_list:
            if Tag.equip in s.tag and s.level < 1 and self.item_slot[s.slot] == s:
                del self.item_slot[s.slot].master
                self.item_slot[s.slot] = None
                self.equip_update_check = True

                



    @property
    def states_bonus(self):
        """ステータスボーナスの計算"""

        bonus = {"max_hp": 0, "max_mp": 0, "str": 0,
                 "dex": 0, "int": 0, "defense": 0, "evasion": 0}
        for parts in self.item_slot.values():
            if parts and parts.states_bonus:
                bonus = Counter(bonus) + Counter(parts.states_bonus)

        return bonus

    @property
    def melee_weapon_damage(self):
        if self.item_slot["main_hand"]:
            return self.item_slot["main_hand"].attack_damage
        else:
            return None

    @property
    def ranged_weapon_damage(self):
        if self.item_slot["ranged_weapon"]:
            return self.item_slot["ranged_weapon"].attack_damage
        else:
            return None

    @property
    def weapon_hit_rate(self):
        if self.item_slot["main_hand"]:
            return self.item_slot["main_hand"].hit_rate
        else:
            return None

    @property
    def ranged_hit_rate(self):
        if self.item_slot["ranged_weapon"]:
            return self.item_slot["ranged_weapon"].hit_rate
        else:
            return None

    def toggle_equip(self, equip_item, sprites):
        """装備アイテムの付け外しを行うメソッド
        """
        results = []

        for item_key, item in self.item_slot.items():
            if item_key == equip_item.slot:  # アイテムキーと装備するスロットが同じか判定

                if item and item.name == equip_item.name:  # equip_itemが装備アイテムと同じなら単に解除
                    del self.item_slot[item_key].master

                    self.item_slot[item_key] = None
                    results.append({"message": f"dequipped {item.name}"})
                    break

                else:
                    # equip_itemが装備されてるものと別のアイテムなら装備を解除しequip_itemを装備
                    if item:
                        del self.item_slot[item_key].master
                        self.item_slot[item_key] = None

                    self.item_slot[item_key] = equip_item
                    self.item_slot[item_key].master = self.owner

                    results.append({"message": f"equipped {equip_item.name}"})
                    break

        self.equip_update_check = True

        return results

    def plus_skill_point(self, item):
        if hasattr(item, "skill_add"):
            for skill, level in item.skill_add.items():
                if skill in self.owner.fighter.skills:
                    self.owner.fighter.skills[skill].level += level

            for skill in self.owner.fighter.skills.values():
                if Tag.equip in skill.tag and Tag.skill in skill.tag and skill.level > 0:
                    self.toggle_equip(skill, None)
                    # self.item_slot[skill.slot] = skill
                    # self.item_slot[skill.slot].master = self.owner

    def minus_skill_point(self, item):
        if hasattr(item, "skill_add"):
            for skill, level in item.skill_add.items():
                if skill in self.owner.fighter.skills:
                    self.owner.fighter.skills[skill].level -= level

            for skill in self.owner.fighter.skills.values():
                if Tag.equip in skill.tag and Tag.skill in skill.tag and skill.level < 1:
                    self.toggle_equip(skill, None)
                    # del self.item_slot[skill.slot].master
                    # self.item_slot[skill.slot] = None

            # スキルにより装備を実体化する
            #     print(skill, "skill")
                    # self.toggle_equip(equip, None)
