class Item:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if type(other) == type(self):
            return self.name == other.name
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Item: {self.name}>"

    def __contains__(self, x):
        return x in self.name.lower()

    def __len__(self):
        return len(self.name)

    def __hash__(self):
        return hash(self.name)


class Building(Item):

    def __init__(self, number, name, abbreviation):
        super().__init__(name)
        self.number = number
        self.abbreviation = abbreviation

    def __eq__(self, other):
        if type(other) == type(self):
            return self.number == other.number
        if type(other) == int:
            return self.number == other
        if type(other) == str:
            return self.name == other or self.abbreviation == other
        return False

    def __repr__(self):
        return f"<Building: {self.number} - {self.name} ({self.abbreviation})>"

    def __hash__(self):
        return hash(self.name)


class ArtWork(Item):
    def __repr__(self):
        return f"<Artwork: {self.name}>"
