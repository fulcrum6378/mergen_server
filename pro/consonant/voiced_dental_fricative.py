import pro.func as fun
import numpy as np


def main():
    raw = fun.openJson('voiced_dental_fricative', 'consonant')
    return np.array(raw)
