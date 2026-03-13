# ESP32 Chiller Monitoring System (Modbus + Web Server + LINE OA)

This project is an **industrial monitoring system for a Chiller** built
using **ESP32 with MicroPython**.\
The system reads operational data from a **Modbus controller**, provides
a **web-based monitoring interface**, and sends **alerts through LINE
Official Account (LINE OA)**.

It is designed for **24/7 stable operation** with built‑in protection
mechanisms such as watchdog reset, memory protection, WiFi
auto‑reconnect, and Modbus timeout recovery.

------------------------------------------------------------------------

# 🚀 Features

### 🌐 Web Server Dashboard

-   Monitor chiller sensor values through a web browser
-   Real‑time refresh dashboard
-   Simple ON/OFF control for the chiller

### 🔌 Modbus Communication

-   Read sensor data via Modbus RTU
-   Send control commands to the chiller controller

### 📲 LINE OA Notification

The system automatically sends notifications when:

-   WiFi is disconnected
-   WiFi reconnects
-   IP address changes
-   Chiller is turned ON
-   Chiller is turned OFF
-   System reboot due to protection mechanisms

### 🔄 Automatic Recovery System

To ensure stable long‑term operation:

-   WiFi auto‑reconnect
-   Watchdog timer reboot if system freezes
-   Automatic reboot when memory becomes too low
-   Modbus timeout protection

------------------------------------------------------------------------

# ⚙️ System Architecture

              +-------------------+
              |   Web Browser     |
              |  (Monitoring UI)  |
              +---------+---------+
                        |
                        | HTTP
                        |
               +--------v--------+
               |      ESP32      |
               |   MicroPython   |
               |                 |
               |  Web Server     |
               |  Modbus Master  |
               |  LINE Notifier  |
               +--------+--------+
                        |
                        | RS485 / UART
                        |
               +--------v--------+
               |  Chiller PLC    |
               |  Modbus Slave   |
               +-----------------+

------------------------------------------------------------------------

# 📂 Directory Structure

    .
    ├── 📄 boot.py        // run system file
    ├── 📄 main.py        // Main source code file
    ├── 📄 JGSmod.py      // Modbus API source code file
    ├── 📄 lineoa.py      // Line OA API source code file
    └── 📄 README.md

------------------------------------------------------------------------

# 📄 File Description

## 📄 boot.py

This file runs when the ESP32 boots.

Main purposes:

-   Initialize the MicroPython environment
-   Prepare memory and system resources
-   Run startup configurations before `main.py`

Example:

``` python
import gc
gc.collect()
```

------------------------------------------------------------------------

## 📄 main.py

The **main application file** of the system.

Responsibilities:

-   WiFi connection and auto reconnect
-   Web server creation
-   Reading Modbus sensor data
-   Sending LINE notifications
-   System protection and error recovery

Main modules used:

-   network
-   socket
-   machine
-   gc
-   watchdog

------------------------------------------------------------------------

## 📄 JGSmod.py

Custom **Modbus API library** used for communicating with the chiller
controller.

Main functions:

-   Read sensor values via Modbus
-   Send control commands
-   Handle Modbus RTU communication

Example functions:

    read_sensor()
    cmd_order()

------------------------------------------------------------------------

## 📄 lineoa.py

A helper library used to send messages to **LINE Official Account (LINE
OA)**.

Used for system notifications such as:

-   WiFi disconnected
-   WiFi reconnected
-   IP address changed
-   Chiller ON/OFF status
-   System reboot alerts

------------------------------------------------------------------------

# 🌐 Web Interface

ESP32 runs a built‑in web server.

Access the dashboard via:

    http://<ESP32_IP>

Example:

    http://192.168.1.25

Dashboard displays:

-   Speed command
-   Speed actual
-   Discharge temperature
-   High pressure
-   Suction temperature
-   Suction pressure
-   Ambient temperature
-   Evaporator temperature
-   EEV steps

Control buttons:

    ON
    OFF

These buttons allow remote control of the chiller.

------------------------------------------------------------------------

# 📲 LINE Notification Examples

### WiFi Connected

    ✅ WIFI CONNECTED
    IP : 192.168.1.25

### WiFi Disconnected

    ⚠ WIFI DISCONNECTED

### IP Address Changed

    📡 IP Address Changed
    New IP : 192.168.1.40

### Chiller ON

    ✅ Chiller ON

### Chiller OFF

    ❌ Chiller OFF

------------------------------------------------------------------------

# 🛡️ System Protection

The system is designed for **continuous industrial operation**.

### 1️⃣ Watchdog Timer

If the system freezes for more than **30 seconds**,\
ESP32 will automatically reboot.

------------------------------------------------------------------------

### 2️⃣ Memory Protection

The system constantly checks available RAM.

If memory drops below a safe threshold:

    ESP32 will reboot automatically

------------------------------------------------------------------------

### 3️⃣ Modbus Timeout Protection

If Modbus communication fails repeatedly:

    ESP32 automatically reboots

to restore the communication.

------------------------------------------------------------------------

### 4️⃣ WiFi Auto Reconnect

If WiFi is lost:

    ESP32 automatically reconnects

and sends a notification to LINE.

------------------------------------------------------------------------

# 🔧 Installation

### 1️⃣ Install MicroPython on ESP32

Flash the ESP32 with the latest MicroPython firmware.

------------------------------------------------------------------------

### 2️⃣ Upload Files

Upload the following files to the ESP32:

    boot.py
    main.py
    JGSmod.py
    lineoa.py

------------------------------------------------------------------------

### 3️⃣ Configure WiFi

Edit `main.py`:

    SSID = "YOUR_WIFI"
    PASSWORD = "YOUR_PASSWORD"

------------------------------------------------------------------------

### 4️⃣ Configure LINE OA

Insert your **LINE Channel Access Token**:

    channel_access_token = "YOUR_TOKEN"

------------------------------------------------------------------------

### 5️⃣ Restart ESP32

After reboot, the system will start automatically.

------------------------------------------------------------------------

# 💡 Recommended Hardware

-   ESP32 DevKit V1
-   RS485 to TTL Converter
-   Chiller Controller (Modbus RTU)
-   Industrial power supply

------------------------------------------------------------------------

# 🔮 Future Improvements

Potential enhancements:

-   Real‑time dashboard graphs
-   Cloud data logging
-   Mobile monitoring interface
-   Temperature / pressure alarm notifications
-   SD card data logging
-   Remote monitoring via the internet

------------------------------------------------------------------------

# 📜 License

This project is intended for **industrial monitoring and automation
purposes**.

You are free to modify and adapt it to your system.

------------------------------------------------------------------------

# 👨‍💻 Developer

ESP32 Industrial Monitoring System\
Modbus + Web Server + LINE OA Notification
