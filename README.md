# FactoryMind AI — AI-Based Predictive Manufacturing Platform

**FactoryMind AI** is an end-to-end intelligent predictive maintenance and machine health monitoring platform connecting factory floor assets, PLC / IIoT edge gateways, machine learning anomaly detection, explainable AI (XAI) diagnostics, and maintenance workflows.

---

## 🌟 Key Highlights & What Makes This Unique

1. **Dual Enterprise Language Architecture (Python + Java):**
   - **Java Industrial Edge Gateway (`IndustrialEdgeGateway.java`):** Mirrors industrial shopfloor standards (Siemens, Fanuc, OPC-UA). High-throughput concurrent worker threads poll machine telemetry and transmit structured JSON frames with retry resilience.
   - **Python AI/ML Diagnostic Engine (`app/ml/engine.py`):** Runs real-time Anomaly Detection, Multi-Class Fault Classification (Bearing Degradation, Thermal Overload, Electrical Imbalance, Looseness), SHAP Feature Decomposition, and Remaining Useful Life (RUL) estimation.
2. **Interactive 3D WebGL Digital Twin (Three.js):**
   - Procedural 3D CNC Spindle and Bearing assembly with mouse/touch orbit, scroll zoom, and real-time hotspot inspection (`Spindle Bearing`, `Thermal Casing`, `Drive Inverter`).
3. **Web Audio API Industrial SFX Synthesizer:**
   - Synthesizes crisp cyber-industrial UI chirps and frequency-modulated dual-tone warning sirens on anomaly/fault triggers without external audio assets.
4. **Live FFT Harmonic Vibration Spectrogram:**
   - Real-time 60 FPS HTML5 Canvas spectrogram visualizing fundamental rotational frequency (1X), harmonic spikes (2X, 3X), and outer race bearing defect harmonics (BPFO at 184 Hz).
5. **Standalone Security Gateway Login Portal:**
   - Industrial security login (`/login`) with 1-click role presets (Reliability Engineer, Plant Operations Manager, Administrator), password visibility toggle, and physical RFID card swipe simulation.
6. **Built-in Conversational AI Copilot:**
   - Context-aware diagnostic assistant grounded in live telemetry database state for natural language troubleshooting.

---

## 📁 Project Architecture & Structure

