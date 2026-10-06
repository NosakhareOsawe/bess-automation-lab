# 🗺️ System Topology & Integration Mapping

This document details the exact physical, electrical, and logical connections that bind the laboratory hardware into a unified system loop.

### 1. Unified IP Networking Infrastructure (Layer 3)
All industrial and computational assets are mapped onto a shared static subnet to ensure reliable, high-speed telemetry paths:
*   **Subnet Mask Boundary:** `255.255.255.0`
*   **Main Internet Gateway (Robustel R3000-3P):** `192.168.1.1` (Interface: `eth0`)
*   **Core Layer 2 Spine (Moxa EDS-G509-T):** `192.168.1.2` (Management Port)
*   **Local Database & Kalman Filter Engine (Raspberry Pi 5):** `192.168.1.10` (Interface: `eth0`)
*   **Master SCADA Programming Terminal (MacBook Pro):** `192.168.1.50` (Ethernet / USB Adapter)

### 2. Modbus-RTU Serial Bus Infrastructure (RS485)
The **Robustel R3000-3P** acts as the Modbus Master Gateway. The industrial serial devices share a common differential two-wire bus:
*   **Bus Connection Profile:** 9600 Baud Rate, 8 Data Bits, 1 Stop Bit, Odd Parity.
*   **Node 1 (Eastron SDM120M AC Meter):** Modbus Slave ID `1`. Tracks external grid power parameters.
*   **Node 2 (Arduino Leonardo BMS Node):** Modbus Slave ID `2`. Tracks core battery thermal telemetry.

### 3. The 2S2P Kelvin Charging Loop
To evaluate battery degradation profiles using the **EBC-A20**, the physical structure uses a centralized terminal block layout:
*   **Terminal Position 1 (Main Pack Ground):** Lands holder `B3-/B4-` strings ──► Clamped to EBC-A20 Black Clip (0V).
*   **Terminal Position 2 (Series Bridge Node A):** Lands holder `B3+/B4+` positive cluster.
*   **Terminal Position 3 (Series Bridge Node B):** Lands holder `B1-/B2-` negative cluster.
    *   *Note: An industrial 2-terminal comb jumper locks Position 2 and 3 together to complete the series bridge.*
*   **Terminal Position 4 (Main Pack Power):** Lands holder `B1+/B2+` lines via a 20A Inline Blade Fuse ──► Clamped to EBC-A20 Red Clip (7.4V - 8.4V).
