# FactoryMind AI — Complete System Architecture Blueprint
**Department of Computer Applications, TKIET, Warananagar**  
**SY MCA Major Project (Academic Year: 2026–2027)**  
*Project Title: FactoryMind AI: An AI-Based Predictive Manufacturing and Machine Health Monitoring Platform*

---

## 1. High-Level Cyber-Physical Architecture (4-Tier Model)

FactoryMind AI is structured around a 4-Tier cyber-physical architecture connecting industrial physical assets on the factory floor to an intelligent web console with 3D spatial twin visualization.

```mermaid
flowchart TD
    subgraph TIER1["Tier 1: Physical Machinery & Edge Telemetry"]
        A1["Physical Assets\n(CNC Lathe, Motor, Pump)"] -->|Physical Signals| S1["Multi-Sensor Array\n(MPU-6050, DS18B20, ACS712, RPM)"]
        S1 -->|I2C / Analog / GPIO| E1["ESP32 IoT Edge Node\n(C++ Arduino Firmware)"]
        A1 -->|Modbus TCP / S7| E2["Java 21 Industrial Edge Gateway\n(Daemon / Socket Listener)"]
        E3["Python IoT Telemetry Streamer\n(High-Frequency Test Rig)"]
    end

    subgraph TIER2["Tier 2: Ingestion & API Gateway"]
        E1 -->|HTTP POST /api/v1/telemetry/ingest| API["FastAPI Ingestion Engine\n(Port 8000, Uvicorn Async)"]
        E2 -->|HTTP REST / WebSocket| API
        E3 -->|HTTP POST| API
        AUTH["JWT Token & Role Security\n(bcrypt / Auth Middleware)"] --- API
    end

    subgraph TIER3["Tier 3: AI Diagnostics & Persistence Layer"]
        API --> DB[(SQLite 3 / PostgreSQL\nRelational Schema)]
        API --> ML["FactoryMind ML Diagnostic Engine"]
        ML --> RF["Random Forest Classifier\n(Health Score: 0-100%)"]
        ML --> RUL["RUL Regression Pipeline\n(Remaining Useful Life in Hours)"]
        ML --> SHAP["XAI Feature Importance\n(Transparent Root-Cause Attribution)"]
        ML --> ALERTS["Automated Alert Engine\n(Warning / Critical / Emergency)"]
    end

    subgraph TIER4["Tier 4: Presentation & Digital Twin Client"]
        API -->|JSON REST & Static Serving| WEB["FactoryMind Web Application\n(SPA / HTML5 / CSS3 / ES6)"]
        WEB --> D3["Interactive 3D WebGL Digital Twin\n(Three.js Real-Time Mesh Animation)"]
        WEB --> CH["Live Telemetry Charts\n(Chart.js Multi-Axis Canvas)"]
        WEB --> SFX["Synthesized Cyber Audio Engine\n(Web Audio API Procedural SFX)"]
        WEB --> CF["Cloudflare Public HTTPS Tunnel\n(Global Remote Access for Viva)"]
    end
```

---

## 2. Component Workflow & Data Sequence

The end-to-end lifecycle of a sensor reading from physical mechanical vibration to browser alert is shown below:

