from actor.equip import EquipmentSlots

class Equipment:
    """装備部位とそこからの追加bonusを返す
       bonusはEquippable関数で設定する
    """
    def __init__(self, main_hand=None, off_hand=None):
        self.main_hand = main_hand
        self.off_hand = off_hand


    def get_dict(self):
        result = {}
        result["main_hand"] = self.main_hand.get_dict()
        result["off_hand"] = self.off_hand.get_dict()

        return result

    def restore_from_dict(self, result):
        self.main_hand = result["main_hand"]
        # self.off_hand = result["off_hand"]

    @property
    # 現在の部位の状態を返す
    def body_equip(self):
        return [self.main_hand, self.off_hand]


    @property
    def max_hp_bonus(self):
        bonus = 0

        for parts in self.body_equip:
            if parts and parts.equippable:
                bonus += parts.equippable.max_hp_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        for parts in self.body_equip:
            if parts and parts.equippable:
                bonus += parts.equippable.power_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        for parts in self.body_equip:
            if parts and parts.equippable:
                bonus += parts.equippable.defense_bonus

        return bonus


    def toggle_equip(self, equip_item, equip_sprites=None):
        """装備アイテムの付け外しを行うメソッド
        """
        results = []

        item_slot = equip_item.equippable.slot

        if item_slot == EquipmentSlots.MAIN_HAND:

            if self.main_hand == equip_item:
                # メインハンドにequippable_itemが装備されてたら解除
                del self.main_hand.owner_ship
                equip_sprites.remove(equip_item)
                self.main_hand = None
                results.append({"dequipped": equip_item})
            else:
                # equippable_itemがメインハンドと別のアイテムなら装備を解除しequippable_itemを装備
                if self.main_hand:
                    del self.main_hand.owner_ship
                    equip_sprites.remove(self.main_hand)
                    self.main_hand = None
                
                self.main_hand = equip_item
                self.main_hand.owner_ship = self.owner
                equip_sprites.append(equip_item)

                results.append({"equipped": equip_item})     

        elif item_slot == EquipmentSlots.OFF_HAND:

            if self.off_hand == equip_item:
                # オフハンドにequippable_itemが装備されてたら解除
                del self.off_hand.owner_ship
                equip_sprites.remove(equip_item)
                self.off_hand = None
                results.append({"dequipped": equip_item})
            else:
                # equippable_itemがオフハンドと別のアイテムなら装備を解除しequippable_itemを装備
                if self.off_hand:
                    del self.off_hand.owner_ship
                    equip_sprites.remove(self.off_hand)
                    self.off_hand = None
                
                self.off_hand = equip_item
                self.off_hand.owner_ship = self.owner
                equip_sprites.append(equip_item)

                results.append({"equipped": equip_item})   


        return results


