from typing import TYPE_CHECKING
import neurokit2 as nk
from scipy.ndimage import median_filter

if TYPE_CHECKING:
    from ecg import ECG


class LineTreatment:
    # Taille de la fenêtre pour la correction de la ligne de base (ms)
    BASELINE_WINDOW_SIZE_MS = 200

    @staticmethod
    def treat_ecg(ecg: 'ECG') -> None:
        """
        Traiter les lignes ECG : appliquer tous les traitements nécessaires.
        """
        ecg.treated_lines = [line.copy(line.label + " (treated)") for line in
                             ecg.lines]
        for line in ecg.treated_lines:
            line.points = nk.signal_filter(
                line.points, sampling_rate=line.sampling_rate,
                lowcut=0.5, highcut=45, method="butterworth", order=5
            )
            LineTreatment.baseline_correct(line)

    @staticmethod
    def baseline_correct(line: 'ECG.Line') -> None:
        """
        Corriger la ligne de base ECG pour éliminer la dérive.
        Utilise un filtrage médian pour une correction robuste.
        """
        window_size = int(
            (LineTreatment.BASELINE_WINDOW_SIZE_MS / 1000) * line.sampling_rate)
        baseline = median_filter(line.points, size=window_size)
        line.points = line.points - baseline
