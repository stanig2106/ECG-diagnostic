# PQRST ECG Analysis Tool

PQRST is a Python-based tool designed to process and analyze ECG (
Electrocardiogram) data using advanced signal processing techniques. The project
leverages the power of the `neurokit2` library to clean ECG signals and applies
methods for baseline correction and merging of multiple signal lines. This
repository is part of a broader effort to enhance diagnostic capabilities in
cardiology.

## Features

- **Signal Cleaning**: Uses `neurokit2` for robust ECG signal cleaning.
- **Baseline Correction**: Applies windowed baseline correction to ECG lines.
- **Signal Merging**: Combines multiple ECG lines into a single, averaged signal
  for easier interpretation.
- **Patient Data Integration**: Handles patient metadata and links it with
  corresponding ECG data files.
- **Diagnosis Handling**: Processes diagnostic information alongside ECG signal
  data.

## Installation

### Requirements

- Python 3.8+
- Virtual environment (recommended)
- Required libraries: `neurokit2`, `numpy`, and any other dependencies mentioned
  in `requirements.txt`.

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pqrst-ecg-tool.git
   cd pqrst-ecg-tool
   ```
   
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv-pqrst
   source venv-pqrst/bin/activate
    ```

3. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Key Files
- line_treatments.py: Contains the core logic for cleaning, baseline correction,
and merging ECG lines.
- detection.py: Contains functions for detecting peaks and other features in ECG
  signals.
- diagnostics.py: Contains functions for processing diagnostic information.
- main.py: Main script for printing and processing patient ECG data.
