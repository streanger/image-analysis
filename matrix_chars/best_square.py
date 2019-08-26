from math import *
from functools import reduce
import itertools


def factor_distributions(x):
    if x <= 0:
        return 0
    i = 2
    e = floor(sqrt(x))
    r = [] #używana jest tablica (lista), nie bepośrednie wypisywanie
    while i <= e:
        if x % i == 0:
            r.append(i)
            x /= i
            e = floor(sqrt(x))
        else:
            i += 1
    if x > 1: r.append(x)
    return [int(item) for item in r]
    


def variations(data):
    '''https://stackoverflow.com/questions/40709488/all-possibilities-to-split-a-list-into-two-lists'''
    pairs = []
    dataLen = len(data)
    for pattern in itertools.product([True, False], repeat=dataLen):
        some = [int(x[1]) for x in zip(pattern, data) if x[0]]
        thing = [int(x[1]) for x in zip(pattern, data) if not x[0]]
        pair = [some, thing]
        if not all(pair):
            continue
        pairs.append(pair)

    # some way, to remove duplicates
    # https://stackoverflow.com/questions/2213923/removing-duplicates-from-a-list-of-lists
    sortedPairs = [sorted(pair) for pair in pairs]
    pairs = list(sortedPairs for sortedPairs, _ in itertools.groupby(sortedPairs))
    return pairs
    
    
def flatten(data):
    return [x for y in data for x in y]
    
    
def best_square(dim_x, dim_y, reverse=False):
    '''generate variations
       e.g. rectange 2 x 15 --> 5 x 6
    '''
    full = dim_x * dim_y
    data = factor_distributions(full)
    pairs = variations(data)
    
    # a, b stored
    # sides = [(a, b, abs(reduce((lambda x, y: x * y), a) - reduce((lambda x, y: x * y), b))) for a, b in pairs]
    
    # a, b multiplied
    sides = [(reduce((lambda x, y: x * y), a), reduce((lambda x, y: x * y), b)) for a, b in pairs]
    sides = [(a, b, abs(a - b)) for a, b in sides]
    out = sorted(sides, key=lambda x: x[2], reverse=reverse)
    return out[0][:2]
    
    
if __name__ == "__main__":
    x, y = 13908, 1
    a, b = best_square(x, y)
    print('best square from ({}, {}) is: ({}, {})'.format(x, y, a, b))
    
    
'''
INFO:
    https://pl.wikipedia.org/wiki/Wariacja_z_powtórzeniami
    https://pl.wikipedia.org/wiki/Wariacja_bez_powtórzeń
    
'''
