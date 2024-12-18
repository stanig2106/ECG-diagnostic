import matplotlib
import pandas as pd

from ecg import ECG
from line_treatments import LineTreatment
from parser import parse_lines
from peak_detection import PeakDetection

matplotlib.use("Qt5Agg")




if __name__ == "__main__":
    PATH = "df_meta.pkl"
    df_meta = pd.read_pickle(PATH)

    first_ecg = df_meta.iloc[0]
    print(first_ecg)

    ecg = ECG(first_ecg,
              parse_lines(first_ecg.ecg_file_path))

    LineTreatment.treat_ecg(ecg)
    LineTreatment.merge_ecg(ecg)
    PeakDetection.detect_peaks(ecg)

    ecg.plot(treated=True)
