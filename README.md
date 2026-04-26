<div align="center">

# 🌸 SENSORLOGGER ELITE

## *Neon Observatory — Day 20 · BUILDCORED ORCAS*

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&pause=1200&color=FF4FD8&center=true&vCenter=true&width=850&lines=Turning+a+Laptop+Into+a+Real-Time+Sensor+Lab;Multi-Channel+DAQ+System+Built+in+Python;Telemetry+%7C+Anomaly+Detection+%7C+Live+Dashboard" />

<br>

![Python](https://img.shields.io/badge/PYTHON-3.9+-2b2d42?style=for-the-badge\&logo=python)
![NumPy](https://img.shields.io/badge/NUMPY-1.24+-9D4EDD?style=for-the-badge\&logo=numpy)
![OpenCV](https://img.shields.io/badge/OPENCV-4.X-2b2d42?style=for-the-badge\&logo=opencv)
![Rich](https://img.shields.io/badge/RICH-LIVE_UI-FF4FD8?style=for-the-badge)
![Status](https://img.shields.io/badge/STATUS-SHIPPED-success?style=for-the-badge)
![DAQ](https://img.shields.io/badge/HARDWARE_INSPIRED-YES-ff66c4?style=for-the-badge)

<br><br>

> Your laptop already contains sensors.
> **SensorLogger makes them visible.**

A portfolio-grade Python system that transforms a normal laptop into a **multi-channel data acquisition station** by continuously sampling real hardware signals in real time.

</div>

---

# ✨ What This Is

Most people use laptops passively.

SensorLogger uses your laptop like an engineer would use a lab instrument.

It continuously reads:

* 🎤 microphone loudness
* 📷 webcam motion activity
* ⌨️ keyboard interaction rate
* 💻 CPU workload
* 🔋 battery / power telemetry

All channels are:

✅ timestamped
✅ sampled every 100ms
✅ stored in circular buffers
✅ analyzed live
✅ displayed in a glowing terminal dashboard
✅ exported to logs

---

# 🌌 Why This Is Cool

This project mirrors how professional **DAQ systems** work.

Real companies use similar ideas in:

* aerospace telemetry
* robotics monitoring
* automotive diagnostics
* industrial automation
* smart buildings
* medical systems

This project recreates those concepts with **consumer hardware + Python**.

---

# ⚡ Live Dashboard

<div align="center">

```text id="j1w1v9"
🌸 Neon Observatory

Mic RMS      8.14    ▁▂▃▄▅▆▇█
Motion       2.91    ▁▁▂▃▄▅▆█
Keys/s      11.00    ▁▃█▅▂▁▁▁
CPU %       27.00    ▂▃▄▅▆▇▅▃
Power       81.00    ████████

Stable • All Channels Healthy
```

</div>

---

# 🧠 What It Teaches

SensorLogger introduces beginner-friendly versions of advanced engineering ideas:

## ⏱ Real-Time Sampling

The program runs every 100 milliseconds:

```text id="mcr15n"
Read Sensors → Analyze → Update UI → Save Logs → Repeat
```

This is how many embedded systems operate.

---

## ♻️ Circular Buffers

Instead of storing infinite data, only recent samples are kept.

```text id="mb2j1q"
[ old old old recent newest ]
```

When full, old data is overwritten.

Efficient. Fast. Industry standard.

---

## 🚨 Anomaly Detection

The logger detects unusual spikes such as:

* loud clap near microphone
* sudden movement in camera
* rapid typing burst
* CPU surge from heavy apps

Using:

* Z-score statistics
* jump detection
* rolling baseline comparison

---

# 🛰 Sensor Channels

| Channel    | Meaning                            |
| ---------- | ---------------------------------- |
| 🎤 Mic RMS | Measures sound energy              |
| 📷 Motion  | Measures scene movement            |
| ⌨️ Keys/s  | Measures interaction activity      |
| 💻 CPU %   | Measures processor usage           |
| 🔋 Power   | Measures battery or fallback power |

---

# 🛠 Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-Primary-blue?style=flat-square)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-green?style=flat-square)
![NumPy](https://img.shields.io/badge/NumPy-Fast_Arrays-purple?style=flat-square)
![Rich](https://img.shields.io/badge/Rich-Terminal_UI-pink?style=flat-square)
![psutil](https://img.shields.io/badge/psutil-System_Metrics-orange?style=flat-square)

</div>

---

# 📂 Project Structure

```text id="85y72d"
SensorLogger/
│── sensorlogger.py
│── README.md
│── logs/
│   ├── session.csv
│   └── session.json
```

---

# ⚙️ Installation

## 1. Clone / Download

```bash id="mymf3n"
git clone <your-repo-link>
cd SensorLogger
```

## 2. Install Requirements

```bash id="2tjjhv"
pip install rich psutil opencv-python numpy sounddevice keyboard
```

## 3. Run

```bash id="mgg7qg"
python sensorlogger.py
```

---

# 📁 Output Logs

When you stop the program:

```text id="yfy1jv"
logs/session.csv
logs/session.json
```

Useful for:

* graphing data
* replay systems
* machine learning
* time-series analysis
* behavior analytics

---

# 🌸 Why This Stands Out on a Portfolio

Most beginner projects say:

> “I learned syntax.”

This one says:

> “I understand systems.”

It demonstrates:

✅ real-time programming
✅ hardware/software thinking
✅ telemetry pipelines
✅ statistics basics
✅ UI design taste
✅ clean engineering mindset

---

# 🚀 Future Upgrades

* FFT audio spectrum analyzer
* scrolling live graphs
* web dashboard
* Raspberry Pi deployment
* ESP32 external sensors
* cloud sync telemetry
* AI anomaly classifier
* sensor correlation heatmaps

---

# 💼 Resume Bullet Example

> Built a real-time multi-channel laptop telemetry system in Python using OpenCV, NumPy, psutil, and Rich UI with anomaly detection, circular buffers, and synchronized 10Hz data logging.

---

# 🌙 Final Thought

A laptop looks ordinary.

But inside it are sensors, signals, and hidden data streams.

**SensorLogger turns invisible hardware into visible intelligence.**

---

<div align="center">

### 🌸 Built with curiosity, engineering obsession, and neon energy.

</div>
