import pro.func as fun
import numpy as np


def main(before):
    raw = np.array(fun.openJson('alveolar_nasal', 'consonant'))
    for r in range(0, len(raw)): raw[r] = raw[r] * 1.25
    if before:
        return raw[3000:]
    else:
        return raw[:-500]
