# 🔋 My BESS Learning & Automation Home Bench

This is a personal home laboratory repository that I am building on my workbench to learn the fundamentals of **Battery Energy Storage Systems (BESS)**, **Industrial Protocols**, and **Systems Engineering**. 

The goal of this project isn't to build a commercial-grade substation, but rather to use a mix of industrial hardware and spare components to teach myself how to write code, handle hardware data flows, and troubleshoot real-world communication blocks.

## 📂 Project Repository Architecture
I have organized my local lab files into subdirectories to keep my learning workspace neat:
*   📂 **`docs/`**: My notes, wiring thoughts, and engineering change logs.
    *   📄 [My Bill of Materials (BOM) List](./docs/BOM.md) - A simple list of the components I am using.
    *   🗺️ [IP & Serial Network Topology Blueprint](./docs/TOPOLOGY.md) - How I mapped out my local IPs.
    *   🔬 [Learning Journal & Methodologies Log](./docs/METHODOLOGIES.md) - Notes on my test procedures.
    *   📐 [My Hardware Design Pivot Note](./docs/PIVOT_ESP32.md) - Why I moved away from my master's degree Arduino Leonardo to an industrial ESP32-S3 module after an unexpected ground loop block.
*   📂 **`src/`**: The code I am writing.
    *   💻 [src/python/](./src/python/) - My Python automation scripts for data logging and graphing.
*   📂 **`data/`**: Simple `.csv` files capturing my cell charging and grid logging tests.

---

## 🎛️ My Workbench Hardware Layout
*   **Edge Controller:** Waveshare Industrial ESP32-S3-RS485-CAN module (chosen specifically because its optocoupler isolation keeps my MacBook and my home router safe from ground loops).
*   **Data Acquisition:** A basic ZKETECH EBC-A20 electronic loader/charger.
*   **Local Network Setup:** A Moxa EDS-G509-T switch connecting my MacBook Pro (`192.168.1.50`) and my Raspberry Pi 5 (`192.168.1.10`) on an isolated `192.168.1.X` local home subnet.
*   **Industrial Gateway:** A Robustel R3000-3P router acting as a Modbus TCP-to-RTU gateway to bridge data channels.
*   **Grid Monitoring:** An Eastron SDM120M AC energy meter to track standard single-phase grid inputs.

---

## 🧭 Main Lessons & Roadmap Milestones Completed
- [x] **Handling Electrical Safety:** Discovered the hard way how an un-isolated ground loop can trip a home network router; pivoted from basic hobbyist pins to an industrially insulated module to keep my home workbench secure.
- [x] **Python Data Logging:** Wrote custom `pyserial` script loops to talk directly to the EBC-A20 charger and extract charging data natively into clean logs on macOS.
- [x] **Live Data Graphing:** Set up an unbuffered live-plotting chart window using `matplotlib` to watch voltage trends update visually in real time.
