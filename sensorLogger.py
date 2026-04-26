# ==========================================================
# 🌸 SensorLogger— Neon Observatory
# Single-file Portfolio Edition
# Real-time Multi-Channel Laptop Sensor DAQ System
# ==========================================================
# Install:
# pip install rich psutil opencv-python numpy sounddevice keyboard
#
# Run:
# python sensor_logger_elite.py
# ==========================================================

import os
import csv
import json
import time
import math
import threading
from collections import deque

import numpy as np
import psutil
import cv2
import sounddevice as sd
import keyboard

from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text

# ==========================================================
# CONFIG
# ==========================================================
SAMPLE_RATE_HZ = 10              # 10 samples/sec = every 100 ms
SAMPLE_INTERVAL = 1 / SAMPLE_RATE_HZ
BUFFER_SIZE = 500
REFRESH_FPS = 4

LOG_DIR = "logs"
CSV_PATH = f"{LOG_DIR}/session.csv"
JSON_PATH = f"{LOG_DIR}/session.json"

os.makedirs(LOG_DIR, exist_ok=True)

# ==========================================================
# RING BUFFER CLASS
# ==========================================================
class RingBuffer:
    def __init__(self, size):
        self.data = deque(maxlen=size)

    def append(self, value):
        self.data.append(value)

    def values(self):
        return list(self.data)

    def latest(self):
        return self.data[-1] if self.data else 0

    def mean(self):
        return float(np.mean(self.data)) if self.data else 0

    def std(self):
        return float(np.std(self.data)) if self.data else 0

    def min(self):
        return float(np.min(self.data)) if self.data else 0

    def max(self):
        return float(np.max(self.data)) if self.data else 0

# ==========================================================
# LOGGER
# ==========================================================
class SessionLogger:
    def __init__(self):
        self.rows = []

        self.csv_file = open(CSV_PATH, "w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.csv_file)

        self.writer.writerow([
            "timestamp",
            "mic_rms",
            "motion",
            "keys_per_sec",
            "cpu_percent",
            "power_metric"
        ])

    def write(self, row):
        self.rows.append(row)
        self.writer.writerow(row)

    def close(self):
        self.csv_file.close()

        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(self.rows, f, indent=2)

# ==========================================================
# ANOMALY DETECTION
# ==========================================================
def zscore_spike(value, mean, std, threshold=2.5):
    if std == 0:
        return False
    z = abs(value - mean) / std
    return z > threshold

def jump_detect(curr, prev, threshold):
    return abs(curr - prev) > threshold

# ==========================================================
# SPARKLINE
# ==========================================================
def sparkline(data, width=40):
    bars = "▁▂▃▄▅▆▇█"

    if not data:
        return ""

    arr = np.array(data[-width:])
    mn = arr.min()
    mx = arr.max()

    if mx - mn == 0:
        return bars[0] * len(arr)

    out = ""
    for v in arr:
        idx = int((v - mn) / (mx - mn) * (len(bars) - 1))
        out += bars[idx]

    return out

# ==========================================================
# KEYBOARD SENSOR
# ==========================================================
key_count = 0

def on_key(event):
    global key_count
    key_count += 1

keyboard.on_press(on_key)

# ==========================================================
# CAMERA SENSOR
# ==========================================================
cap = cv2.VideoCapture(0)
prev_gray = None

def read_motion():
    global prev_gray

    try:
        ok, frame = cap.read()
        if not ok:
            return 0.0

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (160, 120))

        if prev_gray is None:
            prev_gray = gray
            return 0.0

        diff = cv2.absdiff(prev_gray, gray)
        prev_gray = gray

        return float(np.mean(diff))

    except:
        return 0.0

# ==========================================================
# MICROPHONE SENSOR
# ==========================================================
def read_mic():
    try:
        audio = sd.rec(
            400,
            samplerate=8000,
            channels=1,
            blocking=True
        )

        rms = np.sqrt(np.mean(audio ** 2))
        return float(rms * 1000)

    except:
        return 0.0

# ==========================================================
# SYSTEM METRICS
# ==========================================================
def read_cpu():
    try:
        return psutil.cpu_percent()
    except:
        return 0.0