```mermaid
sequenceDiagram
    autonumber
    actor Sensor as Machine Sensor (MPU-6050)
    participant Edge as ESP32 / Java Edge Gateway
    participant API as FastAPI Backend (/telemetry/ingest)
    participant ML as ML Inference Engine
    participant DB as Relational Database
    participant UI as 3D Web Console & Audio SFX

    Sensor->>Edge: Read Accel (X,Y,Z), Temp (°C), Current (A), Spindle RPM
    Edge->>Edge: Compute Vibration RMS = sqrt(ax²+ay²+az²) - 1.0g
    Edge->>API: HTTP POST /api/v1/telemetry/ingest (JSON Payload)
    API->>DB: INSERT into sensor_readings table
    API->>ML: analyze_telemetry(temp, vib_rms, curr, rpm, baseline)
    ML->>ML: Calculate Health Score (0-100%) & Predict Failure Mode
    ML->>ML: Estimate RUL (Hours) & Calculate SHAP Impact Weights
    ML-->>API: Return Inference Result Dict
    API->>DB: INSERT into ml_predictions table
    alt Health Score < 70% or Anomaly Detected
        API->>DB: INSERT into alerts table (CRITICAL / WARNING)
        API->>DB: Generate automated maintenance work order
    end
    API-->>Edge: Return HTTP 200 OK + Health Metrics
    UI->>API: Poll /api/v1/machines & /api/v1/telemetry/latest
    API-->>UI: Deliver JSON telemetry + predictions
    UI->>UI: Update 3D Digital Twin mesh color (Green -> Amber -> Red)
    UI->>UI: Plot latest points on Chart.js canvas
    opt Health Score < 50%
        UI->>UI: Trigger Web Audio API Emergency Siren SFX
    end
```

---

## 3. Database Entity Relationship (ER) Schema

FactoryMind AI uses an ACID-compliant relational database schema with full foreign key constraints and automated cascade updates.

```mermaid
erDiagram
    USERS ||--o{ MAINTENANCE_ORDERS : manages
    MACHINES ||--o{ SENSOR_READINGS : logs
    MACHINES ||--o{ ML_PREDICTIONS : generates
    MACHINES ||--o{ ALERTS : triggers
    MACHINES ||--o{ MAINTENANCE_ORDERS : requires

    USERS {
        string id PK "UUID"
        string full_name "Full Name"
        string email UK "Unique Email Address"
        string hashed_password "bcrypt hash"
        string role "admin | operator | technician"
        boolean is_active "Active flag"
        datetime created_at "Timestamp"
    }

    MACHINES {
        string id PK "UUID"
        string machine_code UK "e.g. CNC-001, Motor-003"
        string name "Descriptive Asset Name"
        string machine_type "Milling, Lathe, Pump, Compressor"
        string department "CNC Shop, Hydraulic Bay, Assembly"
        string status "HEALTHY | WARNING | CRITICAL | OFFLINE"
        float baseline_temp "Nominal Temp °C (e.g. 65.0)"
        float baseline_vibration "Nominal Vibration RMS (e.g. 0.35g)"
        float baseline_current "Nominal Current Amps (e.g. 7.5A)"
        float baseline_rpm "Nominal Speed (e.g. 1450.0)"
        integer operating_hours "Cumulative Run Hours"
        datetime created_at "Registration Timestamp"
    }

    SENSOR_READINGS {
        integer id PK "Auto Increment ID"
        string machine_id FK "References MACHINES.id"
        float temperature "Surface Temp °C"
        float vibration_rms "Vibration Velocity RMS (g or mm/s)"
        float vibration_peak "Peak Amplitude (g)"
        float current_amp "Motor Electrical Current (A)"
        float rpm "Spindle Rotational Speed"
        float pressure_bar "Hydraulic/Pneumatic Pressure (Bar)"
        datetime recorded_at "Ingestion Timestamp"
    }

    ML_PREDICTIONS {
        string id PK "UUID"
        string machine_id FK "References MACHINES.id"
        float health_score "0.0% to 100.0%"
        float failure_probability "0.00 to 1.00"
        string predicted_failure_type "NORMAL | BEARING_WEAR | OVERHEATING | MOTOR_IMBALANCE"
        float estimated_rul_hours "Remaining Useful Life in Hours"
        json shap_impact_factors "Top feature contributions"
        string model_version "e.g. rf-ensemble-v2.1"
        datetime predicted_at "Inference Timestamp"
    }

    ALERTS {
        string id PK "UUID"
        string machine_id FK "References MACHINES.id"
        string severity "INFO | WARNING | CRITICAL | EMERGENCY"
        string title "Alert Heading"
        string description "Detailed Root Cause"
        boolean is_acknowledged "Technician Acknowledgement Flag"
        datetime triggered_at "Timestamp"
    }

    MAINTENANCE_ORDERS {
        string id PK "UUID"
        string machine_id FK "References MACHINES.id"
        string user_id FK "Assigned Technician ID"
        string order_title "Work Order Summary"
        string priority "LOW | MEDIUM | HIGH | URGENT"
        string status "PENDING | IN_PROGRESS | COMPLETED"
        datetime scheduled_date "Scheduled Overhaul Date"
        datetime created_at "Creation Timestamp"
    }
```

