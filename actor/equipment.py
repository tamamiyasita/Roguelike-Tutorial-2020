from pyglet.gl import current_context
from actor.equip import EquipmentSlots

class Equipment:
    """装備部位とそこからの追加bonusを返す
       装備の切り替えもここで行う
       bonusはEquippable関数で設定する
    """
    def __getattr__(self, main_hand=None, off_hand=None):
        self.item_slot = self.owner.inventory.equip_slots
        self.main_hand = self.item_slot["main_hand"]
        self.off_hand = self.item_slot["off_hand"]


    @property
    # 部位をリストにして返す
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


    def toggle_equip(self, equip_item):
        """装備アイテムの付け外しを行うメソッド
        """
        results = []

        for item_key, item in self.item_slot.items():
            if item and item.name == equip_item.name:
                del self.item_slot[item_key].owner_ship
                self.item_slot[item_key] = None
                results.append({"dequipped"})
                break



            else:
                # equippable_itemがメインハンドと別のアイテムなら装備を解除しequippable_itemを装備
                if item:
                    self.item_slot[item_key] = None
                    del self.item_slot[item_key].owner_ship
                    self.main_hand = None
                    
                self.item_slot[item_key] = equip_item
                self.item_slot[item_key].owner_ship = self.owner

                results.append({"equipped": equip_item})
                break     

        # elif item_slot == EquipmentSlots.OFF_HAND:

        #     if self.off_hand == equip_item:
        #         # オフハンドにequippable_itemが装備されてたら解除
        #         del self.off_hand.owner_ship
        #         equip_sprites.remove(equip_item)
        #         self.off_hand = None
        #         results.append({"dequipped": equip_item})
        #     else:
        #         # equippable_itemがオフハンドと別のアイテムなら装備を解除しequippable_itemを装備
        #         if self.off_hand:
        #             del self.off_hand.owner_ship
        #             equip_sprites.remove(self.off_hand)
        #             self.off_hand = None
                
        #         self.off_hand = equip_item
        #         self.off_hand.owner_ship = self.owner
        #         equip_sprites.append(equip_item)

        #         results.append({"equipped": equip_item})   


        return results


