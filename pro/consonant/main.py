from enum import Enum, unique
import numpy as np

import pro.consonant.alveolar_approximant as alveolar_approximant
import pro.consonant.alveolar_nasal as alveolar_nasal
import pro.consonant.alveolar_lateral_approximant as alveolar_lateral_approximant
import pro.consonant.bilabial_nasal as bilabial_nasal
import pro.consonant.velar_ejective_plosive as velar_ejective_plosive
import pro.consonant.voiced_alveolar_fricative as voiced_alveolar_fricative
import pro.consonant.voiced_alveolar_plosive as voiced_alveolar_plosive
import pro.consonant.voiced_dental_fricative as voiced_dental_fricative
import pro.consonant.voiced_labiodental_fricative as voiced_labiodental_fricative
import pro.consonant.voiced_postalveolar_affricate as voiced_postalveolar_affricate
import pro.consonant.voiced_postalveolar_fricative as voiced_postalveolar_fricative
import pro.consonant.voiced_uvular_fricative as voiced_uvular_fricative
import pro.consonant.voiceless_alveolar_fricative as voiceless_alveolar_fricative
import pro.consonant.voiceless_alveolar_plosive as voiceless_alveolar_plosive
import pro.consonant.voiceless_dental_fricative as voiceless_dental_fricative
import pro.consonant.voiceless_glottal_fricative as voiceless_glottal_fricative
import pro.consonant.voiceless_labiodental_fricative as voiceless_labiodental_fricative
import pro.consonant.voiceless_palato_alveolar_affricate as voiceless_palato_alveolar_affricate
import pro.consonant.voiceless_postalveolar_fricative as voiceless_postalveolar_fricative
import pro.consonant.voiceless_velar_plosive as voiceless_velar_plosive


@unique
class Consonant(Enum):  # auto()  # auto-generates numbers for items
    ALVEOLAR_APPROXIMANT = "ɹ"
    ALVEOLAR_NASAL = "n"
    ALVEOLAR_LATERAL_APPROXIMANT = "l"
    BILABIAL_NASAL = "m"
    VELAR_EJECTIVE_PLOSIVE = "kʼ"
    VOICED_ALVEOLAR_FRICATIVE = "z"
    VOICED_ALVEOLAR_PLOSIVE = "d"
    VOICED_DENTAL_FRICATIVE = "ð"
    VOICED_LABIODENTAL_FRICATIVE = "v"
    VOICED_POSTALVEOLAR_AFFRICATE = "d͡ʒ"
    VOICED_POSTALVEOLAR_FRICATIVE = "ʒ"
    VOICED_UVULAR_FRICATIVE = "ʁ"
    VOICELESS_ALVEOLAR_FRICATIVE = "s"
    VOICELESS_ALVEOLAR_PLOSIVE = "t"
    VOICELESS_DENTAL_FRICATIVE = "θ"
    VOICELESS_GLOTTAL_FRICATIVE = "h"
    VOICELESS_LABIODENTAL_FRICATIVE = "f"
    VOICELESS_PALATO_ALVEOLAR_AFFRICATE = "t͡ʃ"
    VOICELESS_POSTALVEOLAR_FRICATIVE = "ʃ"
    VOICELESS_VELAR_PLOSIVE = "k"


def compose(con, before):
    if con == Consonant.ALVEOLAR_APPROXIMANT:
        return alveolar_approximant.main()
    if con == Consonant.ALVEOLAR_NASAL:
        return alveolar_nasal.main(before)
    if con == Consonant.ALVEOLAR_LATERAL_APPROXIMANT:
        return alveolar_lateral_approximant.main(before)
    if con == Consonant.BILABIAL_NASAL:
        return bilabial_nasal.main()
    if con == Consonant.VELAR_EJECTIVE_PLOSIVE:
        return velar_ejective_plosive.main()
    if con == Consonant.VOICED_ALVEOLAR_FRICATIVE:
        return voiced_alveolar_fricative.main()
    if con == Consonant.VOICED_ALVEOLAR_PLOSIVE:
        return voiced_alveolar_plosive.main(before)
    if con == Consonant.VOICED_DENTAL_FRICATIVE:
        return voiced_dental_fricative.main()
    if con == Consonant.VOICED_LABIODENTAL_FRICATIVE:
        return voiced_labiodental_fricative.main()
    if con == Consonant.VOICED_POSTALVEOLAR_AFFRICATE:
        return voiced_postalveolar_affricate.main()
    if con == Consonant.VOICED_POSTALVEOLAR_FRICATIVE:
        return voiced_postalveolar_fricative.main()
    if con == Consonant.VOICED_UVULAR_FRICATIVE:
        return voiced_uvular_fricative.main()
    if con == Consonant.VOICELESS_ALVEOLAR_FRICATIVE:
        return voiceless_alveolar_fricative.main()
    if con == Consonant.VOICELESS_ALVEOLAR_PLOSIVE:
        return voiceless_alveolar_plosive.main(before)
    if con == Consonant.VOICELESS_DENTAL_FRICATIVE:
        return voiceless_dental_fricative.main()
    if con == Consonant.VOICELESS_GLOTTAL_FRICATIVE:
        return voiceless_glottal_fricative.main()
    if con == Consonant.VOICELESS_LABIODENTAL_FRICATIVE:
        return voiceless_labiodental_fricative.main()
    if con == Consonant.VOICELESS_PALATO_ALVEOLAR_AFFRICATE:
        return voiceless_palato_alveolar_affricate.main()
    if con == Consonant.VOICELESS_POSTALVEOLAR_FRICATIVE:
        return voiceless_postalveolar_fricative.main()
    if con == Consonant.VOICELESS_VELAR_PLOSIVE:
        return voiceless_velar_plosive.main()
    return np.array([])
