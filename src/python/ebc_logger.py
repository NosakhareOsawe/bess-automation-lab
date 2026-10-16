
import time
import csv
from datetime import datetime
import serial
import serial.tools.list_ports

BAUD_RATE = 9600
ESP32_BAUD = 115200
TIMEOUT_SEC = 2
AMBIENT_TEMP_C = 22.0

def find_ebc_port():
    for p in list(serial.tools.list_ports.comports()):
        if "14420" in p.device and "144140" not in p.device:
            return p.device
    return None

def find_esp32_port():
    for p in list(serial.tools.list_ports.comports()):
        if "144140" in p.device:
            return p.device
    return None

def read_temperature(esp32):
    if esp32 is None:
        return None, None, None, None, None
    try:
        esp32.reset_input_buffer()
        line = esp32.readline().decode("utf-8").strip()
        if "T1:" in line and "T2:" in line:
            parts = {}
            for item in line.split(","):
                if ":" in item:
                    key, val = item.split(":")
                    parts[key.strip()] = val.strip()
            t1 = float(parts["T1"]) if parts.get("T1") != "N/A" else None
            t2 = float(parts["T2"]) if parts.get("T2") != "N/A" else None
            ds = float(parts["DS"]) if parts.get("DS") != "N/A" else None
            da1 = float(parts["DA1"]) if parts.get("DA1") != "N/A" else None
            da2 = float(parts["DA2"]) if parts.get("DA2") != "N/A" else None
            return t1, t2, ds, da1, da2
        return None, None, None, None, None
    except Exception:
        return None, None, None, None, None

def main():
    ebc_port = find_ebc_port()
    if not ebc_port:
        print("[-] Error: Could not locate EBC-A20.", flush=True)
        return
    print(f"[+] Found EBC-A20: {ebc_port}", flush=True)

    esp32_port = find_esp32_port()
    if esp32_port:
        print(f"[+] Found ESP32: {esp32_port}", flush=True)
    else:
        print("[-] ESP32 not found - temperature logging disabled.", flush=True)

    try:
        ser = serial.Serial(
            port=ebc_port,
            baudrate=BAUD_RATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_ONE,
            timeout=TIMEOUT_SEC
        )
    except Exception as e:
        print(f"[-] Failed to open EBC-A20: {str(e)}", flush=True)
        return

    try:
        esp32 = serial.Serial(
            port=esp32_port,
            baudrate=ESP32_BAUD,
            timeout=2
        ) if esp32_port else None
        if esp32:
            print(f"[+] ESP32 connected: {esp32_port}", flush=True)
    except Exception as e:
        print(f"[-] ESP32 not available: {str(e)}", flush=True)
        esp32 = None

    filename = f"bess_pack_charge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    print(f"[+] Initializing live storage file: {filename}", flush=True)

    with open(filename, mode="w", newline="") as csv_file:
        headers = [
            "Timestamp", "Status", "Voltage_V", "Current_A", "Capacity_mAh",
            "Temp_String1_C", "Temp_String2_C", "Delta_String_C",
            "Delta_Ambient1_C", "Delta_Ambient2_C"
        ]
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()

        print("\n==================================================", flush=True)
        print(" BESS PACK PRODUCTION DATA STREAM ENGAGED")
        print("==================================================\n", flush=True)

        status_map = {0: "Off/Standby", 1: "CC_Charge", 2: "CV_Charge", 3: "Discharge"}

        try:
            while True:
                ser.write(b'\xfa\x05\x00\x00\x00\x00\x00\x00\x05\xf8')
                raw_bytes = ser.read(19)
                ser.reset_input_buffer()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if len(raw_bytes) >= 19 and raw_bytes[0] == 0xfa and raw_bytes[1] in status_map:
                    raw_status = raw_bytes[1]
                    status_text = status_map.get(raw_status, f"Unknown ({raw_status})")

                    raw_voltage = (raw_bytes[11] << 8) | raw_bytes[12]
                    voltage = raw_voltage / 349.18

                    raw_current = (raw_bytes[6] << 8) | raw_bytes[7]
                    current = raw_current / 1000.0

                    capacity_mah = (raw_bytes[2] << 24) | (raw_bytes[3] << 16) | (raw_bytes[4] << 8) | raw_bytes[5]

                    t1, t2, ds, da1, da2 = read_temperature(esp32)

                    print(f"[{timestamp}] State: {status_text:<11} | V: {voltage:.2f}V | I: {current:.2f}A | Cap: {capacity_mah}mAh | T1: {t1}C T2: {t2}C DS: {ds}", flush=True)

                    writer.writerow({
                        "Timestamp": timestamp,
                        "Status": status_text,
                        "Voltage_V": round(voltage, 2),
                        "Current_A": round(current, 2),
                        "Capacity_mAh": capacity_mah,
                        "Temp_String1_C": t1 if t1 is not None else "N/A",
                        "Temp_String2_C": t2 if t2 is not None else "N/A",
                        "Delta_String_C": ds if ds is not None else "N/A",
                        "Delta_Ambient1_C": da1 if da1 is not None else "N/A",
                        "Delta_Ambient2_C": da2 if da2 is not None else "N/A"
                    })
                    csv_file.flush()
                else:
                    print(f"[{timestamp}] [-] Message validation timeout frame dropped.", flush=True)

                time.sleep(1)

        except KeyboardInterrupt:
            print("\n[+] Data logging suspended via terminal override.", flush=True)
        finally:
            ser.close()
            print("[+] Serial port closed safely.", flush=True)

if __name__ == "__main__":
    main()