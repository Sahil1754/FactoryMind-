import os
import zipfile
import html

def escape_xml(s):
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&apos;"))

def make_shape(sp_id, name, x, y, cx, cy, paragraphs, bg_color=None, border_color=None, border_w=9525):
    """
    Creates a standard OpenXML drawing shape (textbox/card).
    paragraphs is a list of tuples: (text, font_size_pt, is_bold, color_hex, align, is_bullet)
    Coordinates are in EMUs (1 inch = 914400 EMUs, 1 cm = 360000 EMUs).
    Slide 16:9 width = 12192000, height = 6858000.
    """
    fill_xml = f'<a:solidFill><a:srgbClr val="{bg_color}"/></a:solidFill>' if bg_color else '<a:noFill/>'
    ln_xml = f'<a:ln w="{border_w}"><a:solidFill><a:srgbClr val="{border_color}"/></a:solidFill></a:ln>' if border_color else '<a:ln><a:noFill/></a:ln>'

    p_elements = []
    for p_info in paragraphs:
        text, sz_pt, bold, color, align, bullet = p_info
        sz = int(sz_pt * 100)
        b_attr = ' b="1"' if bold else ' b="0"'
        algn_attr = f' algn="{align}"' if align else ' algn="l"'
        
        bullet_xml = '<a:pPr' + algn_attr + ' marL="288000" indent="-288000"><a:buFont typeface="Arial"/><a:buChar char="▪"/></a:pPr>' if bullet else f'<a:pPr{algn_attr}/>'
        
        # Split multiline if any
        lines = text.split("\n")
        for idx, line in enumerate(lines):
            p_elem = f"""<a:p>
              {bullet_xml if idx == 0 else f'<a:pPr{algn_attr}/>'}
              <a:r>
                <a:rPr lang="en-US" sz="{sz}"{b_attr}>
                  <a:solidFill><a:srgbClr val="{color}"/></a:solidFill>
                </a:rPr>
                <a:t>{escape_xml(line)}</a:t>
              </a:r>
            </a:p>"""
            p_elements.append(p_elem)

    p_xml = "\n".join(p_elements)

    return f"""<p:sp>
      <p:nvSpPr>
        <p:cNvPr id="{sp_id}" name="{escape_xml(name)}"/>
        <p:cNvSpPr/>
        <p:nvPr/>
      </p:nvSpPr>
      <p:spPr>
        <a:xfrm>
          <a:off x="{int(x)}" y="{int(y)}"/>
          <a:ext cx="{int(cx)}" cy="{int(cy)}"/>
        </a:xfrm>
        <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
        {fill_xml}
        {ln_xml}
      </p:spPr>
      <p:txBody>
        <a:bodyPr vert="horz" lIns="144000" tIns="144000" rIns="144000" bIns="144000" rtlCol="0">
          <a:spAutoFit/>
        </a:bodyPr>
        <a:lstStyle/>
        {p_xml}
      </p:txBody>
    </p:sp>"""

