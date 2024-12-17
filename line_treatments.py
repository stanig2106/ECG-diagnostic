from typing import TYPE_CHECKING

import numpy as np
from scipy.ndimage import median_filter
from scipy.signal import savgol_filter

if TYPE_CHECKING:
    from ecg import ECG


class LineTreatment:
    # Fréquence basse (Hz) pour le filtre passe-bande
    LOW_CUTOFF = 0.5
    # Fréquence haute (Hz) pour le filtre passe-bande
    HIGH_CUTOFF = 40

    # Taille de la fenêtre pour la correction de la ligne de base (ms)
    BASELINE_WINDOW_SIZE_MS = 200

    # Taille de la fenêtre de lissage (impair)
    SMOOTH_WINDOW_LENGTH = 31
    # Ordre du polynôme pour le filtre Savitzky-Golay
    SMOOTH_POLYORDER = 2

    @staticmethod
    def treat_ecg(ecg: 'ECG') -> None:
        """
        Traiter les lignes ECG : appliquer tous les traitements nécessaires.
        """
        ecg.treated_lines = [line.copy(line.label + " (treated)") for line in
                             ecg.lines]
        for line in ecg.treated_lines:
            LineTreatment.denoise_with_fft(line)
            LineTreatment.baseline_correct(line)
            LineTreatment.smooth(line)

    @staticmethod
    def denoise_with_fft(line: 'ECG.Line') -> None:
        """
        Denoiser une ligne ECG avec un filtre passe-bande dans le domaine fréquentiel.
        """
        low_cutoff = LineTreatment.LOW_CUTOFF
        high_cutoff = LineTreatment.HIGH_CUTOFF
        sampling_rate = line.sampling_rate

        # Transformer le signal dans le domaine fréquentiel
        freq = np.fft.rfftfreq(len(line.points), d=1 / sampling_rate)
        fft_values = np.fft.rfft(line.points)

        # Appliquer un filtre passe-bande
        fft_filtered = np.zeros_like(fft_values)
        for i, f in enumerate(freq):
            if low_cutoff <= f <= high_cutoff:  # type: ignore
                fft_filtered[i] = fft_values[i]

        # Revenir dans le domaine temporel
        line.points = np.fft.irfft(fft_filtered)

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

    @staticmethod
    def smooth(line: 'ECG.Line') -> None:
        """
        Lisser le signal ECG avec un filtre Savitzky-Golay pour réduire les variations mineures.
        """
        window_length = LineTreatment.SMOOTH_WINDOW_LENGTH
        polyorder = LineTreatment.SMOOTH_POLYORDER
        line.points = savgol_filter(line.points, window_length, polyorder)
