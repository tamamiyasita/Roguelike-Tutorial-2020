from actor.equip import EquipmentSlots

class Equipment:
    def __init__(self, main_hand=None, off_hand=None):
        self.main_hand = main_hand
        self.off_hand = off_hand

    @property
    def max_hp_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.power_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.power_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defense_bonus

        return bonus

    def toggle_equip(self, equippable_item):
        """装備アイテムの付け外しを行うメソッド
        """
        results = []

        item_slot = equippable_item.equippable.slot

        if item_slot == EquipmentSlots.MAIN_HAND:

            if self.main_hand == equippable_item:
                # メインハンドにequippable_itemが装備されてたら解除
                self.main_hand = None
                results.append({"dequipped": equippable_item})
            else:
                # equippable_itemがメインハンドと別のアイテムなら装備を解除しequippable_itemを装備
                if self.main_hand:
                    results.append({"dequipped": self.main_hand})
                
                self.main_hand = equippable_item
                results.append({"equipped": equippable_item})     

        elif item_slot == EquipmentSlots.OFF_HAND:

            if self.off_hand == equippable_item:
                # オフハンドにequippable_itemが装備されてたら解除
                self.off_hand = None
                results.append({"dequipped": equippable_item})
            else:
                # equippable_itemがオフハンドと別のアイテムなら装備を解除しequippable_itemを装備
                if self.off_hand:
                    results.append({"dequipped": self.off_hand})
                
                self.off_hand = equippable_item
                results.append({"equipped": equippable_item})

        return results

        


