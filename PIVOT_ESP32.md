# 📐 Engineering Note: Why I Ditched the Arduino Leonardo for an Industrial ESP32-S3

## 🔍 The Situation
While setting up my Battery Energy Storage System (BESS) lab bench, my edge controller layer—the Arduino Leonardo—started fighting me at every turn. I had originally chosen to use the Leonardo because it cost me exactly **`0 kr`**—I already owned it as a leftover component from my master's degree engineering studies. However, trying to reuse this legacy hobbyist hardware turned into a major bottleneck for the project. It created massive timing headaches when flashing code, clashing serial lines, and exposed my home network to a bad ground loop that actually knocked out my house internet.

To stop wasting time, protect my gear, and keep my lab bench professional, I decided to pull the Leonardo out of the setup and upgrade to the **Waveshare Industrial ESP32-S3-RS485-CAN module**.

---

## 🚨 What Broke (The Real Problems)

### 1. The Annoying Port-Changing Glitch (butterfly_recv / OS Errors)
The Leonardo handles USB communication directly inside its main chip. When you try to upload code via the terminal (arduino-cli upload), the board has to drop its current port, reset itself, and create a brand-new "bootloader" port in a tiny 8-second window. My Mac terminal kept missing this timing window because the port name kept changing on its own. It kept throwing `No such file or directory` or `butterfly_recv()` timeout errors, burning hours of my limited time.

### 2. Fighting with the Serial Pins (MAX485 Collisions)
To get Modbus RTU talking to my Robustel router, I had to wire a separate MAX485 chip module straight to the Leonardo’s hardware RX and TX pins (Pins 0 and 1). Because the MAX485 chip locks onto those lines to keep the signal clean, it blocked my Mac from uploading new code. To flash anything, I had to manually unplug the data wires and plug them back in every single time. It made testing impossible.

### 3. Zero Safety Protection (The Whole-House Internet Crash)
The cheap MAX485 breakout modules don't have any electrical isolation built-in. The second I flipped on the main 230V AC distribution box, a sudden voltage shift traveled backwards right up my data wires. This spike traveled down the line, hit my Moxa switch, and flooded my Tele2 Home Hub router—freezing its memory and completely knocking out the internet for the whole house.

---

## ⚡ Network Impact & The Galvanic Solution
When that un-isolated ground loop spiked, it caused an immediate router memory pool crash, knocking out the internet connection for the entire house. It proved that standard, uninsulated hobbyist setups are too vulnerable for an environment tied to high-voltage lines.

The permanent fix for this vulnerability was migrating to the Waveshare board's built-in optocoupler isolation. The optocoupler creates a complete galvanic barrier that physically air-gaps the data lines from the processing silicon. This successfully prevents ground potential differences from propagating backward into the networking spine, keeping my MacBook Pro, my Moxa switch, and my family's Tele2 network 100% safe.

---

## 🧭 Other Options I Considered
Before buying new gear, I looked at a few different ways to fix this bottleneck:
*   **Option A: Stick with the Leonardo and write custom reset scripts.** I thought about writing a shell script to force-trigger the serial port and catch the changing bootloader address. *Why I rejected it:* It doesn't actually fix the root issues. I’d still have to unplug the wires manually every upload, the 2.5 KB RAM limit would crash if I tried running heavy Kalman Filter math later, and my Mac would still be unprotected against high-voltage spikes.
*   **Option B: Upgrade to an Arduino UNO R4.** Shifting to a newer 32-bit board would fix the memory limits and give me a more stable USB link. *Why I rejected it:* At the end of the day, it's still a bare hobbyist board. I'd still have to manually wire up separate MAX485 modules, it lacks built-in electrical protection, and it can't clip cleanly onto a standard 35mm industrial DIN rail.
*   **Option C: Go Industrial with the Waveshare ESP32-S3-RS485-CAN.** This meant getting an enclosed, protected controller built specifically for industrial setups. This is the path I chose.

---

## 🏆 Why the New Waveshare Board is the Best Alternative
Upgrading to this module immediately stabilized my whole lab network for a few clear reasons:

1.  **True Electrical Isolation (Optocouplers):** As noted above, the physical data wires are completely air-gapped from the main processor core, trapping high-voltage spikes or ground loops entirely inside the module.
2.  **Built-In RS-485 (No Extra Modules):** The transceiver chip is built right into the motherboard inside the white casing. The raw wires from my Robustel router screw straight into the terminal blocks (`A+` and `B-`). I can finally throw away the separate MAX485 chips and messy jumper wires.
3.  **Flawless USB-C Flashing:** The ESP32-S3 has a rock-solid native USB bridge. It keeps the exact same serial port identity when resetting, so code compiles and flashes instantly on the first try, every time.
4.  **Substation-Ready Form Factor:** The casing has a built-in 35mm DIN-rail clip. It snaps right onto the rail next to my ABB circuit breaker and MeanWell power supply, making the inside of my CAMWAY box look like a real, professional industrial control panel.
