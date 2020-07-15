from actor.actor import Actor


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.bag = [None for _ in range(self.capacity)]

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
