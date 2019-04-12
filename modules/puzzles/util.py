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


def brute_force_coordinates(digits_list):
    # Add token to seperate latitude and longitude later
    digits_list.append(',')


    perms = [''.join(x) for x in list(map(list, permutations(digits_list, len(digits_list))))]
    perms = permutations(digits_list, len(digits_list))

    coordinates_list = []
    for perm in perms:
        perm_string = ''.join([x for x in perm])

        lat, lon = perm_string.split(',')
        # Coarse filter
        if lat.startswith('522') and lon.startswith('68') and len(lat) >= 6 and len(lon) >= 5:
            # Add decimal point, cut off excess significance and convert to float
            lat = float(lat[:2] + '.' + lat[2:6])
            lon = float(lon[:1] + '.' + lon[1:5])

            if is_on_campus(lat, lon):
                similar_coordinates = [x for x in coordinates_list if abs(x[0]-lat) < 0.0003 and abs(x[1]-lon) < 0.0003]
                if not similar_coordinates:
                    coordinates_list.append((lat, lon))

    return coordinates_list


@lru_cache()
# Campus area is approximated by a square
def is_on_campus(latitude, longitude):
    return 52.2336 < latitude < 52.2524 and 6.84246 < longitude < 6.86630
