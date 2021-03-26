import pro.func as fun
import numpy as np


def main():
    raw = fun.openJson('voiced_labiodental_fricative', 'consonant')
    data = np.array([raw, raw])
    return data.flatten()
