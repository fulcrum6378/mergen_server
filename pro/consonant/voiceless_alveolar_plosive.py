import pro.func as fun
import numpy as np


def main(before):
    raw = np.array(fun.openJson('voiceless_alveolar_plosive', 'consonant'))
    for r in range(0, len(raw)): raw[r] = raw[r] * 2.1
    if before: return raw[:-2500]
    else: return raw[1000:]
