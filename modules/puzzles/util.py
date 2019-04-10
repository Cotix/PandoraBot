from functools import lru_cache
from collections import Counter
from itertools import chain, permutations

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

    for symbol in s_dict:
        ls = [l for l in ls if l.name.lower().replace('ë','e').replace('é','e').count(symbol) >= s_dict[symbol]]

    return remove_duplicate_locations(ls)


@lru_cache()
def buildings_by_length(length):
    return location_by_length(length, ls=tuple(buildings()))


@lru_cache()
def buildings_containing_symbols(symbols):
    return locations_containing_symbols(symbols, ls=tuple(buildings()))


def remove_duplicate_locations(locations):
    results = []
    storedLocations = []
    for l in locations:
        # Normalize name by removing spaces and putting it in lowercase
        normalizedL = l.name.replace(' ', '').lower()
        if normalizedL not in storedLocations:
            results.append(l)
            storedLocations.append(normalizedL)
    return results


@lru_cache()
def brute_force_coordinates(digits):
    # Perform a coarse filter on the digits to check if they can possibly form valid coordinates
    if (not(digits.count('5') >= 1 and digits.count('2') >= 2 and digits.count('6') >= 1 and digits.count('8') >= 1)):
        return []

    # Remove predetermined digits
    digits = digits.replace('5', '', 1).replace('2', '', 2).replace('6', '', 1).replace('8', '', 1)
    digits_perms = [''.join(x) for x in list(map(list, permutations(digits, 6)))]
    # Coordinate strings have the form '52.2xxx,6.8yyy'
    coor_strings = []
    for digits_perm in digits_perms:
        lat_digits = digits_perm[:3]
        long_digits = digits_perm[3:]
        coor_strings.append('52.2' + lat_digits + ',6.8' + long_digits)

    return [x for x in coor_strings if is_on_campus(x)]


@lru_cache()
# Campus area is approximated by a square
# coordinate_string has the form '52.2xxx,6.8yyy'
def is_on_campus(coordinate_string):
    coordinates = coordinate_string.split(',')
    latitude = coordinates[0]
    longitude = coordinates[1]
    return 52.2336 < float(latitude) < 52.2524 and 6.84246 < float(longitude) < 6.86630
