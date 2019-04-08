from functools import lru_cache
from collections import Counter

from modules.puzzles.model import Building, ArtWork

BUILDING_FILE = 'data/buildings.txt'
ARTWORKS_FILE = 'data/artworks.txt'


@lru_cache()
def buildings():
    result = []
    with open(BUILDING_FILE, 'r') as f:
        for line in f.read().split('\n')[1:]:
            columns = line.split('\t')
            result.append(Building(int(columns[0]), columns[1], columns[2]))
    return result


@lru_cache()
def artworks():
    result = []
    with open(ARTWORKS_FILE, 'r') as f:
        for line in f.read().split('\n')[1:]:
            columns = line.split('\t')
            result.append(ArtWork(columns[0]))
    return result


@lru_cache()
def locations():
    return artworks() + buildings()


@lru_cache()
def building_by_number(number):
    number = int(number)
    results = [building for building in buildings() if building.number == number]
    if not results:
        return None
    return results[0]


@lru_cache()
def location_by_length(length):
    return [l for l in locations() if len(l.name) == int(length)]


@lru_cache()
def locations_containing_symbols(symbols):
    # Transform symbol list to dict, counting the occurences of all symbols
    s_dict = Counter(symbols.lower())

    ls = locations()
    for symbol in s_dict:
        ls = [l for l in ls if l.name.lower().count(symbol) >= s_dict[symbol]]
    return ls
