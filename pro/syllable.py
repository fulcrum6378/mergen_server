import copy
import numpy as np

import pro.consonant.main as con
import pro.func as fun
import pro.vowel.main as vow

stress = "'"
prolong = ":"


def main(text):
    syllables = np.array([])
    s = Syllable()
    rollBack = 0
    for c in range(0, len(text)):
        if rollBack > 0:
            rollBack -= 1
            continue

        conFound = findCons(text[c:])
        isCon = conFound[0]
        rollBack = conFound[1]
        ch = text[c]
        isVow = fun.findEnum(vow.Vowel, ch)

        if isCon is not None:
            if len(s.vows) == 0:
                s.addBCon(isCon)
            elif upcomingVowel(text[c:], rollBack):
                syllables = np.append(syllables, [copy.deepcopy(s)])
                s = Syllable()
                s.addBCon(isCon)
                continue
            else:
                s.addACon(isCon)
        elif isVow is not None:
            s.addVow(isVow)
        elif ch == prolong:
            s.prolong = True
        elif ch == stress:
            s.stressed = True
        elif ch == " ":
            s.space += 1
            if len(text) < (c + 1) or text[c + 1] != " ":
                syllables = np.append(syllables, [copy.deepcopy(s)])
                s = Syllable()
        else:
            raise Exception("Unknown IPA character: " + text[c:])
    # for loop ends here

    if len(s.vows) > 0:
        syllables = np.append(syllables, [s])
    # print([sy.__dict__ for sy in syllables])
    return syllables


def findCons(text):
    ch = text[0]
    isCon = fun.findEnum(con.Consonant, ch)
    rollBack = 0
    if len(text) > 2:
        if ch == 't' and text[1] == '͡' and text[2] == 'ʃ':
            isCon = con.Consonant.VOICELESS_PALATO_ALVEOLAR_AFFRICATE
            rollBack += 2
        if ch == 'd' and text[1] == '͡' and text[2] == 'ʒ':
            isCon = con.Consonant.VOICED_POSTALVEOLAR_AFFRICATE
            rollBack += 2
    if len(text) > 1:
        if ch == 'k' and text[1] == 'ʼ':
            isCon = con.Consonant.VELAR_EJECTIVE_PLOSIVE
            rollBack += 1
    return [isCon, rollBack]


def upcomingVowel(text, roll):
    return len(text) > (1 + roll) and fun.findEnum(vow.Vowel, text[1 + roll]) is not None


class Syllable:
    def __init__(self):
        self.stressed = False
        self.bCons = []
        self.vows = []
        self.aCons = []
        self.prolong = False
        self.space = 0

    def addBCon(self, consonant):
        self.bCons.append(consonant)

    def addVow(self, vowel):
        self.vows.append(vowel)

    def addACon(self, consonant):
        self.aCons.append(consonant)

    def compose(self):
        data = np.array([])
        for bc in self.bCons:
            data = np.concatenate((data, con.compose(bc, True)))
        mul = 2  # too much of this bitch makes an echo sound
        if self.stressed: mul *= 1.25
        for vv in self.vows:
            for d in range(0, 15):
                data = np.concatenate((data, vow.tremble(vv, mul)))
                if mul > 1: mul -= 0.25
                if mul < 1: mul = 1
        for ac in self.aCons:
            data = np.concatenate((data, con.compose(ac, False)))
        for spc in range(0, self.space):
            spacer = np.array([])
            for mut in range(0, 2500): spacer = np.append(spacer, 0)
            data = np.concatenate((data, spacer))
        return data
