from dataclasses import dataclass
from typing import List, Optional
from typing import Union

import numpy as np

from plot import Plot


class ECG:
    lines: ['ECG.Line']
    treated_lines: ['ECG.Line'] = None

    # pickle data
    @dataclass
    class PatientData:
        patient_id: Optional[str]
        age: Optional[int]
        date_of_birth: Optional[str]
        gender: Optional[Union[str, int]]
        height_cm: Optional[float]
        weight_kg: Optional[float]
        date: Optional[str]
        location: Optional[str]
        diagnosis: Optional[Union[List[str], str]]
        original_diagnosis: Optional[Union[List[str], str]]

    data: 'ECG.PatientData'

    class Line:
        label: str
        points: np.ndarray
        sampling_rate: int
        metadata: Optional[dict] = None

        def __init__(self, label: str, points: np.ndarray, sampling_rate: int):
            self.label = str.strip(label)
            self.points = points
            self.sampling_rate = sampling_rate

        def copy(self, new_label: Optional[str] = None) -> 'ECG.Line':
            return ECG.Line(new_label or self.label,
                            self.points.copy(), self.sampling_rate)

    def __init__(self, data: 'ECG.PatientData', lines: List['ECG.Line']):
        self.data = data
        self.lines = lines

    def plot(self, line: Optional[str] = None, treated: bool = False):
        """Plot one or more ECG lines with patient information."""
        # Prepare patient information
        patient_info = (
            f"Patient ID: {self.data.patient_id}\n"
            f"Age: {self.data.age}\n"
            f"Date of Birth: {self.data.date_of_birth}\n"
            f"Gender: {self.data.gender}\n"
            f"Height: {self.data.height_cm} cm\n"
            f"Weight: {self.data.weight_kg} kg\n"
            f"Date: {self.data.date}\n"
            f"Location: {self.data.location}\n"
            f"Diagnosis: {self.data.diagnosis}\n"
            f"Original Diagnosis: {self.data.original_diagnosis}"
        )

        # Show patient info and plot lines
        Plot.show_text(patient_info)
        if treated:
            # display line and treated line
            Plot.plot_lines(
                [*self.lines, *self.treated_lines],
                title="ECG Lines",
                selected_label=line)
        else:
            Plot.plot_lines(self.lines, title=f"ECG Line: {line}",
                            selected_label=line)

        Plot.show()
