# 🔬 BESS Engineering Methodologies, Challenges, & Operational Logs

A living industrial journal logging testing procedures, mathematical estimation algorithm rules, real-world troubleshooting challenges, and BESS execution outcomes.

## 🚀 Active Testing Methodologies

### 1. Verification of Initial Storage State & Calibration (Cycle 1 Charge)
*   **Objective:** Stabilize newly unboxed Samsung 25R cells from their default storage charge state and confirm sensor scaling factors.
*   **Procedure:** Execute a Constant Current / Constant Voltage (CC/CV) charge profile using the EBC-A20 up to an upper ceiling of **8.40V**, using a controlled current profile of **2.50A**, terminating when current dips to **0.10A**.
*   **Data Parsing:** Telemetry is monitored via an asynchronous Python connection using the `pyserial` framework on macOS, querying data fields over an unbuffered terminal stream every 1000ms.

---

## ⚠️ Laboratory Engineering Challenges & Resolutions

### Challenge 1: The Independent Holder Circuit Disconnect Bug
*   **Symptom:** Individual cell arrays measured a healthy 3.85V directly at the holder, but when transferred to a single-row serial distribution block, the upper output terminal dropped to 0.00V.
*   **Root Cause Analysis:** The 4-slot multi-configuration holder isolates all positive and negative terminals (`B1` through `B4`) onto separate copper islands to support individual cell tracing. The internal PCB traces do not bridge the parallel sets automatically.
*   **Engineering Resolution:** Modified the installation blueprint. Parallel groupings were explicitly wired by bringing the positive cables (`B1+ / B2+`) together into Terminal Position 4, and the negative cables (`B1- / B2-`) into Terminal Position 3. This closed the parallel bridge and restored the system loop to a stable 7.70V baseline.

---

## 📊 Analytical Results & Data Captures
*(Logs, graphical plots, Coulomb counting trends, and State of Health analysis outputs will be populated here as testing runs complete).*