def read_power():
    try:
        battery = psutil.sensors_battery()

        if battery:
            return battery.percent

        # desktop fallback
        return psutil.cpu_freq().current / 100

    except:
        return 0.0

# ==========================================================
# DASHBOARD UI
# ==========================================================
def build_dashboard(buffers, alerts, uptime, sample_count):
    table = Table(
        title="🌸 Neon Observatory — SensorLogger ELITE",
        expand=True
    )

    table.add_column("Channel", style="bold magenta")
    table.add_column("Now", justify="right")
    table.add_column("Avg", justify="right")
    table.add_column("Min", justify="right")
    table.add_column("Max", justify="right")
    table.add_column("Trend", style="bright_magenta")

    for name, buf in buffers.items():
        table.add_row(
            name,
            f"{buf.latest():.2f}",
            f"{buf.mean():.2f}",
            f"{buf.min():.2f}",
            f"{buf.max():.2f}",
            sparkline(buf.values())
        )

    if alerts:
        status = " | ".join(alerts)
        color = "bold red"
    else:
        status = "Stable • All Channels Healthy"
        color = "bold bright_magenta"

    subtitle = (
        f"[{color}]{status}[/{color}]"
        f" | Samples: {sample_count}"
        f" | Uptime: {uptime:.1f}s"
    )

    return Panel(
        table,
        subtitle=subtitle,
        border_style="magenta"
    )

# ==========================================================
# MAIN
# ==========================================================
def main():
    global key_count

    buffers = {
        "Mic RMS": RingBuffer(BUFFER_SIZE),
        "Motion": RingBuffer(BUFFER_SIZE),
        "Keys/s": RingBuffer(BUFFER_SIZE),
        "CPU %": RingBuffer(BUFFER_SIZE),
        "Power": RingBuffer(BUFFER_SIZE),
    }

    logger = SessionLogger()

    start_time = time.time()
    sample_count = 0

    with Live(
        build_dashboard(buffers, [], 0, 0),
        refresh_per_second=REFRESH_FPS,
        screen=False
    ) as live:

        try:
            while True:
                loop_start = time.time()

                # ----------------------------------
                # READ SENSORS
                # ----------------------------------
                mic = read_mic()
                motion = read_motion()

                keys = key_count * SAMPLE_RATE_HZ
                key_count = 0

                cpu = read_cpu()
                power = read_power()

                readings = {
                    "Mic RMS": mic,
                    "Motion": motion,
                    "Keys/s": keys,
                    "CPU %": cpu,
                    "Power": power
                }

                # ----------------------------------
                # ANALYZE
                # ----------------------------------
                alerts = []

                for name, value in readings.items():
                    buf = buffers[name]

                    prev = buf.latest()
                    mean = buf.mean()
                    std = buf.std()

                    if len(buf.values()) > 20:
                        if zscore_spike(value, mean, std):
                            alerts.append(f"{name} spike")

                        if jump_detect(
                            value,
                            prev,
                            threshold=max(5, std * 2)
                        ):
                            alerts.append(f"{name} jump")

                    buf.append(value)

                # ----------------------------------
                # LOG
                # ----------------------------------
                ts = time.time()

                logger.write([
                    ts,
                    mic,
                    motion,
                    keys,
                    cpu,
                    power
                ])

                sample_count += 1

                # ----------------------------------
                # UI UPDATE
                # ----------------------------------
                uptime = ts - start_time

                live.update(
                    build_dashboard(
                        buffers,
                        alerts,
                        uptime,
                        sample_count
                    )
                )

                # ----------------------------------
                # SAMPLE RATE CONTROL
                # ----------------------------------
                elapsed = time.time() - loop_start
                sleep_time = max(0, SAMPLE_INTERVAL - elapsed)
                time.sleep(sleep_time)

        except KeyboardInterrupt:
            pass

        finally:
            logger.close()
            cap.release()

            print("\n🌸 Session Saved:")
            print("   logs/session.csv")
            print("   logs/session.json")

# ==========================================================
# RUN
# ==========================================================
if __name__ == "__main__":
    main()