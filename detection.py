import neurokit2 as nk


class Detection:
    @staticmethod
    def detect_local_maxima(signal, threshold_ratio=0.7):
        """
        Détecte les maxima locaux dans un signal ECG.

        Args:
            signal (list or array): Signal ECG brut à analyser.
            threshold_ratio (float): Ratio pour déterminer le seuil de détection.

        Returns:
            list: Indices des maxima locaux détectés.
        """
        if not isinstance(signal, (list, tuple)) and not hasattr(signal,
                                                                 '__iter__'):
            raise ValueError("Le signal doit être un tableau ou une liste.")

        interval = max(signal) - min(signal)
        threshold = threshold_ratio * interval + min(signal)
        maxima = []
        maxima_indices = []
        detected_indices = []
        above_threshold = False

        for i in range(len(signal)):
            if signal[i] >= threshold:  # Si la valeur dépasse le seuil
                above_threshold = True
                maxima_indices.append(i)
                maxima.append(signal[i])
            elif above_threshold and signal[
                i] < threshold:  # Si on retombe en dessous du seuil
                # Trouver l'indice du maximum local
                index_local_max = maxima.index(max(maxima))
                detected_indices.append(maxima_indices[index_local_max])
                # Réinitialiser les valeurs temporaires
                maxima = []
                maxima_indices = []
                above_threshold = False

        return detected_indices

    @staticmethod
    def detect_q_and_s(signal, r_peaks_indices, fs, qrs_duration=0.20):
        """
        Détecte les points Q et S autour des pics R dans un signal ECG.

        Args:
            signal (list or array): Signal ECG brut.
            r_peaks_indices (list): Indices des pics R détectés.
            fs (int): Fréquence d'échantillonnage du signal.
            qrs_duration (float): Durée maximale du complexe QRS en secondes (par défaut : 0.14 s).

        Returns:
            dict: Indices des points Q et S détectés.
        """
        qs_indices = {"Q_Peaks": [], "S_Peaks": []}

        # Taille des fenêtres (en nombre d'échantillons) pour la recherche de Q et S
        window_size = int(
            qrs_duration * fs / 2)  # Demi-fenêtre autour de chaque R

        for r_peak_i in r_peaks_indices:
            # Vérifier les limites des indices pour éviter des erreurs d'accès
            left_start = max(0, r_peak_i - window_size)
            right_end = min(len(signal), r_peak_i + window_size)

            # Intervalle gauche pour détecter Q
            left_interval = signal[left_start:r_peak_i]
            if len(left_interval) > 0:  # Vérification explicite de la taille de l'intervalle
                q_index = left_start + list(left_interval).index(
                    min(left_interval))
                qs_indices["Q_Peaks"].append(q_index)

            # Intervalle droit pour détecter S
            right_interval = signal[r_peak_i:right_end]
            if len(right_interval) > 0:  # Vérification explicite de la taille de l'intervalle
                s_index = r_peak_i + list(right_interval).index(
                    min(right_interval))
                qs_indices["S_Peaks"].append(s_index)

        return qs_indices

    @staticmethod
    def detect_p_wave(signal, r_peaks_indices, fs, search_window=0.3,
                      deriv_window=0.08, threshold=0.25):
        """
        Détecte les débuts des ondes P dans un signal ECG.

        Args:
            signal (list or array): Signal ECG brut.
            r_peaks_indices (list): Indices des pics R détectés.
            fs (int): Fréquence d'échantillonnage.
            search_window (float): Durée (en secondes) avant le pic R pour rechercher l'onde P (par défaut : 0.3 s).
            deriv_window (float): Durée (en secondes) de la fenêtre pour calculer la dérivée (par défaut : 0.08 s).
            threshold (float): Seuil pour détecter l'inflexion (par défaut : 25000).

        Returns:
            list: Indices des débuts des ondes P détectées.
        """
        p_wave_begin = []
        time_derivative_vec = []

        # Convertir les fenêtres de temps en échantillons
        nn = int(search_window * fs)
        interval_der = int(deriv_window * fs)

        for r_peak_i in r_peaks_indices:
            # Limiter la recherche aux indices valides
            start_index = max(0, r_peak_i - nn)
            end_index = max(0, start_index + nn - int(0.2 * fs))

            for i in range(start_index, end_index):
                # Calcul de la dérivée discrète
                if i + interval_der < len(signal):
                    aux = (signal[i + interval_der] - signal[i]) / interval_der
                    time_derivative_vec.append(aux)

                    # Détection du seuil
                    if aux > threshold:
                        p_wave_begin.append(i)
                        break

        return p_wave_begin


    @staticmethod
    def detect_t_wave_end(signal, r_peaks_indices, fs, search_window=0.3,
                          deriv_window=0.04):
        """
        Détecte les fins des ondes T dans un signal ECG.

        Args:
            signal (list or array): Signal ECG brut.
            r_peaks_indices (list): Indices des pics R détectés.
            fs (int): Fréquence d'échantillonnage.
            search_window (float): Durée (en secondes) après le pic R pour rechercher la fin de l'onde T (par défaut : 0.3 s).
            deriv_window (float): Durée (en secondes) de la fenêtre pour calculer la dérivée (par défaut : 0.04 s).

        Returns:
            list: Indices des fins des ondes T détectées.
        """
        t_wave_end = []
        time_derivative_vec = [0]  # Inclure un zéro initial pour comparaison

        # Convertir les fenêtres de temps en échantillons
        nn = int(search_window * fs)
        interval_der = int(deriv_window * fs)

        for r_peak_i in r_peaks_indices:
            # Limiter la recherche aux indices valides
            start_index = min(len(signal) - 1, r_peak_i + nn)
            end_index = min(len(signal), start_index + nn)

            for i in range(start_index, end_index):
                # Calcul de la dérivée discrète
                if i + interval_der < len(signal):
                    aux = (signal[i + interval_der] - signal[i]) / interval_der
                    time_derivative_vec.append(aux)

                    # Détection du point d'inflexion
                    if time_derivative_vec[-1] > 0 > time_derivative_vec[-2]:
                        t_wave_end.append(i)
                        break

        return t_wave_end

    @staticmethod
    def process_ecg_signal(signal, fs):

        _, rpeaks = nk.ecg_peaks(signal, sampling_rate=fs)
        r_peaks = rpeaks["ECG_R_Peaks"]

        qs_peaks = Detection.detect_q_and_s(signal, r_peaks, fs)
        p_wave_starts = Detection.detect_p_wave(signal, r_peaks, fs)
        t_wave_ends = Detection.detect_t_wave_end(signal, r_peaks, fs)

        return {
            "R_Peaks": r_peaks,
            "Q_Peaks": qs_peaks["Q_Peaks"],
            "S_Peaks": qs_peaks["S_Peaks"],
            "P_Peaks": p_wave_starts,
            "T_Wave_Ends": t_wave_ends,
        }

    @staticmethod
    def detect(ecg):
        """Détection des ondes PQRST pour un ensemble de signaux ECG."""
        for line in ecg.treated_lines:
            line.metadata = Detection.process_ecg_signal(line.points,
                                                         line.sampling_rate)
