import matplotlib
import pandas as pd

from detection import Detection
from ecg import ECG
from line_treatments import LineTreatment
from parser import parse_lines

matplotlib.use("Qt5Agg")

if __name__ == "__main__":
    PATH = "df_meta.pkl"
    df_meta = pd.read_pickle(PATH)

    first_ecg = df_meta.iloc[2]
    # first_ecg = df_meta[df_meta.patient_id == "13sXbYL/2zfNpTZwcuDVQA=="].iloc[
    #     0]
    print(first_ecg)

    ecg = ECG(first_ecg,
              parse_lines(first_ecg.ecg_file_path))

    LineTreatment.treat_ecg(ecg)
    LineTreatment.merge_ecg(ecg)
    Detection.detect(ecg)

    ecg.plot(treated=True)
