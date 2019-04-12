import unicodedata


class Item:
    def __init__(self, name, variants=[]):
        self.name = name
        self.variants = Item._generate_variants(variants + [name])

    def __eq__(self, other):
        if type(other) == type(self):
            return self.name == other.name
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Item: {self.name}>"

    def __contains__(self, x):
        return True in [x.lower() in variant.lower() for variant in self.variants]

    def __len__(self):
        return len(self.name)

    def __hash__(self):
        return hash(self.name)

    @staticmethod
    def _generate_variants(names):
        results = set()
        # Remove special unicode characters
        for name in names:
            canonical = unicodedata.normalize('NFD', name)\
                .encode('ascii', 'ignore')\
                .decode('utf-8')

            results.add(canonical)

        # Remove spaces
        for name in list(results):
            results.add(name.replace(' ', ''))

        # Remove the/de/het
        for name in list(results):
            results.add(name.replace('the', '').replace('de', '').replace('het', ''))

        return frozenset(results)


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