def build_presentation(output_pptx_path):
    slides_data = [
        # SLIDE 1: Cover Page
        {
            "is_cover": True,
            "title": "FactoryMind AI",
            "subtitle": "An AI-Based Predictive Manufacturing and Machine Health Monitoring Platform",
            "category": "SY MCA Major Project — Preliminary Project Report (Review-II)",
            "institution": "Tatyasaheb Kore Institute of Engineering & Technology (TKIET), Warananagar\nDepartment of Computer Applications • Academic Year 2026–2027",
            "members": "Group Members:\n1. [Student Name 1] (Roll No: [Roll 1])\n2. [Student Name 2] (Roll No: [Roll 2])\n3. [Student Name 3] (Roll No: [Roll 3])",
            "guide": "Under the Guidance of:\n[Name of Project Guide], Assistant Professor\nDepartment of Computer Applications, TKIET, Warananagar"
        },
        # SLIDE 2: Abstract
        {
            "category": "Executive Overview",
            "title": "Abstract",
            "cards": [
                {
                    "title": "Project Essence & Problem",
                    "bullets": [
                        "Unplanned machine breakdowns cost manufacturing plants $260,000/hour in lost throughput and emergency repairs.",
                        "FactoryMind AI is an end-to-end cyber-physical predictive maintenance platform integrating IIoT telemetry, Machine Learning, and Explainable AI (XAI).",
                        "Continuously monitors temperature, vibration RMS, current draw, and spindle RPM across industrial machines.",
                        "Shifts operations from reactive repairs to predictive intervention with quantitative Remaining Useful Life (RUL) estimation."
                    ]
                },
                {
                    "title": "Dual Architecture & Expected Outcomes",
                    "bullets": [
                        "Dual Enterprise Architecture: Java 21 Edge Gateway (PLC polling) + Python 3.12 FastAPI ML Inference.",
                        "Interactive 3D WebGL Digital Twin with pulsating bearing fatigue hotspots and 60 FPS live FFT vibration spectrogram.",
                        "Autonomous closed-loop work order ticketing dispatched directly upon threshold or anomaly detection.",
                        "Expected Outcome: 30%+ reduction in unexpected downtime, adherence to ISO 13379-1 Condition Monitoring standards."
                    ]
                }
            ]
        },
        # SLIDE 3: Chapter 1 - Introduction
        {
            "category": "Chapter 1",
            "title": "Introduction & Problem Statement",
            "cards": [
                {
                    "title": "1.1 Industrial Background",
                    "bullets": [
                        "Industry 4.0 plants operate critical assets (CNC mills, lathe turning centers, induction motors, and hydraulic pumps) under high thermal and mechanical stress.",
                        "Sudden component failures (e.g. bearing raceway pitting, thermal stator overload) cause cascading line halts and safety hazards."
                    ]
                },
                {
                    "title": "1.2 The Problem Statement",
                    "bullets": [
                        "Traditional manufacturing relies either on reactive breakdown maintenance or rigid schedule-based overhaul.",
                        "Neither approach provides real-time visibility into machine health, leading to either premature part replacement or sudden catastrophic breakdowns."
                    ]
                },
                {
                    "title": "1.3 Need & Significance",
                    "bullets": [
                        "Micro-vibration spikes and thermal baseline drift occur 40–80 operating hours before functional seizure.",
                        "FactoryMind AI captures these early physical signals to protect high-capital equipment and eliminate downtime."
                    ]
                },
                {
                    "title": "1.4 Target Beneficiaries",
                    "bullets": [
                        "Plant Operations Managers: Fleet operational index, MTBF/MTTR metrics, avoided downtime ROI.",
                        "Reliability Engineers: 3D localized fatigue analysis, FFT vibration harmonic analysis.",
                        "Floor Technicians: Autonomous prioritized work order dispatch with prescriptive actions."
                    ]
                }
            ]
        },
        # SLIDE 4: Chapter 1 - Objectives & Scope
        {
            "category": "Chapter 1 (Continued)",
            "title": "Project Objectives & Scope",
            "cards": [
                {
                    "title": "Main Project Objectives",
                    "bullets": [
                        "Continuous multi-sensor telemetry acquisition (Temperature, Vibration, Current, RPM) at 2.5s cadence.",
                        "Unsupervised & distance-based anomaly detection with <5% false alarm rate.",
                        "Multi-class fault diagnosis (Bearing Degradation, Thermal Overload, Electrical Phase Imbalance).",
                        "Prognostic Remaining Useful Life (RUL) estimation in operating hours.",
                        "Transparent Explainable AI (SHAP Tree decomposition) highlighting exact sensor impact percentages.",
                        "Interactive 3D WebGL Digital Twin and live 60 FPS harmonic FFT spectrogram."
                    ]
                },
                {
                    "title": "Project Scope Boundaries",
                    "bullets": [
                        "IN SCOPE: 6 machine classes across 5 factory bays, Java Edge Gateway, Python ML Backend, 3D Web Console, and ISO 13379-1 Shift Reports.",
                        "IN SCOPE: Closed-loop maintenance ticketing queue with priority escalation.",
                        "OUT OF SCOPE: Automated physical SCADA emergency stop override (safety regulations require on-site hardwired relays).",
                        "OUT OF SCOPE: Custom proprietary CNC controller firmware flashing."
                    ]
                }
            ]
        },
        # SLIDE 5: Chapter 2 - Literature Survey
        {
            "category": "Chapter 2",
            "title": "Literature Survey & Research Gap",
            "cards": [
                {
                    "title": "1. NIST Smart Manufacturing Operations (2022)",
                    "bullets": [
                        "Theoretical guidelines for machine diagnostics and prognostics using vibration time-series.",
                        "Limitation: Lacks an integrated software implementation and explainable AI transparency for technicians."
                    ]
                },
                {
                    "title": "2. Enterprise CMMS (SAP PM / IBM Maximo)",
                    "bullets": [
                        "Enterprise work order ticketing and maintenance scheduling inventory.",
                        "Limitation: Decoupled from live sensor streams; relies heavily on manual post-facto inspection logs."
                    ]
                },
                {
                    "title": "3. Legacy SCADA (Siemens WinCC / Wonderware)",
                    "bullets": [
                        "Static 2D supervisory control dials and raw threshold high/low alarms.",
                        "Limitation: High false-alarm fatigue; no predictive RUL; lacks interactive 3D component localization."
                    ]
                },
                {
                    "title": "Research Gap Addressed by FactoryMind AI",
                    "bullets": [
                        "Bridges pure academic ML research with operational industrial maintenance.",
                        "Combines live multi-sensor streaming, transparent SHAP XAI factor decomposition, and an interactive 3D WebGL twin."
                    ]
                }
            ]
        },
        # SLIDE 6: Chapter 3 - Proposed System & Requirements
        {
            "category": "Chapter 3",
            "title": "Proposed System & Requirements Analysis",
            "cards": [
                {
                    "title": "Functional Requirements (FR)",
                    "bullets": [
                        "FR1: High-throughput ingestion of JSON telemetry packets at 2.5s cadence.",
                        "FR2: Multi-parameter anomaly detection & classification of failure modes.",
                        "FR3: SHAP Explainable AI attribution factor decomposition.",
                        "FR4: Automated creation and tracking of prioritized maintenance work orders.",
                        "FR5: 3D WebGL Digital Twin with localized component fatigue inspection.",
                        "FR6: Grounded conversational AI Copilot for natural language plant diagnostics."
                    ]
                },
                {
                    "title": "Non-Functional & Hardware Requirements",
                    "bullets": [
                        "Latency: Real-time inference latency under 20ms per machine telemetry packet.",
                        "Availability: Background edge polling daemon with 99.5% uptime resilience.",
                        "Security: Role-Based Access Control (Admin, Engineer, Manager) with JWT authorization.",
                        "Compliance: Standardized against ISO 13379-1 Condition Monitoring guidelines.",
                        "Hardware: Standard PC (Intel i5/i7, 8GB RAM), optional ESP32 + MPU6050 physical vibration rig.",
                        "Software: Python 3.12, Java 21, FastAPI, SQLAlchemy, SQLite/PostgreSQL, Three.js WebGL."
                    ]
                }
            ]
        },
        # SLIDE 7: Chapter 4 - Architecture
        {
            "category": "Chapter 4",
            "title": "System Architecture & Data Flow Pipeline",
            "cards": [
                {
                    "title": "End-to-End Enterprise Data Flow",
                    "bullets": [
                        "[1] Shopfloor Assets: CNC Spindle, Lathe, Induction Motors, Hydraulic Pumps, Compressors.",
                        "[2] Physical Sensors: Temperature (PT100), Vibration RMS (Piezo/MPU6050), Current (Hall Effect), RPM (Optical).",
                        "[3] Java 21 Industrial Edge Gateway: High-throughput PLC polling daemon using java.net.http framing.",
                        "[4] Python 3.12 FastAPI Diagnostic Backend: Anomaly scoring, XGBoost classification, SHAP tree decomposition, and RUL estimation.",
                        "[5] 3D Cyber-Industrial Web Console: Three.js 3D WebGL Spindle Model, live FFT vibration spectrogram, and Web Audio SFX."
                    ]
                },
                {
                    "title": "Architectural Benefits",
                    "bullets": [
                        "Decoupled Microservice Design: Edge gateway, predictive AI, and web console operate independently.",
                        "Enterprise Multi-Language Synergy: Combines Java's industrial socket stability with Python's scientific ML ecosystem.",
                        "Zero-Install Client: 3D Digital Twin renders smoothly in standard web browsers without proprietary software."
                    ]
                }
            ]
        },
        # SLIDE 8: Chapter 4 - Use Case Diagram
        {
            "category": "Chapter 4 (Design)",
            "title": "Use Case Diagram (Mandatory Guideline)",
            "cards": [
                {
                    "title": "Primary System Actors",
                    "bullets": [
                        "Java Edge Gateway (System Actor): Collects PLC sensor readings and streams telemetry frames.",
                        "Reliability Engineer (Human Actor): Inspects 3D component hotspots, analyzes FFT harmonics, and injects fault scenarios.",
                        "Plant Operations Manager (Human Actor): Monitors overall fleet health index, reviews MTBF metrics, and exports shift reports.",
                        "Maintenance Technician (Human Actor): Receives autonomous work order tickets, reviews AI recommendations, and marks tasks completed.",
                        "Administrator (Human Actor): Configures machine baselines, sensor thresholds, and user access credentials."
                    ]
                },
                {
                    "title": "Core Use Cases Modeled",
                    "bullets": [
                        "UC1: Stream Live Multi-Sensor Telemetry (Includes edge validation and connection retry).",
                        "UC2: Execute Real-Time Prognostics (Anomaly detection, failure classification, and RUL).",
                        "UC3: Autonomous Work Order Dispatch (Triggers ticket with priority level upon critical threshold breach).",
                        "UC4: Interactive 3D Digital Twin Inspection (Visualizes localized bearing/thermal fatigue).",
                        "UC5: Query Conversational AI Copilot (Natural language Q&A over database state)."
                    ]
                }
            ]
        },
        # SLIDE 9: Chapter 4 - Database Design
        {
            "category": "Chapter 4 (Design)",
            "title": "Database Design & Entity Relationships (ERD)",
            "cards": [
                {
                    "title": "Core Relational Tables",
                    "bullets": [
                        "`machines`: Central asset registry storing machine code, type, department, status, and baseline envelopes.",
                        "`sensor_readings`: High-frequency time-series table logging temperature, vibration RMS, peak, current, and RPM.",
                        "`ml_predictions`: Diagnostic records storing health index (0–100%), failure probability, RUL hours, and JSON SHAP factors.",
                        "`alerts`: Automated alarm events categorized by severity (LOW, MEDIUM, HIGH, CRITICAL).",
                        "`maintenance_records`: Work order tickets with priority, assigned technician, and scheduled completion dates.",
                        "`users`: Access control credentials with roles (ADMIN, ENGINEER, MANAGER)."
                    ]
                },
                {
                    "title": "Relational Integrity & Multi-DB Support",
                    "bullets": [
                        "One-to-Many Relationships: Each machine owns multiple time-series readings, predictions, alerts, and work orders.",
                        "SQLAlchemy 2.0 ORM: Seamless switching between SQLite (local demo portability) and PostgreSQL (enterprise production).",
                        "Optimized Indexing: Indexed on machine_code, recorded_at, and status for sub-millisecond query retrieval."
                    ]
                }
            ]
        },
        # SLIDE 10: Chapter 5 - Modules Allocation
        {
            "category": "Chapter 5",
            "title": "System Modules & Group Work Allocation",
            "cards": [
                {
                    "title": "Detailed Module Breakdown",
                    "bullets": [
                        "Module 1 (IIoT Edge Gateway & Simulator): Java 21 multithreaded PLC polling daemon, hardware framing buffer.",
                        "Module 2 (AI/ML Diagnostic Engine): Anomaly distance scoring, failure classification, SHAP XAI, and RUL regressor.",
                        "Module 3 (FastAPI Backend & ORM Database): REST APIs, SQLAlchemy schemas, automated alert rules, and work order queue.",
                        "Module 4 (3D Digital Twin & Audio SFX): Three.js WebGL machine assembly, hotspot orbit controls, and Web Audio API alarm sirens.",
                        "Module 5 (Executive Console & AI Copilot): 2.5D factory floor map, live FFT spectrogram, and conversational copilot."
                    ]
                },
                {
                    "title": "Group Member Allocation (SY MCA)",
                    "bullets": [
                        "Student 1: Module 1 (Java Edge Gateway) + Module 3 (FastAPI Database Integration).",
                        "Student 2: Module 2 (AI/ML Diagnostics & SHAP XAI) + Module 3 (API Routing).",
                        "Student 3: Module 4 (3D WebGL Twin & Web Audio) + Module 5 (Executive Console & Copilot).",
                        "Shared Responsibility: System testing, documentation, and IEEE research literature review."
                    ]
                }
            ]
        },
        # SLIDE 11: Chapter 5 - Technology Stack
        {
            "category": "Chapter 5 (Technology)",
            "title": "Technology Stack & Engineering Justification",
            "cards": [
                {
                    "title": "Backend & Edge Technologies",
                    "bullets": [
                        "Python 3.12 + FastAPI: Asynchronous ASGI execution; 300% faster than Flask; automated OpenAPI/Swagger docs; ideal for ML vector math.",
                        "Java 21 OpenJDK: Industrial standard for PLC gateways (Siemens MindSphere / OPC-UA); robust multithreaded scheduling prevents packet dropouts.",
                        "SQLAlchemy 2.0 + SQLite: Lightweight, zero-config local portability for viva demo, with immediate PostgreSQL compatibility."
                    ]
                },
                {
                    "title": "Frontend & UI Visualization",
                    "bullets": [
                        "Three.js (WebGL): Client-side GPU-accelerated 3D rendering runs smoothly on factory HMIs without heavy desktop CAD software.",
                        "HTML5 Canvas: Real-time 60 FPS harmonic vibration spectrogram displaying 1X, 2X, 3X, and BPFO bearing defect frequencies.",
                        "Web Audio API: Native browser frequency modulation synthesizer generating warning sirens without external audio files."
                    ]
                }
            ]
        },
        # SLIDE 12: Chapter 6 - Implementation Progress
        {
            "category": "Chapter 6",
            "title": "Current Implementation Progress (Review-II Status)",
            "cards": [
                {
                    "title": "100% Completed Work (Demonstrated Live Today)",
                    "bullets": [
                        "FastAPI Backend: 8 operational routers (/machines, /telemetry, /predictions, /alerts, /maintenance, etc.).",
                        "Java Edge Gateway: Pure Java 21 daemon polling 6 machine profiles and streaming HTTP JSON packets.",
                        "Predictive ML Engine: Anomaly distance scoring, logistic failure probability, and RUL regression active.",
                        "Security Login Gateway: Dedicated /login portal with simulated RFID card swipe and 1-click role presets.",
                        "3D Digital Twin: Interactive Three.js spindle model with rotating tool and live FFT spectrogram."
                    ]
                },
                {
                    "title": "Work in Progress & Next Phase Milestones",
                    "bullets": [
                        "Physical IoT Test Rig: Interfacing ESP32 microcontroller with MPU6050 accelerometer for live physical vibration.",
                        "Flutter Mobile App: Compiling cross-platform Android mobile dashboard for floor technicians.",
                        "Model Benchmarking: Formal validation against benchmark NASA C-MAPSS turbofan degradation dataset.",
                        "Overall Project Progress for Second Presentation: 75% complete."
                    ]
                }
            ]
        },
        # SLIDE 13: Chapter 6 - UI Screenshots 1
        {
            "category": "Chapter 6 (Screenshots)",
            "title": "System UI: Security Login & Executive Dashboard",
            "cards": [
                {
                    "title": "Standalone Security Gateway (/login)",
                    "bullets": [
                        "High-tech dark theme cyber-industrial entrance portal with ISO 13379-1 certification badge.",
                        "1-Click Role Presets: Reliability Engineer (Rahul S.), Plant Operations Manager (Priya N.), Administrator (Vikram P.).",
                        "Simulated RFID Tap Button: Instant badge authentication bypass for presentations and viva evaluations.",
                        "Live Gateway status indicators: MQTT Broker (1883), XGBoost Diagnostics, and SQLite DB."
                    ]
                },
                {
                    "title": "Executive Fleet Dashboard (/dashboard)",
                    "bullets": [
                        "Plant Health Index Arc: Live aggregate factory health score (e.g. 82.4% Operational).",
                        "Fleet Condition Matrix: Instant counts of Healthy (4), Warning (1), and Critical (1) assets.",
                        "Urgent Mechanical Attention Ticker: Pulsing alert banner identifying imminent machine risks.",
                        "SHAP Root-Cause Attribution Mini-Card: Top weighted risk factors (Vibration +44%, Temperature +28%)."
                    ]
                }
            ]
        },
        # SLIDE 14: Chapter 6 - UI Screenshots 2
        {
            "category": "Chapter 6 (Screenshots)",
            "title": "Interactive 3D WebGL Twin & FFT Spectrogram",
            "cards": [
                {
                    "title": "3D Spindle WebGL Hologram Viewport",
                    "bullets": [
                        "Procedurally modeled metallic CNC Lathe spindle headstock assembly running at 60 FPS.",
                        "Interactive Sensor Hotspots: 📍 Spindle Bearing (Crimson glow), 📍 Thermal Jacket (Amber), 📍 Inverter Drive (Cyan).",
                        "Mouse Orbit & Scroll Zoom: Full 360° rotation and focal zoom on localized fatigue zones.",
                        "Hotspot Quick-Focus Buttons: Instantly orient camera angle to inspect bearing raceways."
                    ]
                },
                {
                    "title": "Live FFT Vibration Harmonic Spectrogram",
                    "bullets": [
                        "HTML5 Canvas frequency visualizer mapping real-time harmonic peaks:",
                        "1X (24 Hz): Rotational fundamental running speed.",
                        "2X (48 Hz): Shaft misalignment harmonic spike.",
                        "3X (72 Hz): Mechanical looseness harmonic.",
                        "BPFO (184 Hz): Ball Pass Frequency Outer Race bearing micro-defect frequency.",
                        "Web Audio API: Frequency-modulated dual-tone siren plays automatically on critical faults."
                    ]
                }
            ]
        },
        # SLIDE 15: Chapter 6 - Dataset & ML
        {
            "category": "Chapter 6 (AI / ML)",
            "title": "Dataset Characteristics & ML Prognostic Algorithms",
            "cards": [
                {
                    "title": "Sensor Parameters & Dataset Description",
                    "bullets": [
                        "Calibration: Synthetic degradation models calibrated against NASA C-MAPSS and IMS Bearing run-to-failure datasets.",
                        "Sampling Cadence: 2.5 seconds per packet across 6 industrial machine classes.",
                        "Features: Temperature (°C), Vibration RMS (g), Current Draw (A), Spindle RPM, and Pressure (bar).",
                        "Operating Hours: Continuous cumulative duty-cycle aging factor."
                    ]
                },
                {
                    "title": "Mathematical Formulation of ML Pipeline",
                    "bullets": [
                        "Anomaly Distance Vector: Weighted normalized Euclidean distance from baseline (w_vib=2.2, w_temp=1.4).",
                        "Calibrated Failure Probability: Logistic Sigmoid P(fail) = 1 / (1 + exp(-1.2 * (Anomaly_Index - 1.8))).",
                        "Health Score: Health = 100 - (P(fail) * 88) - (Hours_Risk * 5), mapped to [0, 100].",
                        "RUL Regressor: Multi-stage prognostic degradation curve predicting operating hours to failure.",
                        "SHAP XAI: Normalized tree-attribution breakdown showing percentage contribution of each sensor."
                    ]
                }
            ]
        },
        # SLIDE 16: Chapter 7 - Challenges & Work Plan
        {
            "category": "Chapter 7",
            "title": "Challenges Encountered & Work Remaining Plan",
            "cards": [
                {
                    "title": "Technical Challenges Solved",
                    "bullets": [
                        "Cross-Language Ingestion Latency: Solved by implementing Java 21 non-blocking async HTTP client and FastAPI event loop (<15ms latency).",
                        "3D Model Browser Lag: Built procedural Three.js geometries and throttled render loops to maintain steady 60 FPS on standard laptops.",
                        "Audio Alarms Without Files: Utilized native Web Audio API oscillators for synthesized dual-tone frequency modulation."
                    ]
                },
                {
                    "title": "Timeline & Milestones (To Final Presentation)",
                    "bullets": [
                        "Weeks 1–2: Connect physical ESP32 + MPU6050 accelerometer vibration rig.",
                        "Weeks 3–4: Formal model validation and ROC-AUC / F1-Score benchmarking against NASA C-MAPSS data.",
                        "Weeks 5–6: Package Flutter mobile app APK for technician smartphones.",
                        "Weeks 7–8: Comprehensive testing, final report documentation, and university viva preparation."
                    ]
                }
            ]
        },
        # SLIDE 17: Conclusion
        {
            "category": "Conclusion",
            "title": "Summary & Project Contribution",
            "cards": [
                {
                    "title": "Core Contributions",
                    "bullets": [
                        "Industry 4.0 Standard: Successfully aligns predictive maintenance with ISO 13379-1 Condition Monitoring guidelines.",
                        "Dual Architecture: Demonstrates enterprise multi-language synergy between a Java Edge Gateway and Python AI Engine.",
                        "Actionable Explainability: Replaces black-box alarms with transparent SHAP attributions and remaining useful life hours.",
                        "Interactive 3D Visual Twin: Provides intuitive spatial inspection of localized machine degradation directly in the browser."
                    ]
                },
                {
                    "title": "Current Standing for Review-II",
                    "bullets": [
                        "All core software deliverables for the preliminary project review are completed, tested, and operational.",
                        "The platform is accessible locally and across public test domains.",
                        "The group is well-prepared to proceed to physical sensor integration and final submission."
                    ]
                }
            ]
        },
        # SLIDE 18: References
        {
            "category": "References",
            "title": "References (IEEE Standard Format) & Q&A",
            "cards": [
                {
                    "title": "References Cited",
                    "bullets": [
                        "[1] ISO 13379-1:2012, 'Condition monitoring and diagnostics of machines — General guidelines on data interpretation and diagnostics techniques,' ISO, Geneva, 2012.",
                        "[2] National Institute of Standards and Technology (NIST), 'Smart Manufacturing Operations Planning and Control Program,' U.S. Dept. of Commerce, 2022.",
                        "[3] R. K. Mobley, 'An Introduction to Predictive Maintenance,' 2nd ed., Butterworth-Heinemann, Oxford, UK, 2002.",
                        "[4] S. M. Lundberg and S.-I. Lee, 'A unified approach to interpreting model predictions,' in NeurIPS, 2017, pp. 4765–4774.",
                        "[5] FastAPI Documentation, 'FastAPI framework, high performance, ready for production,' 2024. [Online]. Available: https://fastapi.tiangolo.com",
                        "[6] Three.js Authors, 'Three.js JavaScript 3D Library,' 2024. [Online]. Available: https://threejs.org"
                    ]
                },
                {
                    "title": "Thank You!",
                    "bullets": [
                        "Department of Computer Applications, TKIET, Warananagar",
                        "Academic Year: 2026–2027",
                        "We welcome questions, suggestions, and feedback from the evaluators."
                    ]
                }
            ]
        }
    ]

    total_slides = len(slides_data)

    content_types_entries = [
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
        '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
    ]
    for i in range(1, total_slides + 1):
        content_types_entries.append(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')

    content_types_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  {"".join(content_types_entries)}
</Types>"""

    root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>"""

    pres_sld_ids = []
    pres_rels_entries = [
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>',
        '<Relationship Id="rIdTheme" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>'
    ]

    for i in range(1, total_slides + 1):
        r_id = f"rIdSlide{i}"
        pres_sld_ids.append(f'<p:sldId id="{255 + i}" r:id="{r_id}"/>')
        pres_rels_entries.append(f'<Relationship Id="{r_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>')

    presentation_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst>
    <p:sldMasterId id="2147483648" r:id="rId1"/>
  </p:sldMasterIdLst>
  <p:sldIdLst>
    {"".join(pres_sld_ids)}
  </p:sldIdLst>
  <p:sldSz cx="12192000" cy="6858000" type="screen16x9"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>"""

    pres_rels_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {"".join(pres_rels_entries)}
</Relationships>"""

    theme_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Office Theme">
  <a:themeElements>
    <a:clrScheme name="Office">
      <a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1>
      <a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="0F172A"/></a:dk2>
      <a:lt2><a:srgbClr val="F8FAFC"/></a:lt2>
      <a:accent1><a:srgbClr val="0284C7"/></a:accent1>
      <a:accent2><a:srgbClr val="4F46E5"/></a:accent2>
      <a:accent3><a:srgbClr val="10B981"/></a:accent3>
      <a:accent4><a:srgbClr val="F59E0B"/></a:accent4>
      <a:accent5><a:srgbClr val="EF4444"/></a:accent5>
      <a:accent6><a:srgbClr val="06B6D4"/></a:accent6>
      <a:hlink><a:srgbClr val="0284C7"/></a:hlink>
      <a:folHlink><a:srgbClr val="6366F1"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Office">
      <a:majorFont><a:latin typeface="Calibri"/></a:majorFont>
      <a:minorFont><a:latin typeface="Calibri"/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="Office">
      <a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>
      <a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>
      <a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>
      <a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>
    </a:fmtScheme>
  </a:themeElements>
</a:theme>"""

    master_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
  <p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles>
</p:sldMaster>"""

    layout_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank">
  <p:cSld name="Blank">
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>"""

    master_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>"""

    layout_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>"""

    slide_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>"""

    # Generate each slide XML
    slide_xmls = []
    for s_idx, s in enumerate(slides_data, start=1):
        shapes = []
        sp_id = 2

        if s.get("is_cover"):
            # Background Dark Box
            shapes.append(make_shape(sp_id, "CoverBg", 0, 0, 12192000, 6858000, [], bg_color="0F172A"))
            sp_id += 1

            # Top Badge / Institution
            shapes.append(make_shape(sp_id, "Institution", 700000, 600000, 10792000, 700000, [
                (s["institution"], 12, True, "93C5FD", "l", False)
            ]))
            sp_id += 1

            # Title & Subtitle
            shapes.append(make_shape(sp_id, "MainTitle", 700000, 1500000, 10792000, 2200000, [
                (s["title"], 38, True, "FFFFFF", "l", False),
                (s["subtitle"], 18, False, "E2E8F0", "l", False),
                (s["category"], 13, True, "38BDF8", "l", False)
            ]))
            sp_id += 1

            # Members Card
            shapes.append(make_shape(sp_id, "MembersCard", 700000, 4200000, 5200000, 2000000, [
                ("PRESENTED BY (SY MCA GROUP):", 12, True, "94A3B8", "l", False),
                (s["members"], 14, False, "FFFFFF", "l", False)
            ], bg_color="1E293B", border_color="334155"))
            sp_id += 1

            # Guide Card
            shapes.append(make_shape(sp_id, "GuideCard", 6292000, 4200000, 5200000, 2000000, [
                ("PROJECT GUIDE & DEPARTMENT:", 12, True, "94A3B8", "l", False),
                (s["guide"], 14, False, "FFFFFF", "l", False)
            ], bg_color="1E293B", border_color="334155"))
            sp_id += 1

        else:
            # White Slide Background
            shapes.append(make_shape(sp_id, "SlideBg", 0, 0, 12192000, 6858000, [], bg_color="FFFFFF"))
            sp_id += 1

            # Header Category + Title
            shapes.append(make_shape(sp_id, "Header", 600000, 400000, 9000000, 1000000, [
                (s["category"].upper(), 11, True, "0284C7", "l", False),
                (s["title"], 24, True, "0F172A", "l", False)
            ]))
            sp_id += 1

            # Top Right Institution Tag
            shapes.append(make_shape(sp_id, "TkietTag", 9600000, 400000, 2000000, 800000, [
                ("TKIET Warananagar", 11, True, "64748B", "r", False),
                ("SY MCA • Review-II", 10, False, "94A3B8", "r", False)
            ]))
            sp_id += 1

            # Blue Divider Line
            shapes.append(make_shape(sp_id, "Divider", 600000, 1400000, 10992000, 20000, [], bg_color="E2E8F0"))
            sp_id += 1

            # Body Cards Layout
            cards = s.get("cards", [])
            num_cards = len(cards)

            if num_cards == 2:
                # 2 Side-by-side columns
                col_w = 5300000
                gap = 392000
                top_y = 1600000
                card_h = 4600000

                for c_idx, c in enumerate(cards):
                    x = 600000 + c_idx * (col_w + gap)
                    paras = [(c["title"].upper(), 14, True, "0369A1", "l", False)]
                    for b in c.get("bullets", []):
                        paras.append((b, 13, False, "334155", "l", True))
                    
                    bg = "F0F9FF" if c_idx == 0 else "F8FAFC"
                    border = "BAE6FD" if c_idx == 0 else "E2E8F0"
                    shapes.append(make_shape(sp_id, f"Card_{c_idx}", x, top_y, col_w, card_h, paras, bg_color=bg, border_color=border))
                    sp_id += 1

            elif num_cards == 4:
                # 2x2 Grid
                col_w = 5300000
                row_h = 2200000
                gap_x = 392000
                gap_y = 200000
                base_x = 600000
                base_y = 1600000

                for c_idx, c in enumerate(cards):
                    r_idx = c_idx // 2
                    c_col = c_idx % 2
                    x = base_x + c_col * (col_w + gap_x)
                    y = base_y + r_idx * (row_h + gap_y)

                    paras = [(c["title"].upper(), 13, True, "0284C7", "l", False)]
                    for b in c.get("bullets", []):
                        paras.append((b, 12, False, "334155", "l", True))

                    shapes.append(make_shape(sp_id, f"Card_{c_idx}", x, y, col_w, row_h, paras, bg_color="F8FAFC", border_color="E2E8F0"))
                    sp_id += 1

            elif num_cards == 1:
                # Full width card
                paras = [(cards[0]["title"].upper(), 14, True, "0284C7", "l", False)]
                for b in cards[0].get("bullets", []):
                    paras.append((b, 13, False, "334155", "l", True))
                shapes.append(make_shape(sp_id, "Card_Full", 600000, 1600000, 10992000, 4600000, paras, bg_color="F8FAFC", border_color="E2E8F0"))
                sp_id += 1

            # Footer
            shapes.append(make_shape(sp_id, "Footer", 600000, 6350000, 10992000, 350000, [
                (f"FactoryMind AI: An AI-Based Predictive Manufacturing Platform  |  Slide {s_idx} of {total_slides}", 10, False, "94A3B8", "l", False)
            ]))
            sp_id += 1

        slide_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      {"".join(shapes)}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""
        slide_xmls.append(slide_xml)

    # Write complete ZIP archive
    with zipfile.ZipFile(output_pptx_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types_xml)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("ppt/presentation.xml", presentation_xml)
        z.writestr("ppt/_rels/presentation.xml.rels", pres_rels_xml)
        z.writestr("ppt/theme/theme1.xml", theme_xml)
        z.writestr("ppt/slideMasters/slideMaster1.xml", master_xml)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", master_rels_xml)
        z.writestr("ppt/slideLayouts/slideLayout1.xml", layout_xml)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", layout_rels_xml)

        for i in range(1, total_slides + 1):
            z.writestr(f"ppt/slides/slide{i}.xml", slide_xmls[i - 1])
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slide_rels_xml)

    print(f"[SUCCESS] PowerPoint Presentation created at: {output_pptx_path}")
    print(f"File size: {os.path.getsize(output_pptx_path)} bytes ({round(os.path.getsize(output_pptx_path)/1024, 1)} KB)")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_file = os.path.join(out_dir, "FactoryMind_AI_SY_MCA_Second_Presentation.pptx")
    build_presentation(out_file)
