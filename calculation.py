from ecg import ECG


class Calculation:
    ecg: 'ECG'

    def __init__(self, ecg: 'ECG'):
        """
        Initialise l'objet Calculation avec une instance de la classe ECG.
        """
        self.ecg = ecg

    def pr_intervals(self) -> [int]:
        """
        Retourne les durées des intervalles PR en millisecondes.
        """
        return self.ecg.get_pr_intervals()

    def pr_segments(self) -> [int]:
        """
        Retourne les durées des segments PR en millisecondes.
        """
        return self.ecg.get_pr_segments()

    def qrs_complexes(self) -> [int]:
        """
        Retourne les durées des complexes QRS en millisecondes.
        """
        return self.ecg.get_qrs_durations()

    def qt_intervals(self) -> [int]:
        """
        Retourne les durées des intervalles QT en millisecondes.
        """
        return self.ecg.get_qt_intervals()

    def st_segments(self) -> [int]:
        """
        Retourne les déviations du segment ST en millivolts (converti en millisecondes si nécessaire).
        """
        return self.ecg.get_st_segments()

    def rr_intervals(self) -> [int]:
        """
        Retourne les intervalles RR en millisecondes (temps entre deux pics R successifs).
        """
        return self.ecg.get_rr_intervals()

    def heart_rate(self) -> int:
        """
        Calcule et retourne la fréquence cardiaque moyenne en battements par minute (bpm).
        """
        rr = self.rr_intervals()
        return int(60000 / (sum(rr) / len(rr))) if rr else 0

    def age_of_patient(self) -> int:
        """
        Retourne l'âge du patient en années.
        """
        return self.ecg.get_patient_age()

    def p_wave_amplitudes(self) -> [float]:
        """
        Retourne les amplitudes des ondes P en millivolts.
        """
        return self.ecg.get_p_wave_amplitudes()

    def qrs_amplitudes(self) -> [float]:
        """
        Retourne les amplitudes maximales des complexes QRS en millivolts.
        """
        return self.ecg.get_qrs_amplitudes()

    def t_wave_amplitudes(self) -> [float]:
        """
        Retourne les amplitudes des ondes T en millivolts.
        """
        return self.ecg.get_t_wave_amplitudes()

    def electrical_axis_qrs(self) -> float:
        """
        Retourne l'axe électrique du complexe QRS en degrés.
        """
        return self.ecg.get_qrs_axis()
