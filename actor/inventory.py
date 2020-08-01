# from actor.actor import Actor
from actor.restore_actor import restore_actor
from actor.equipment import Equipment

class Inventory:
    def __init__(self, capacity=5):
        self.bag = []
        self.capacity = capacity
        self.on_equip_name = {"main_hand":None, "off_hand":None}

        self.bag = [None for _ in range(self.capacity)]

    def get_dict(self):
        result = {}
        result["capacity"] = self.capacity
        result["on_equip_name"] = self.on_equip_name
        item_dicts = []
        for item in self.bag:
            if item is None:
                item_dicts.append(None)
            else:
                name = item.__class__.__name__
                item_dicts.append({name: item.get_dict()})
        result["items"] = item_dicts
        print(item_dicts, "item_dicts")
        return result

    def restore_from_dict(self, result):
        self.capacity = result["capacity"]
        self.on_equip_name = result["on_equip_name"]
        for  i, item_dict in enumerate(result["items"]):
            if item_dict is None:
                self.bag[i] = None
            else:
                item = restore_actor(item_dict)
                self.bag[i] = item
                if item.name in self.on_equip_name.values():
                    self.owner.equipment.toggle_equip(item)
            print(self.bag, "rest")
                

    def add_item(self, item):
        results = []

        item_placed = False
        for i in range(self.capacity):
            if self.bag[i] is None:
                self.bag[i] = item
                item_placed = True
                break

        if not item_placed:
            results.append(
                {"message": "You cannot carry any more, your inventory is full"}
            )
        else:
            results.append(
                {"message": f"You pick up the {item.name}!"}
            )
            item.remove_from_sprite_lists()

        return results

    def get_item_number(self, item_number: int):
        return self.bag[item_number]

    def remove_item_number(self, item_number: int):
        results = []
        self.bag[item_number] = None
        return results

    def remove_item(self, item: int):
        results = []
        for i in range(self.capacity):
            if self.bag[i] is item:
                self.bag[i] = None
        return results
