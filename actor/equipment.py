from collections import Counter


class Equipment:
    """装備部位とそこからの追加bonusを返す
       装備の切り替えもここで行う
       bonusはEquippable関数で設定する
    """

    def __init__(self):
        """アイテムスロット、及び装備するタイミングを決めるequip_update_check
        """
        self.item_slot = {
            "main_hand": None,
            "off_hand": None,
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

    def update(self, sprites):
        """装備スプライトの表示はここで行う"""
        if self.equip_update_check:

            for item in self.item_slot.values():
                if item and item not in sprites:
                    sprites.append(item)
            for sprite in sprites:
                if sprite not in self.item_slot.values():
                    sprites.remove(sprite)

            self.equip_update_check = False

    @property
    def states_bonus(self):
        """ステータスボーナスの計算"""

        bonus = {"max_hp": 0, "power": 0, "defense": 0}
        for parts in self.item_slot.values():
            if parts and parts.states_bonus:
                bonus = Counter(bonus) + Counter(parts.states_bonus)

        return bonus

    @property
    def main_weapon(self):
        if self.item_slot["main_hand"]:
            return self.item_slot["main_hand"].attack_damage
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
                    # sprites.remove(self.item_slot[item_key])

                    self.item_slot[item_key] = None
                    results.append({"message": f"dequipped {item.name}"})
                    break

                else:
                    # equip_itemが装備されてるものと別のアイテムなら装備を解除しequip_itemを装備
                    if item:
                        del self.item_slot[item_key].master
                        # sprites.remove(self.item_slot[item_key])
                        self.item_slot[item_key] = None

                    self.item_slot[item_key] = equip_item
                    self.item_slot[item_key].master = self.owner
                    # sprites.append(equip_item)

                    results.append({"message": f"equipped {equip_item.name}"})
                    break

        self.equip_update_check = True

        return results
