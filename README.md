# 📈 SNMP Bandwidth Poller & Graph Generator

![Language](https://img.shields.io/badge/Language-Python%203-blue)
![Protocol](https://img.shields.io/badge/Protocol-SNMP%20v2c-orange)
![Function](https://img.shields.io/badge/Function-Network%20Monitoring-green)

## 📖 Overview
Network Administrators need to visualize traffic flow to detect congestion. Tools like MRTG or Cacti rely on **SNMP Polling**. This repository contains a raw Python Poller that acts as the backend for such monitoring systems.

It connects to any SNMP-enabled router (MikroTik, Cisco, Huawei), queries the **Interface OIDs**, and calculates the real-time bandwidth usage in **Mbps**.

## 🛠 Features
- 📊 **Real-Time Polling:** Fetches `ifInOctets` and `ifOutOctets` every few seconds.
- 🧮 **Auto-Calculation:** Converts raw bytes into readable Mbps/Gbps.
- 🔍 **Interface Discovery:** Automatically finds active interfaces on the router.
- 💾 **CSV Logging:** Saves traffic data to a CSV file for graphing (Excel/Matplotlib).

## ⚙️ How It Works
1.  **OID Query:** Sends an SNMP GET request to `1.3.6.1.2.1.2.2.1.10` (Inbound Traffic).
2.  **Delta Calculation:** (Current_Bytes - Previous_Bytes) / Time_Interval * 8 = Bits per Second.
3.  **Output:** Prints the speed in Console and saves to Log.

## 🚀 Usage Guide

### Step 1: Install Dependencies
```bash
pip install pysnmp

Step 2: Configure Router (MikroTik Example)
Enable SNMP on your router first:
/snmp set enabled=yes trap-version=2
/snmp community add name=public addresses=0.0.0.0/0

Step 3: Run the Poller
Edit the script with your Router IP and Community String, then run:
python3 traffic_poller.py

⚠️ Requirements
Python 3.6+

Access to UDP Port 161 on the target device.
Author: Sheikh Alamin Santo
Cloud Infrastructure Specialist & Network Engineer
