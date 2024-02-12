import math

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return round(math.ceil(n * multiplier) / multiplier)