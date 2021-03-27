import logging

from whimsylib.globals import G
from whimsylib import say


class Bag(set):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._alias_dict = {}
        for item in self:
            self._add_aliases(item)

    def __contains__(self, v):
        """Return True if an Item is present in the bag.
        If v is a str, then find the item by name, otherwise find the item by
        identity.
        """
        if isinstance(v, str):
            return bool(self.find(v))
        else:
            return super().__contains__(v)

    def _add_aliases(self, item, message=None):
        for alias in item.aliases:
            self._alias_dict.setdefault(alias.lower(), set()).add(item)

        item.holder = self
        if self is G.player.inventory:
            message = message or f"You acquire {item.name}."
        if message is not None:
            say.insayne(message)

    def _discard_aliases(self, item, message=None):
        for alias in item.aliases:
            item_set = self._alias_dict.get(alias.lower(), set())
            item_set.discard(item)
            if not item_set and alias in self._alias_dict:
                del self._alias_dict[alias]

        item.holder = None
        if self is G.player.inventory:
            message = message or f"You lose possession of {item.name}."
        if message is not None:
            say.insayne(message)

    def add(self, item, message=None):
        super().add(item)
        self._add_aliases(item, message)

    def find(self, name):
        """Find an object in the bag by name, but do not remove it.
        Return None if the name does not match.

        If more than one object with the same name exists, returns one of them.
        """
        name = name.lower()
        for element in self._alias_dict.get(name, []):
            return element

    def remove(self, item, message=None):
        super().remove(item)
        self._discard_aliases(item, message)

    def clear(self):
        super().clear()
        self._alias_dict.clear()

    def copy(self):
        result = Bag(super().copy())
        result._alias_dict = self._alias_dict.copy()
        return result

    def difference(self, other_bag):
        return Bag(super().difference(other_bag))

    def difference_update(self, other_bag):
        for element in other_bag:
            self.discard(element)

    def discard(self, item):
        super().discard(item)
        self._discard_aliases(item)

    def intersection(self, other_bag):
        return Bag(super().intersection(other_bag))

    def intersection_update(self, other_bag):
        for element in other_bag:
            self.add(element)

    def pop(self):
        result = super().pop()
        self._discard_aliases(result)
        return result

    def symmetric_difference(self, other_bag):
        return Bag(super().symmetric_difference(other_bag))

    def symmetric_difference_update(self, other_bag):
        diff = super().symmetric_difference(other_bag)
        for element in self:
            if element not in diff:
                self.remove(element)
        for element in diff:
            if element not in self:
                self.add(element)

    def union(self, other_bag):
        return Bag(super().union(other_bag))

    def update(self, elements):
        for element in elements:
            self.add(element)

    def items_by_name(self):
        """Convenience function mapping item names to item lists.

        This is the preferred way to get a name-to-item(s) mapping for a Bag.
        Naive attempts to do so may result in abstruse bugs when multiple items
        have the same name.
        """
        items = {}
        for item in self:
            items.setdefault(item.name, []).append(item)
        return items
