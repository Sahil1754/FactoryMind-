# FactoryMind AI — College Project IoT Hardware Guide & Setup Manual
**Department of Computer Applications, TKIET, Warananagar**  
**SY MCA Major Project (Academic Year: 2026–2027)**

---

## 1. Recommended IoT Hardware Components & Price Breakdown

For a college major project presentation and viva evaluation, you do not need industrial $1,000 sensors. The best, most widely accepted and cost-effective setup uses an **ESP32 Microcontroller** with standard digital and analog sensors.

### Component Price List (Amazon / Robu.in / ElectronicsComp)

| # | Component Name | Model / Specification | Purpose in Project | Approx. Price (INR ₹) | Approx. Price (USD $) |
|---|---|---|---|:---:|:---:|
| 1 | **Main IoT Controller** | ESP32 DevKit V1 (30 or 38 Pin) | Built-in 2.4 GHz Wi-Fi, dual-core 240MHz CPU, reads sensors and sends HTTP POST | ₹380 – ₹450 | $4.50 – $5.50 |
| 2 | **Vibration Sensor** | MPU-6050 (3-Axis Accelerometer + Gyro) | Measures X, Y, Z acceleration to calculate Vibration RMS & Peak | ₹160 – ₹220 | $2.00 – $2.60 |
| 3 | **Temperature Sensor** | DS18B20 (Waterproof Probe) OR DHT22 | Measures machine casing/bearing temperature in °C | ₹120 – ₹190 | $1.50 – $2.30 |
| 4 | **Current Sensor** | ACS712 (5A or 20A Hall Effect Module) | Measures motor electrical current draw in Amperes (A) | ₹130 – ₹180 | $1.60 – $2.20 |
| 5 | **RPM / Speed Sensor** | LM393 Optical Coupler / TCRT5000 IR | Measures spindle rotational speed (RPM) | ₹60 – ₹90 | $0.70 – $1.10 |
| 6 | **Prototyping Kit** | 830-Point Breadboard + 40 Jumper Wires | Solderless connection between ESP32 and sensors | ₹140 – ₹180 | $1.70 – $2.20 |
| 7 | **Demo Rotating Asset** | 5V DC Toy Motor with small propeller/fan | Creates real physical motion and vibration during viva | ₹50 – ₹80 | $0.60 – $1.00 |
| 8 | **USB Cable** | Micro-USB to USB-A data cable | Powers ESP32 and flashes firmware from laptop | ₹50 – ₹80 | $0.60 – $1.00 |
| **TOTAL** | **Complete Hardware Kit** | **Ready for Live Evaluation** | **Full 4-Sensor Industrial Kit** | **₹1,090 – ₹1,470** | **~$13 – $17 USD** |