```
factorymind/
│
├── start_all.bat              # Master Interactive 1-Click Launcher (Python Backend + 3D Console + IoT Streamer)
├── run_backend.bat            # 1-Click launcher for FastAPI Server & Live Web Dashboard
├── run_java_gateway.bat       # 1-Click launcher for Java Industrial Edge Gateway
├── run_simulator.bat          # 1-Click launcher for Python IoT Telemetry Streamer
├── run_mobile.bat             # 1-Click launcher for Flutter Mobile App
├── README.md                  # Comprehensive platform documentation
│
├── java-edge-gateway/         # JAVA INDUSTRIAL IIoT EDGE GATEWAY
│   └── src/com/factorymind/gateway/
│       └── IndustrialEdgeGateway.java  # Pure Java 21 edge daemon (Concurrent PLC polling & HTTP/JSON ingestion)
│
├── backend/                   # PYTHON FASTAPI & PREDICTIVE ML ENGINE
│   ├── requirements.txt       # Dependencies (FastAPI, Uvicorn, SQLAlchemy, Pydantic v2)
│   ├── seed_data.py           # Populates 6 industrial machines & initial telemetry
│   ├── factorymind.db         # Persistent SQLite database
│   ├── app/
│   │   ├── main.py            # FastAPI Application Entrypoint (/login, /dashboard, /api/v1)
│   │   ├── core/              # Config & SQLAlchemy Engine
│   │   ├── models/            # ORM Models (Users, Machines, Sensors, Predictions, Alerts, Work Orders)
│   │   ├── schemas/           # Pydantic v2 Request/Response Validation Schemas
│   │   ├── ml/
│   │   │   └── engine.py      # Core Anomaly Scoring, Multi-Class Classifier, SHAP XAI & RUL Estimator
│   │   └── api/               # Modular REST API Endpoints:
│   │       ├── auth.py        # Authentication & Role Gateway (Admin, Engineer, Manager)
│   │       ├── machines.py    # Machine catalog & metadata
│   │       ├── telemetry.py   # Multi-sensor ingestion & history
│   │       ├── predictions.py # ML diagnostics & SHAP feature impacts
│   │       ├── alerts.py      # Automated threshold & anomaly triggers
│   │       ├── maintenance.py # Work order dispatch & technician workflow
│   │       ├── analytics.py   # MTBF, MTTR, prevented downtime & accuracy metrics
│   │       └── copilot.py     # AI Plant Copilot Assistant with live database grounding
│   ├── static/                # 3D CYBER-INDUSTRIAL WEB CONSOLE
│   │   ├── login.html         # Standalone Security Gateway Login Portal & RFID tap
│   │   ├── index.html         # High-tech dashboard: 2.5D floor map + 3D WebGL Hologram + FFT Spectrogram
│   │   ├── style.css          # Hologram grids, cyber-industrial neon styling & print styles
│   │   └── app.js             # Three.js 3D engine, Web Audio synthesizer, FFT spectrogram & live polling
│   └── simulator/
│       └── iot_simulator.py   # Python IoT Multi-Sensor Streamer with interactive Fault Injection
│
└── mobile/                    # FLUTTER MOBILE APPLICATION
    ├── pubspec.yaml           # Flutter Dependencies (Riverpod, GoRouter, fl_chart, Dio)
    └── lib/
        ├── main.dart          # Mobile Entrypoint with Riverpod ProviderScope
        ├── core/              # Theme (Slate Dark Mode), Constants, GoRouter with Shell Navigation
        ├── models/            # Dart Models (Machine, Prediction, Alert, WorkOrder)
        ├── services/          # Dio REST API Client with Mock Fallback
        └── features/          # Screens: Dashboard, Machines, Alerts, Maintenance, Digital Twin
```

---

## 🚀 Quick Start Guide

### Option 1: Master 1-Click Launcher (Recommended)
Double-click:
```cmd
start_all.bat
```
This opens the interactive menu:
- `[1]` Starts the **Python FastAPI Backend**, launches the **3D Web Console** in your browser, and starts the **IoT Telemetry Streamer**.
- `[2]` Starts Python AI Backend Server only.
- `[3]` Starts the **Java Industrial Edge Gateway**.
- `[4]` Starts the Python IoT Telemetry Streamer.
- `[5]` Opens the Web Console in your default browser (`http://127.0.0.1:8000/login`).

---

### Option 2: Running the Java Industrial Edge Gateway
If you have Java (JDK 17 or 21) installed:
```cmd
run_java_gateway.bat
```
This automatically compiles `IndustrialEdgeGateway.java` into bytecode and streams live multi-sensor PLC frames directly into the Python AI backend at `http://127.0.0.1:8000/api/v1/telemetry/ingest`.

---

## 🔑 Demo Access Profiles

| Role | Email | Password | Viva / Demo Function |
| :--- | :--- | :--- | :--- |
| **Reliability Engineer** | `engineer@factorymind.io` | `engineer123` | Sensor calibration, 3D hotspot inspection, work orders |
| **Plant Operations Manager** | `manager@factorymind.io` | `manager123` | Fleet health KPI, shift executive report, downtime ROI |
| **Factory Administrator** | `admin@factorymind.io` | `admin123` | Full asset configuration, security settings |

---

## 🌐 URLs & Endpoints

- **Standalone Login Portal:** [http://127.0.0.1:8000/login](http://127.0.0.1:8000/login)
- **3D Digital Twin Web Console:** [http://127.0.0.1:8000/dashboard](http://127.0.0.1:8000/dashboard)
- **Interactive Swagger API Docs:** [http://127.0.0.1:8000/api/v1/docs](http://127.0.0.1:8000/api/v1/docs)
- **Alternative ReDoc API Docs:** [http://127.0.0.1:8000/api/v1/redoc](http://127.0.0.1:8000/api/v1/redoc)