---

## 4. API Endpoints Contract Matrix

All endpoints are hosted by FastAPI at `http://127.0.0.1:8000` with interactive Swagger UI at `/api/v1/docs`:

| Method | Endpoint | Access Role | Description |
|---|---|---|---|
| `POST` | `/api/v1/auth/login` | Public | Authenticates user credentials via JWT Bearer Token |
| `GET` | `/api/v1/auth/me` | Authenticated | Retrieves current logged-in user profile & role |
| `GET` | `/api/v1/machines/` | Authenticated | Lists all machines with live status and latest sensor metrics |
| `POST` | `/api/v1/machines/` | Admin | Registers a new physical or virtual industrial machine |
| `GET` | `/api/v1/machines/{id}` | Authenticated | Retrieves single machine details and historical diagnostic metrics |
| `POST` | `/api/v1/telemetry/ingest` | Public / Edge | **Primary Ingestion API:** Receives sensor readings, triggers ML inference & alerts |
| `GET` | `/api/v1/telemetry/latest/{code}`| Authenticated | Retrieves the most recent telemetry frame for a machine |
| `GET` | `/api/v1/predictions/` | Authenticated | Lists ML predictions, anomaly probabilities, and RUL forecasts |
| `GET` | `/api/v1/alerts/` | Authenticated | Lists all active and historical alerts filtered by severity |
| `PUT` | `/api/v1/alerts/{id}/ack` | Technician/Admin| Acknowledges an active alert and silences sirens |
| `GET` | `/api/v1/maintenance/` | Authenticated | Lists maintenance work orders and technician assignments |
| `POST` | `/api/v1/maintenance/` | Manager/Admin | Dispatches a new corrective maintenance ticket |
| `GET` | `/api/v1/analytics/overview` | Authenticated | Aggregates plant-wide OEE, health index, and failure breakdowns |
| `GET` | `/presentation` | Public | Serves the SY MCA Review-II Widescreen Interactive Slide Deck |
| `GET` | `/download-ppt` | Public | Direct one-click download of the official Microsoft PowerPoint `.pptx` file |

---

## 5. Technology Stack Specifications

```
+-------------------------------------------------------------------------------+
|                             FACTORYMIND AI STACK                              |
+-------------------------------------------------------------------------------+
|  TIER 1 (IoT & Edge)       |  ESP32 C++ Firmware (WiFi, HTTPClient, ArduinoJson)|
|                            |  Java 21 LTS Edge Gateway (Sockets, Modbus)       |
|                            |  Python High-Frequency IoT Telemetry Simulator   |
+----------------------------+--------------------------------------------------+
|  TIER 2 (Backend & APIs)   |  Python 3.12 64-bit                              |
|                            |  FastAPI (Asynchronous REST & WebSockets)        |
|                            |  Uvicorn ASGI Web Server                         |
|                            |  Pydantic v2 (Strict Schema Data Validation)      |
+----------------------------+--------------------------------------------------+
|  TIER 3 (AI/ML & DB)       |  Scikit-Learn (Random Forest & Gradient Boost)   |
|                            |  NumPy & SciPy (Signal Processing & RMS Math)    |
|                            |  SQLAlchemy 2.0 ORM                              |
|                            |  SQLite 3 (Development) / PostgreSQL (Production) |
+----------------------------+--------------------------------------------------+
|  TIER 4 (Frontend UI/UX)   |  HTML5 & CSS3 Glassmorphism UI (Zero-Build SPA)  |
|                            |  Three.js WebGL (Interactive 3D Digital Twin)    |
|                            |  Chart.js (High-Speed Time-Series Telemetry)     |
|                            |  Web Audio API (Synthesized Procedural SFX)       |
+----------------------------+--------------------------------------------------+
|  NETWORKING & TUNNELING    |  Cloudflare Named/Quick Tunnels (Free HTTPS)     |
|                            |  Localhost Bindings (127.0.0.1:8000)             |
|                            |  start_all.bat (One-Click Windows Orchestrator)  |
+-------------------------------------------------------------------------------+
```

