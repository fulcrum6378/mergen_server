import numpy as np

import pro.func as fun
import pro.syllable as syl


def main(text):
    data = np.array([])
    for s in syl.main(text.strip()):
        data = np.concatenate((data, s.compose()))
    fun.arrayToAudio(data, 'output', 1)
    return 'output'
