class Item:
    def __init__(self, name, *aliases, **kwargs):
        self.name = name
        self.aliases = tuple(label.lower() for label in (name,) + aliases)

        description = kwargs.get("description")

        if description is None:
            description = f"a {name}"

        idle_description = kwargs.get("idle_description")
        if idle_description is None:
            idle_description = f"There is a {name} lying on the ground."

        self.description = description  # Fully mutable member.
        self.idle_description = idle_description  # Fully mutable member.
        self.holder = None  # Fully mutable member.
        self._obtainable = kwargs.get("obtainable", True)

    def __repr__(self):
        return f"{type(self).__name__}({', '.join(repr(n) for n in self.aliases)})"

    def __str__(self):
        return self.name

    @property
    def obtainable(self):
        return self._obtainable


class Consumable(Item):
    def consume(self, consumer):
        return NotImplemented


class Book(Item):
    def read(self, actor):
        return NotImplemented
