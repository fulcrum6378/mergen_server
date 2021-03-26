from enum import Enum, unique
import numpy as np

import pro.vowel.close_back_rounded as close_back_rounded
import pro.vowel.close_front_unrounded as close_front_unrounded
import pro.vowel.near_open_front_unrounded as near_open_front_unrounded
import pro.vowel.open_front_unrounded as open_front_unrounded
import pro.vowel.open_mid_back_rounded as open_mid_back_rounded


@unique
class Vowel(Enum):
    CLOSE_BACK_ROUNDED = "u"
    CLOSE_FRONT_UNROUNDED = "i"
    OPEN_FRONT_UNROUNDED = "a"
    OPEN_MID_BACK_ROUNDED = "ɔ"
    NEAR_OPEN_FRONT_UNROUNDED = "æ"


def tremble(vow, multiply):
    data = np.array([])
    for i in range(0, 500):  # unchangeable
        if vow == Vowel.OPEN_FRONT_UNROUNDED:
            myFun = lambda: open_front_unrounded.main(i)
        elif vow == Vowel.NEAR_OPEN_FRONT_UNROUNDED:
            myFun = lambda: near_open_front_unrounded.main(i)
        elif vow == Vowel.CLOSE_FRONT_UNROUNDED:
            myFun = lambda: close_front_unrounded.main(i)
        elif vow == Vowel.OPEN_MID_BACK_ROUNDED:
            myFun = lambda: open_mid_back_rounded.main(i)
        elif vow == Vowel.CLOSE_BACK_ROUNDED:
            myFun = lambda: close_back_rounded.main(i)
        else:
            return None
        data = np.append(data, myFun() * multiply)
    return data
