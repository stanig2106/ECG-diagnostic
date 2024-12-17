from typing import List

import pandas as pd

from ecg import ECG

SAMPLING_RATE = 500


def parse_lines(csv_path: str) -> List['ECG.Line']:
    df = pd.read_csv(csv_path)
    lines = [
        ECG.Line(label=column, points=df[column].to_numpy(),
                 sampling_rate=SAMPLING_RATE)
        for column in df.columns if len(str.strip(column)) > 0
    ]

    return lines
