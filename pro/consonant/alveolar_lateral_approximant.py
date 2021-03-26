import pro.func as fun
import numpy as np


def main(before):
    raw = np.array(fun.openJson('alveolar_lateral_approximant', 'consonant'))
    for r in range(0, len(raw)): raw[r] = raw[r] * 1.5
    if before:
        return raw
    else:
        return raw[:-500]
