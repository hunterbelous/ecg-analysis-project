import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# --- LOAD DATA ---
patient = int(input("Which patient would you like to receive data from (1) or (2)? "))

filepath = r"C:\Users\BelousH\Downloads\ecgPatientData.xlsx"

if patient == 1:
    data = pd.read_excel(filepath, usecols="A:B", nrows=75000).to_numpy()
else:
    data = pd.read_excel(filepath, usecols="A,C", nrows=75000).to_numpy()

# --- EXTRACT TIME AND ECG ---
time = data[:, 0]
ecg_raw = data[:, 1]

# --- NORMALIZE ECG to ±1 for relative amplitude ---
ecg = ecg_raw / np.max(np.abs(ecg_raw))

# --- SAMPLING FREQUENCY ---
fs = round(1 / np.mean(np.diff(time)))  # Hz

# --- WINDOW PARAMETERS ---
winSize = 6           # seconds
pctOver = 0.5         # 50% overlap
sampPerWin = int(fs * winSize)
winInc = int((1 - pctOver) * sampPerWin)

startInd = 0
endInd = sampPerWin

# --- PLOT SETUP ---
fig, ax = plt.subplots(figsize=(12, 6))


def plot_window():
    global startInd, endInd
    ax.clear()
    window_ecg = ecg[startInd:endInd]
    window_time = time[startInd:endInd]

    # --- Adaptive R-wave detection ---
    local_max = np.max(window_ecg)
    r_min_height = 0.3 * local_max  # 30% of window max
    # Estimate min distance: ~200ms (max 300 bpm) → fs * 0.2
    min_dist = int(0.2 * fs)
    r_peaks, _ = find_peaks(window_ecg, height=r_min_height, distance=min_dist)

    # --- S-wave detection (trough just after R) ---
    s_peaks = []
    for r in r_peaks:
        search_end = min(r + int(0.06 * fs), len(window_ecg))
        if r < search_end:
            s_idx = r + np.argmin(window_ecg[r:search_end])
            s_peaks.append(s_idx)
    s_peaks = np.array(s_peaks)

    # --- T-wave detection (local max after S, 30–300ms) ---
    t_peaks = []
    for s in s_peaks:
        search_start = s + int(0.03 * fs)
        search_end = min(s + int(0.3 * fs), len(window_ecg))
        if search_start < search_end:
            t_idx = search_start + np.argmax(window_ecg[search_start:search_end])
            t_peaks.append(t_idx)
    t_peaks = np.array(t_peaks)

    # --- Voltages for S and T waves ---
    s_volt = window_ecg[s_peaks] if len(s_peaks) > 0 else []
    t_volt = window_ecg[t_peaks] if len(t_peaks) > 0 else []

    # --- Mean S-T voltage difference ---
    if len(s_volt) > 0 and len(t_volt) > 0:
        avg_ST = round(abs(np.mean(s_volt) - np.mean(t_volt)), 3)
    else:
        avg_ST = np.nan

    # --- Plotting ---
    ax.plot(window_time, window_ecg, label="ECG (normalized)")
    if len(s_peaks) > 0:
        ax.plot(window_time[s_peaks], s_volt, "ro", label="S wave")
    if len(t_peaks) > 0:
        ax.plot(window_time[t_peaks], t_volt, "bd", label="T wave")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Voltage (normalized)")
    ax.set_title(f"Mean S-T Voltage Difference: {avg_ST}")
    ax.legend()
    fig.canvas.draw()


def on_key(event):
    global startInd, endInd
    if event.key == "right":
        if endInd + winInc <= len(ecg):
            startInd += winInc
            endInd += winInc
            plot_window()
    elif event.key == "left":
        if startInd - winInc >= 0:
            startInd -= winInc
            endInd -= winInc
            plot_window()


def on_click(event):
    global startInd, endInd
    if endInd + winInc <= len(ecg):
        startInd += winInc
        endInd += winInc
        plot_window()


# --- CONNECT EVENTS ---
fig.canvas.mpl_connect("key_press_event", on_key)
fig.canvas.mpl_connect("button_press_event", on_click)

# --- INITIAL PLOT ---
plot_window()
plt.show()