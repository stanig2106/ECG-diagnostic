from calculation import Calculation


class Diagnostics:
    @staticmethod
    def is_tachycardie(calc: Calculation) -> bool:
        """Détecte une tachycardie : fréquence cardiaque supérieure à 100 bpm."""
        return calc.heart_rate() > 100

    @staticmethod
    def is_bradycardie(calc: Calculation) -> bool:
        """Détecte une bradycardie : fréquence cardiaque inférieure à 60 bpm."""
        return calc.heart_rate() < 60

    @staticmethod
    def is_pr_interval_prolonged(calc: Calculation) -> bool:
        """Détecte un PR prolongé : intervalle PR supérieur à 200 ms."""
        return any(pr > 200 for pr in calc.pr_intervals())

    @staticmethod
    def is_pr_interval_short(calc: Calculation) -> bool:
        """Détecte un PR court : intervalle PR inférieur à 120 ms."""
        return any(pr < 120 for pr in calc.pr_intervals())

    @staticmethod
    def is_qrs_duration_prolonged(calc: Calculation) -> bool:
        """Détecte un QRS élargi : durée supérieure à 120 ms."""
        return any(qrs > 120 for qrs in calc.qrs_complexes())

    @staticmethod
    def is_st_elevation(calc: Calculation) -> bool:
        """Détecte une élévation du segment ST : déviation supérieure à 0,2 mV."""
        return any(st > 200 for st in calc.st_segments())

    @staticmethod
    def is_st_depression(calc: Calculation) -> bool:
        """Détecte une dépression du segment ST : déviation inférieure à -0,1 mV."""
        return any(st < -100 for st in calc.st_segments())

    @staticmethod
    def is_p_wave_absent(calc: Calculation) -> bool:
        """Détecte l'absence d'onde P, suggérant une fibrillation auriculaire."""
        return all(p == 0 for p in calc.p_wave_amplitudes())

    @staticmethod
    def is_qt_prolonged(calc: Calculation) -> bool:
        """
        Détecte un QT prolongé : QTc > 460 ms (femmes) ou 440 ms (hommes).
        Utilise la formule de Bazett : QTc = QT / sqrt(RR).
        """
        qt = calc.qt_intervals()
        rr = calc.rr_intervals()
        qtcs = [qt[i] / (rr[i] ** 0.5) for i in range(len(qt))]
        seuil = 460 if calc.age_of_patient() > 18 else 440
        return any(qtc > seuil for qtc in qtcs)

    @staticmethod
    def is_hypertrophy_left_ventricular(calc: Calculation) -> bool:
        """Détecte une hypertrophie ventriculaire gauche selon le critère de Sokolow-Lyon : S(V1) + R(V5/V6) > 35 mm."""
        qrs_amplitudes = calc.qrs_amplitudes()
        return sum(qrs_amplitudes) > 35

    @staticmethod
    def is_fibrillation_atrial(calc: Calculation) -> bool:
        """Détecte une fibrillation auriculaire : absence d'onde P et RR irréguliers."""
        rr_intervals = calc.rr_intervals()
        return Diagnostics.is_p_wave_absent(calc) and len(set(rr_intervals)) > 1

    @staticmethod
    def is_infarctus_acute(calc: Calculation) -> bool:
        """Détecte un infarctus aigu du myocarde : élévation ST et QRS élargi."""
        return Diagnostics.is_st_elevation(
            calc) and Diagnostics.is_qrs_duration_prolonged(
            calc)

    @staticmethod
    def is_hyperkaliemia(calc: Calculation) -> bool:
        """Détecte une hyperkaliémie : onde T pointue avec amplitude supérieure à 0,5 mV."""
        return any(t > 0.5 for t in calc.t_wave_amplitudes())

    @staticmethod
    def is_hypokaliemia(calc: Calculation) -> bool:
        """Détecte une hypokaliémie : onde T aplatie et segment ST déprimé."""
        return any(t < 0.1 for t in
                   calc.t_wave_amplitudes()) and Diagnostics.is_st_depression(
            calc)
