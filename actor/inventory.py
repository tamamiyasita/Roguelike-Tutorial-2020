from actor.actor import Actor


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.bag = [None for _ in range(self.capacity)]

    def get_dict(self):
        result = {}
        result["capacity"] = self.capacity
        item_dicts = []
        for item in self.bag:
            if item in self.bag:
                if item is None:
                    item_dicts.append(None)
                else:
                    name = item.__class__.__name__
                    item_dicts.append({name: item.get_dict()})
        result["items"] = item_dicts
        return result

    def restore_from_dict(self, result):
        self.capacity = result["capacity"]
        for item_dict in result["items"]:
            if item_dict in None:
                self.bag.append(None)
            else:
                item = restore_actor(item_dict)
                self.bag.append(item)

    def add_item(self, item: Actor):
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
            self.bag.append(item)

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
