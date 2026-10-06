# 📋 Bill of Materials (BOM) & Component Specifications

This asset index tracks all primary infrastructure components, computational nodes, edge sensing modules, and power distribution devices integrated into the testing laboratory.

### 1. Computational & Routing Core (IT Layer)

| Asset Description | Function Profile | Interfacing Ports | Quant. | Est. Status |
| :--- | :--- | :--- | :--- | :--- |
| **MacBook Pro** | Engineering Workstation & SCADA Visualizer | USB-C / WiFi | 1 | Active |
| **Raspberry Pi 5** | Core Energy Management System (EMS) Brain | RJ45 Ethernet / USB | 1 | Active |
| **Moxa EDS-G509** | Layer 2 Managed Switch Network Backbone | 9x Gigabit RJ45 Ports | 1 | Active |
| **Robustel R3000 3P** | Industrial Modbus Gateway & Remote Perimeter Router | RJ45 Ethernet / RS485 Serial / USB | 1 | Active |
| **Jensen AL59300 v6** | Lab Security Perimeter Firewall & Gateway Router | 1x WAN / 4x LAN RJ45 | 1 | Active |

### 2. Physical Automation & Sensing Arrays (OT Layer)

| Asset Description | Sensor Protocol | Hardware Address / PIN | Quant. | Est. Status |
| :--- | :--- | :--- | :--- | :--- |
| **Arduino Leonardo** | Pack-Level Local BMS Controller Node | USB-TTL Serial / Digital Pins | 1 | Active |
| **DS18B20 Kit Probe** | Waterproof Core Cell Thermal Sensor | 1-Wire Digital Bus / Pin D2 | 1 | Active |
| **Eastron SDM120M** | AC Grid Energy Metering Node | Modbus-RTU over RS485 / Slave ID 1 | 1 | Standby |
| **MCU-219 (INA219)** | Zero-Drift Bidirectional DC Power Monitor | I2C Protocol Bus / Hex Address 0x40 | 1 | Inventory |
| **ZMPT101B Module** | Active Single-Phase AC Voltage Transformer | Analog ADC Interface Input | 1 | Inventory |
| **MAX485 Converter** | TTL Serial to RS485 Differential Voltage Shield | UART Pins 0, 1 / Control Pin 3 | 5 | Active |

### 3. Electrochemical Power & Test Systems

| Asset Description | Operational Limits | Configuration Setup | Quant. | Est. Status |
| :--- | :--- | :--- | :--- | :--- |
| **ZKETECH EBC-A20** | 19-20V Input / 5A Max Charge / 20A Max Discharge | Kelvin Configuration (Split-Jaw) | 1 | Active |
| **Samsung INR18650-25R**| 3.6V Nominal / 4.2V Max / 2500mAh / 20A Continuous | 2S2P (7.4V Nominal / 5000mAh) | 4 | Active |
| **4-Slot Multi-Config Holder**| Independent isolated PCB screw terminal tracking strip | Arranged in true 2P blocks | 1 | Active |
| **2S 20A Green BMS** | Overcharge / Overdischarge / Short Circuit Hardware Protection | Bypassed for analytical CC/CV testing | 1 | Standby |
| **Mean Well MDR-60-24** | 24V DC 2.5A Industrial DIN-Rail Switching Power Supply | Feeds core Moxa switch and rails | 1 | Active |
| **12AWG Inline Fuse Casing**| High-current copper fuse array holder protection loop | Populated with 20A safety blade | 1 | Active |
