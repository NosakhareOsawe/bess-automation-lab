# Import the time module to establish delays and control the logging frequency
import time
# Import the comma-separated-values utility to handle file exports cleanly
import csv
# Import the datetime package to record system clock metrics
from datetime import datetime
# Import the main serial package to handle terminal-to-hardware communication
import serial
# Import the serial port listing framework to automate device detection
import serial.tools.list_ports

# Define global connectivity profiles for the CH340 serial infrastructure
PORT_TARGET = "AUTO"
BAUD_RATE = 9600
TIMEOUT_SEC = 2

# Define a background function to scan for the physical USB-to-TTL hardware node
def find_serial_port():
    # Iterate through all available communications links attached to the Mac
    for p in list(serial.tools.list_ports.comports()):
        # Check if the hardware label matches the CH340 interface signatures
        if "usbserial" in p.device.lower() or "1a86" in str(p.hwid).lower():
            # Return the direct absolute device route path
            return p.device
    # Return nothing if no hardware matches are found
    return None

# The main orchestrator function where our real-time data parser lives
def main():
    # Load our configured connection point string
    port = PORT_TARGET
    
    # If set to auto, call our scanner function to resolve the hardware route
    if port == "AUTO":
        detected_port = find_serial_port()
        if detected_port:
            port = detected_port
            print(f"[+] Found device interface: {port}", flush=True)
        else:
            print("[-] Error: Could not locate the USB serial link cable.", flush=True)
            return

    # Open the serial gateway inside a validation block to manage hardware access locks
    try:
        ser = serial.Serial(
            port=port,
            baudrate=BAUD_RATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_ODD,       # Apply ZKETECH's required odd parity bit validation
            stopbits=serial.STOPBITS_ONE,
            timeout=TIMEOUT_SEC
        )
    except Exception as e:
        print(f"[-] Failed to map serial gateway: {str(e)}", flush=True)
        return

    # Build a timestamped file name for your battery modeling records
    filename = f"bess_pack_charge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    print(f"[+] Initializing live storage file: {filename}", flush=True)

    # Open the text file and write the system data headers
    with open(filename, mode="w", newline="") as csv_file:
        headers = ["Timestamp", "Status", "Voltage_V", "Current_A", "Capacity_mAh"]
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()

        print("\n==================================================", flush=True)
        print(" 🔋 BESS PACK PRODUCTION DATA STREAM ENGAGED")
        print("==================================================\n", flush=True)

        # Operational status mapping dictionary for the ZKETECH motherboard
        status_map = {0: "Off/Standby", 1: "CC_Charge", 2: "CV_Charge", 3: "Discharge"}

        try:
            while True:
                # Issue the standard inquiry frame query across the wire
                ser.write(b'\xfa\x05\x00\x00\x00\x00\x00\x00\x05\xf8')
                
                # Capture the incoming 19-byte telemetry response array
                raw_bytes = ser.read(19)
                
                # Fetch a synchronized timestamp string
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Verify that a full, valid message packet was captured
                if len(raw_bytes) >= 19 and raw_bytes[0] == 0xfa:
                    
                    # Parse the operating state byte (Byte index 1)
                    raw_status = raw_bytes[1]
                    status_text = status_map.get(raw_status, f"Unknown ({raw_status})")
                    
                    # Extract the voltage metrics from bytes 11 and 12 and apply the ZKETECH scaling index
                    raw_voltage = (raw_bytes[11] << 8) | raw_bytes[12]
                    voltage = raw_voltage / 120.0
                    
                    # Extract the current draw from bytes 6 and 7 and scale to Amps
                    raw_current = (raw_bytes[6] << 8) | raw_bytes[7]
                    current = raw_current / 1000.0
                    
                    # Extract the running calculated cell capacity metrics from bytes 2, 3, 4, and 5
                    capacity_mah = (raw_bytes[2] << 24) | (raw_bytes[3] << 16) | (raw_bytes[4] << 8) | raw_bytes[5]

                    # Output the cleanly parsed engineering telemetry line directly onto the terminal screen
                    print(f"[{timestamp}] State: {status_text:<11} | V: {voltage:.2f}V | I: {current:.2f}A | Cap: {capacity_mah}mAh", flush=True)
                    
                    # Write the synchronized telemetry parameters directly into the CSV row tracking pool
                    writer.writerow({
                        "Timestamp": timestamp,
                        "Status": status_text,
                        "Voltage_V": round(voltage, 2),
                        "Current_A": round(current, 2),
                        "Capacity_mAh": capacity_mah
                    })
                    # Force Python to commit the row data data to the disk immediately to prevent caching losses
                    csv_file.flush()
                else:
                    print(f"[{timestamp}] [-] Message validation timeout frame dropped.", flush=True)
                    
                # Pause execution for exactly 1 second before requesting the next tracking loop
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n[+] Data logging suspended via terminal override.", flush=True)
        finally:
            # Safely release the communication channel back to the macOS kernel
            ser.close()
            print("[+] Serial port closed safely.", flush=True)

if __name__ == "__main__":
    main()
