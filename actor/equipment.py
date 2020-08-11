
class Equipment:
    """装備部位とそこからの追加bonusを返す
       装備の切り替えもここで行う
       bonusはEquippable関数で設定する
    """
    def __init__(self):
        self.item_slot = {
            "main_hand":None,
            "off_hand":None
          }


    @property
    def max_hp_bonus(self):
        bonus = 0
        for parts in self.item_slot.values():
            if parts and parts.equippable.max_hp_bonus:
                bonus += parts.equippable.max_hp_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        for parts in self.item_slot.values():
            if parts and parts.equippable.power_bonus:
                bonus += parts.equippable.power_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        for parts in self.item_slot.values():
            if parts and parts.equippable.defense_bonus:
                bonus += parts.equippable.defense_bonus

        return bonus


    def toggle_equip(self, equip_item, sprites):
        """装備アイテムの付け外しを行うメソッド
        """
        results = []

        for item_key, item in self.item_slot.items():
            if item_key == equip_item.equippable.slot:# アイテムキーと装備するスロットが同じか判定

                if item and item.name == equip_item.name:# equip_itemが装備アイテムと同じなら単に解除
                    del self.item_slot[item_key].master
                    sprites.remove(self.item_slot[item_key])

                    self.item_slot[item_key] = None
                    results.append({"message":f"dequipped {item.name}"})
                    break



                else:
                    # equip_itemが装備されてるものと別のアイテムなら装備を解除しequip_itemを装備
                    if item:
                        del self.item_slot[item_key].master
                        sprites.remove(self.item_slot[item_key])
                        self.item_slot[item_key] = None
                        
                    self.item_slot[item_key] = equip_item
                    self.item_slot[item_key].master = self.owner
                    sprites.append(equip_item)

                    results.append({"message":f"equipped {equip_item.name}"})
                    break     

        return results


