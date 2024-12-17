import matplotlib
import pandas as pd

from ecg import ECG
from line_treatments import LineTreatment
from parser import parse_lines

matplotlib.use("Qt5Agg")

if __name__ == "__main__":
    PATH = "df_meta.pkl"
    df_meta = pd.read_pickle(PATH)

    first_ecg = df_meta.iloc[2]
    print(first_ecg)

    ecg = ECG(first_ecg,
              parse_lines(first_ecg.ecg_file_path))

    LineTreatment.treat_ecg(ecg)

    ecg.plot(treated=True)
