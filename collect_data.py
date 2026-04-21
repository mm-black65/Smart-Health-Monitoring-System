import serial
import json
import time
import os

# Configuration
SERIAL_PORT = 'COM3'  # Replace with your ESP32's serial port (e.g., COM3 on Windows, /dev/ttyUSB0 on Linux)
BAUD_RATE = 115200    # Match your ESP32's baud rate
OUTPUT_FILE = 'diagram.json'

# Initialize the JSON file if it doesn't exist or is empty
if not os.path.exists(OUTPUT_FILE) or os.stat(OUTPUT_FILE).st_size == 0:
    with open(OUTPUT_FILE, 'w') as f:
        json.dump([], f)  # Start with an empty array

def collect_data():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT}. Collecting data... Press Ctrl+C to stop.")

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    # Assume the ESP32 sends data like "temperature:25.5,humidity:60"
                    # Parse it into a dict (customize based on your ESP32 output)
                    data_point = {}
                    pairs = line.split(',')
                    for pair in pairs:
                        if ':' in pair:
                            key, value = pair.split(':', 1)
                            data_point[key.strip()] = value.strip()

                    # Add timestamp
                    data_point['timestamp'] = time.time()

                    # Load existing data, append new point, and save
                    with open(OUTPUT_FILE, 'r') as f:
                        data = json.load(f)
                    data.append(data_point)
                    with open(OUTPUT_FILE, 'w') as f:
                        json.dump(data, f, indent=4)

                    print(f"Collected: {data_point}")

            time.sleep(0.1)  # Small delay to avoid overwhelming the port

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("Stopped collecting data.")
    finally:
        if 'ser' in locals():
            ser.close()

if __name__ == "__main__":
    collect_data()