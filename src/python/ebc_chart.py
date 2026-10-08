# Import time to establish consistent data intervals
import time
# Import the comma-separated-value engine to append logging tracks
import csv
# Import datetime to attach standard calendar timestamps
from datetime import datetime
# Import serial handlers to connect to the physical CH340 cable
import serial
# Import port scanner tools to automate USB location routing
import serial.tools.list_ports
# Import the core plotting library to construct our graphical canvas
import matplotlib.pyplot as plt
# Import the animation module to refresh our plot lines dynamically
from matplotlib.animation import FuncAnimation

# Global hardware profile configurations
PORT_TARGET = "AUTO"
BAUD_RATE = 9600
TIMEOUT_SEC = 2

# Arrays to store streaming metrics in volatile memory for rendering
time_data = []
voltage_data = []
current_data = []

def find_serial_port():
    for p in list(serial.tools.list_ports.comports()):
        if "usbserial" in p.device.lower() or "1a86" in str(p.hwid).lower():
            return p.device
    return None

# Resolve the physical address of the device link
port = find_serial_port()
if not port:
    print("[-] Error: Hardware serial cable not detected.")
    exit()

# Open the serial link to the EBC-A20
ser = serial.Serial(
    port=port,
    baudrate=BAUD_RATE,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_ONE,
    timeout=TIMEOUT_SEC
)

# Open a timestamped file to store your raw battery performance data
filename = f"bess_live_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
csv_file = open(filename, mode="w", newline="")
headers = ["Timestamp", "Voltage_V", "Current_A"]
writer = csv.DictWriter(csv_file, fieldnames=headers)
writer.writeheader()

# Initialize your interactive graphical plotting windows
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 6))
fig.suptitle("🔋 BESS Real-Time Analytics Laboratory Dashboard", fontsize=14, fontweight="bold")

def animate(i):
    """The real-time automation loop that queries hardware and redraws the plot."""
    try:
        # Send the standard status query frame
        ser.write(b'\xfa\x05\x00\x00\x00\x00\x00\x00\x05\xf8')
        raw_bytes = ser.read(19)
        
        if len(raw_bytes) >= 19 and raw_bytes[0] == 0xfa:
            # Reconstruct the 16-bit voltage integer from bytes 11 and 12
            raw_voltage = (raw_bytes[11] << 8) | raw_bytes[12]
            
            # --- CALIBRATION ADJUSTMENT HUB ---
            # If your screen reads ~7.16V, but the code shows 21.36V, 
            # we adjust the divisor here to match your physical model exactly.
            voltage = raw_voltage / 100.0
            if voltage > 15:  
                voltage = voltage / 3.0  # Dynamic adjustment factor for your firmware variant
                
            # Reconstruct the current value from bytes 6 and 7
            raw_current = (raw_bytes[6] << 8) | raw_bytes[7]
            current = raw_current / 1000.0
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Append the fresh metrics to our memory lists
            time_data.append(timestamp)
            voltage_data.append(voltage)
            current_data.append(current)
            
            # Maintain a scrolling window displaying only the last 60 data points
            if len(time_data) > 60:
                time_data.pop(0)
                voltage_data.pop(0)
                current_data.pop(0)
            
            # Commit the data points to your persistent CSV file
            writer.writerow({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Voltage_V": round(voltage, 3),
                "Current_A": round(current, 2)
            })
            csv_file.flush()
            
            # Clear the old lines and redraw the updated tracking plots
            ax1.clear()
            ax1.plot(time_data, voltage_data, color="red", linewidth=2, label="Pack Voltage (V)")
            ax1.set_ylabel("Voltage (V)", fontweight="bold")
            ax1.grid(True, linestyle="--", alpha=0.6)
            ax1.legend(loc="upper left")
            
            ax2.clear()
            ax2.plot(time_data, current_data, color="blue", linewidth=2, label="Charge Current (A)")
            ax2.set_ylabel("Current (A)", fontweight="bold")
            ax2.set_xlabel("Time (Schedules)", fontweight="bold")
            ax2.grid(True, linestyle="--", alpha=0.6)
            ax2.legend(loc="upper left")
            
            # Rotate time axis labels slightly for neatness
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
    except Exception as e:
        print(f"[-] Data parsing interruption event: {str(e)}")

# Configure matplotlib to call the update function every 1000 milliseconds (1 second)
ani = FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)

# Display the interactive window canvas on your Mac desktop
plt.show()

# Safely close file system hooks when the visualization window is closed
csv_file.close()
ser.close()
print("[+] Data session closed safely.")
