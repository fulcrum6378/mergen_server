import pro.func as fun
import numpy as np


def main(before):
    raw = np.array(fun.openJson('voiced_alveolar_plosive', 'consonant'))
    if before:
        for r in range(0, len(raw)): raw[r] = raw[r] * 2
        return raw[300:-2000]
    else:
        for r in range(0, len(raw)): raw[r] = raw[r] * 0.6
        return raw[1000:]