---

## 6. Project Directory File Map

```
C:\Users\Pratiksha\.gemini\antigravity\scratch\factorymind\
│
├── start_all.bat                        <-- Master 1-Click Platform Launcher (Options 1-9)
├── run_free_domain.bat                  <-- Free Public HTTPS Cloudflare Tunnel Launcher
├── run_java_gateway.bat                 <-- Java 21 Industrial Edge Gateway Launcher
├── FactoryMind_AI_SY_MCA_Second_Presentation.pptx  <-- Official Microsoft PowerPoint File
├── presentation.html                    <-- 16:9 Interactive Presentation Slide Deck
├── FACTORYMIND_SECOND_PRESENTATION_PPT.md <-- Slide-by-Slide Viva Speaking Notes
├── HARDWARE_IOT_GUIDE.md                <-- Complete Hardware Wiring & Price Guide
├── hardware_esp32_firmware.ino          <-- Ready-to-flash Arduino C++ Code for ESP32
├── PROJECT_BLUEPRINT.md                 <-- This Complete Architecture Blueprint
│
├── backend/
│   ├── app/
│   │   ├── main.py                      <-- FastAPI Application & Static Mounts
│   │   ├── core/
│   │   │   ├── config.py                <-- Environment & CORS Configuration
│   │   │   ├── database.py              <-- SQLAlchemy Session & Database Engine
│   │   │   └── security.py              <-- Password Hashing & JWT Token Generation
│   │   ├── models/
│   │   │   └── models.py                <-- Database Models (Machines, Telemetry, Alerts)
│   │   ├── schemas/
│   │   │   └── schemas.py               <-- Pydantic Ingest & Response Schemas
│   │   ├── api/
│   │   │   ├── auth.py                  <-- Login & Current User Endpoints
│   │   │   ├── machines.py              <-- Machine Management Endpoints
│   │   │   ├── telemetry.py             <-- Telemetry Ingestion & Real-Time Query
│   │   │   ├── predictions.py           <-- ML Diagnostics & RUL Forecasts
│   │   │   ├── alerts.py                <-- Machine Health Alerts & Acknowledgements
│   │   │   ├── maintenance.py           <-- Maintenance Work Orders
│   │   │   ├── analytics.py             <-- Factory OEE & Health Summary
│   │   │   └── copilot.py               <-- AI Diagnostic Assistant
│   │   └── ml/
│   │       └── engine.py                <-- Random Forest & RUL Prediction Engine
│   ├── simulator/
│   │   └── iot_simulator.py             <-- High-Frequency Multi-Machine IoT Simulator
│   ├── static/
│   │   ├── index.html                   <-- 3D Digital Twin & Live Telemetry Dashboard
│   │   ├── login.html                   <-- Standalone Authentication Portal
│   │   ├── presentation.html            <-- Slide Deck Host
│   │   └── FactoryMind_AI_SY_MCA_Second_Presentation.pptx <-- Downloadable Presentation
│   └── seed_data.py                     <-- Seeds 6 Machines & Initial Sensor Readings
│
└── edge_gateway/
    └── src/
        └── FactoryEdgeGateway.java      <-- Java 21 High-Throughput Edge Daemon
```
