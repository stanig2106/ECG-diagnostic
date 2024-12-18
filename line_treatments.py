import neurokit2 as nk
import numpy as np

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
            line.points = nk.ecg_clean(line.points,
                                       sampling_rate=line.sampling_rate,
                                       method="neurokit")

    @staticmethod
    def merge_ecg(ecg: 'ECG'):
        if any([line.sampling_rate != ecg.treated_lines[0].sampling_rate for
                line in ecg.treated_lines]):
            raise ValueError("All lines must have the same sampling rate.")
        if any([line.points.shape[0] != ecg.treated_lines[0].points.shape[0] for
                line in ecg.treated_lines]):
            raise ValueError("All lines must have the same length.")

        treated_points = [np.asarray(line.points) for line in ecg.treated_lines]
        merged = np.mean(treated_points, axis=0)

        ecg.treated_lines += [
            ECG.Line("Merged", merged, ecg.treated_lines[0].sampling_rate)]
