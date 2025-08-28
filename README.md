# Adaptive ECG ST-Peak Analysis

## Project Overview
This project analyzes ECG data from two patients, detecting S- and T-wave peaks to calculate the S-T voltage difference. The analysis adapts automatically to any ECG dataset, regardless of heart rate or amplitude.

## Dataset
- Source: `ecgPatientData.xlsx`
- Columns:
  - Column A: Time (seconds)
  - Column B: Patient 1 ECG
  - Column C: Patient 2 ECG
- Sample size: 75,000 rows per patient
- Context: Patient 1 appears to be exercising (jogging/running), resulting in faster, tighter peaks. Patient 2 is likely at rest.

## Methods
1. ECG data is normalized to ±1 for relative amplitude comparison.
2. Adaptive R-wave detection identifies S-waves by finding the local minimum immediately after R-peaks.
3. T-waves are detected as local maxima within 30–300 ms after each S-wave.
4. The S-T voltage difference is computed as the mean difference between S- and T-wave voltages for each window of 6 seconds with 50% overlap.
5. Visualization includes the ECG trace with S- and T-wave markers, and the mean S-T voltage difference.

## Results
- Patient 1: Average S-T voltage difference ≈ 0.268–0.283
- Patient 2: Average S-T voltage difference ≈ 0.208–0.340

### Interpretation
- Patient 1 shows stable S-T segments consistent with exercise-induced repolarization changes.
- Patient 2 shows more variability in S-T difference, consistent with normal physiological fluctuations at rest.
- No extreme S-T elevations or depressions were observed.

## Caveats
- ECG data is normalized; absolute clinical interpretation requires raw mV calibration.
- Heart rate, electrode placement, and noise can influence peak detection.
- Small S-T differences are normal during activity and do not indicate pathology by themselves.

## Usage
1. Place the dataset in the `data/` folder.
2. Run the Python script:

```bash
python scripts/adaptive_ecg_st_peak_analysis.py