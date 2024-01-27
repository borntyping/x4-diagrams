import itertools

from x4.colours import Palette
from x4_data.economy import WARES

stats = {color: len(list(group)) for color, group in itertools.groupby(WARES, key=lambda w: w.colour)}


for color in Palette:
    count = stats.get(color, 0)
    print(f"{color.name:<10} {count:2} {count * '█'}")
