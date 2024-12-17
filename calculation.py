from ecg import ECG


class Calculation:
    ecg: 'ECG'

    def __init__(self, ecg: 'ECG'):
        self.ecg = ecg

    def pr_intervals(self) -> [int]:
        """
        PR intervals in milliseconds.
        """
        pass

    def pr_segments(self) -> [int]:
        """
        PR segments in milliseconds.
        """
        pass

    def qrs_complexes(self) -> [int]:
        """
        QRS durations in milliseconds.
        """
        pass

    def qt_intervals(self) -> [int]:
        """
        QT intervals in milliseconds.
        """
        pass

    def st_segments(self) -> [int]:
        """
        ST segments in milliseconds.
        """
        pass

    def periods(self) -> [int]
        """
        Return time of each period in milliseconds.
        A period is the time between two R-peaks.
        """
        pass

    def heart_rate(self) -> int:
        """
        Heart rate in beats per minute. (mean)
        """
        pass

    def age_of_patient(self) -> int:
        """
        Age of the patient in years.
        """
        pass
