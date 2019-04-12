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
def location_by_length(length, ls=locations()):
    return [l for l in ls if len(l.name) == int(length)]


@lru_cache()
def locations_containing_symbols(symbols, ls=locations()):
    # Transform symbol list to dict, counting the occurences of all symbols
    s_dict = Counter(symbols.lower())
    results = set()
    for location in ls:
        # Make a list of counters of all variants
        variant_counters = [Counter(variant.lower()) for variant in location.variants]
        # Subtract these counters from s_dict, and map to the highest remainder
        variant_counters = [
            max([v - counter.get(k, 0) for k, v in s_dict.items()])
            for counter in variant_counters
        ]
        # If all values are below or equal to 0
        # this location matches on atleast one variant
        if min(variant_counters) <= 0:
            results.add(location)
    return results


@lru_cache()
def buildings_by_length(length):
    return location_by_length(length, ls=tuple(buildings()))


@lru_cache()
def buildings_containing_symbols(symbols):
    return locations_containing_symbols(symbols, ls=tuple(buildings()))
