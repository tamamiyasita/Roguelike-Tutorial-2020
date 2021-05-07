from actor.restore_actor import restore_actor


class Inventory:
    def __init__(self, capacity=5):
        self.item_bag = []
        self.capacity = capacity
        self.item_bag = [None for _ in range(self.capacity)]

    def get_dict(self):
        result = {}
        result["capacity"] = self.capacity
        item_dicts = []
        for item in self.item_bag:
            if item is None:
                item_dicts.append(None)
            else:
                name = item.__class__.__name__
                item_dicts.append({name: item.get_dict()})
        result["item_bag"] = item_dicts
        return result

    def restore_from_dict(self, result):
        self.capacity = result["capacity"]
        self.item_bag = [None for _ in range(self.capacity)]
        for i, item_dict in enumerate(result["item_bag"]):
            if item_dict is None:
                self.item_bag[i] = None
            else:
                item = restore_actor(item_dict)
                self.item_bag[i] = item
                print(self.item_bag, "rest")

    def add_item(self, item, engine):
        results = []

        item_placed = False
        for i in range(self.capacity):
            if self.item_bag[i] is None:
                self.item_bag[i] = item
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
        if item_number <= self.capacity:
            return self.item_bag[item_number]

    def remove_item_number(self, item_number: int):
        results = []
        self.item_bag[item_number] = None
        return results

    def remove_item(self, item: int):
        results = []
        for i in range(self.capacity):
            if self.item_bag[i] is item:
                self.item_bag[i] = None
        return results