> **Where to buy in India:**
> - [Robu.in](https://robu.in) (Fast 2-day delivery across Maharashtra)
> - [ElectronicsComp.com](https://www.electronicscomp.com)
> - Amazon India ([amazon.in](https://amazon.in))
> - Local electronic components shops in Warananagar, Kolhapur, or Sangli.

---

## 2. Pin Connection Diagram (Circuit Wiring)

Connect the sensors to the ESP32 pins using standard breadboard jumper wires:

```
                  +-----------------------------------+
                  |          ESP32 DevKit V1          |
                  +-----------------------------------+
                   | 3V3   GND   GPIO21 GPIO22 GPIO34 GPIO35 GPIO18
                   |  |     |      |      |      |      |      |
                   |  |     |      |      |      |      |      |
  +----------------+  |     |      |      |      |      |      |
  | MPU-6050 (Vib)    |     |      |      |      |      |      |
  |   VCC ------------+     |      |      |      |      |      |
  |   GND ------------------+      |      |      |      |      |
  |   SDA -------------------------+      |      |      |      |
  |   SCL --------------------------------+      |      |      |
  +-------------------------------------------------------------+
  | ACS712 (Current)  |     |                    |             |
  |   VCC ------------+     |                    |             |
  |   GND ------------------+                    |             |
  |   OUT ---------------------------------------+ (Analog 34) |
  +-------------------------------------------------------------+
  | Temp Sensor       |     |                           |      |
  |   VCC ------------+     |                           |      |
  |   GND ------------------+                           |      |
  |   DATA ---------------------------------------------+ (GPIO35)|
  +-------------------------------------------------------------+
  | RPM Sensor        |     |                                  |
  |   VCC ------------+     |                                  |
  |   GND ------------------+                                  |
  |   DO (Digital Out)-----------------------------------------+ (GPIO18)
```

---

## 3. Step-by-Step Installation & Flashing Instructions

### Step 1: Install Arduino IDE & ESP32 Board
1. Download and install **Arduino IDE 2.x** from [arduino.cc](https://www.arduino.cc/en/software).
2. Open Arduino IDE &rarr; **File** &rarr; **Preferences**.
3. In **Additional boards manager URLs**, paste:
   ```text
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
4. Click **Tools** &rarr; **Board** &rarr; **Boards Manager** &rarr; Search for `esp32` by Espressif &rarr; Click **Install**.

### Step 2: Install Required Libraries in Arduino IDE
Go to **Tools** &rarr; **Manage Libraries** (or `Ctrl + Shift + I`) and install:
1. **ArduinoJson** (by Benoit Blanchon, Version 6 or 7) — For formatting JSON payloads.

### Step 3: Open and Configure the Firmware
1. Open the file [hardware_esp32_firmware.ino](file:///C:/Users/Pratiksha/.gemini/antigravity/scratch/factorymind/hardware_esp32_firmware.ino) in Arduino IDE.
2. In lines 24–29, enter your Wi-Fi name and password:
   ```cpp
   const char* WIFI_SSID     = "Your_WiFi_Hotspot_Name";
   const char* WIFI_PASSWORD = "Your_WiFi_Password";
   ```
3. Set your laptop's IP address:
   ```cpp
   const char* SERVER_URL    = "http://192.168.1.105:8000/api/v1/telemetry/ingest";
   ```
   *(To find your laptop's IP: Open Command Prompt &rarr; type `ipconfig` &rarr; look for **IPv4 Address**, e.g., `192.168.1.105`)*

### Step 4: Flash Firmware to ESP32
1. Connect ESP32 to your laptop using a Micro-USB cable.
2. Under **Tools** &rarr; **Board**, select **DOIT ESP32 DEVKIT V1**.
3. Under **Tools** &rarr; **Port**, select your COM port (e.g., `COM3` or `COM4`).
4. Click the **Upload** arrow button (or press `Ctrl + U`).
5. Open **Serial Monitor** at **115200 baud** to see live Wi-Fi connection and HTTP 200 responses!

---

## 4. How the Website Receives & Visualizes the Live IoT Data

When your ESP32 sends a reading:
1. **HTTP Ingestion:** The ESP32 sends `POST /api/v1/telemetry/ingest` with JSON:
   ```json
   {
     "machine_code": "CNC-001",
     "temperature": 68.4,
     "vibration_rms": 0.38,
     "vibration_peak": 0.54,
     "current_amp": 7.45,
     "rpm": 1450.0,
     "pressure_bar": 5.8
   }
   ```
2. **AI Inference:** The FastAPI backend runs Random Forest classification & calculates Remaining Useful Life (RUL).
3. **Database Log:** The reading and prediction are written to SQLite/PostgreSQL.
4. **Live 3D Dashboard:** The browser (`http://127.0.0.1:8000/dashboard`) receives the update:
   - The 3D Digital Twin pulses green (normal) or red (critical).
   - Real-time Chart.js graphs draw the vibration, temperature, and current trends.
   - An alert siren chime plays automatically if parameters cross danger thresholds.

---

## 5. Live Demonstration Trick for External Examiners & Viva

During your SY MCA Review-II / Final Project Viva:
1. **Show Normal Operation:** Let the ESP32 sit peacefully on the table. The web dashboard will show:
   - Status: **HEALTHY (Green)**
   - Health Score: **96%**
   - Predicted RUL: **450+ Hours**
2. **Inject a Physical Fault (The Wow Factor):**
   - Gently **tap, flick, or shake** the MPU-6050 vibration sensor on the breadboard, OR place your warm thumb on the temperature sensor.
   - Within 2 seconds, the dashboard will detect high vibration (>1.2g) or high heat.
   - The 3D CNC model will turn **flashing RED**, an **audio alert chime** will trigger through the laptop speakers, and an automated **Maintenance Work Order** will pop up on screen.
3. This clearly proves to the committee that you have built a **genuine, working Cyber-Physical System (CPS)**, not just mock frontend screens!
