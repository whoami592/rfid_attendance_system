import serial
import time
import csv
from datetime import datetime

# Banner
print("""
============================================================
          RFID-BASED ATTENDANCE SYSTEM
============================================================
      Coded By Pakistani Ethical Hacker Mr Sabaz Ali Khan
============================================================
""")

# Configuration
SERIAL_PORT = 'COM3'  # Change to your port (e.g., '/dev/ttyUSB0' for Linux)
BAUD_RATE = 9600
CSV_FILE = 'attendance.csv'

# Sample user database (RFID tag ID -> Name)
USER_DATABASE = {
    '1234567890': 'Ali Ahmed',
    '0987654321': 'Sana Khan',
    '1122334455': 'Hassan Raza'
}

def initialize_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to RFID reader on {SERIAL_PORT}")
        return ser
    except serial.SerialException as e:
        print(f"Error connecting to RFID reader: {e}")
        return None

def log_attendance(tag_id):
    name = USER_DATABASE.get(tag_id, 'Unknown')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([tag_id, name, timestamp])
    
    print(f"Attendance logged: {name} (ID: {tag_id}) at {timestamp}")

def main():
    # Initialize CSV file with headers if it doesn't exist
    try:
        with open(CSV_FILE, mode='x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Tag ID', 'Name', 'Timestamp'])
    except FileExistsError:
        pass

    # Initialize serial connection
    ser = initialize_serial()
    if not ser:
        print("Exiting due to connection failure.")
        return

    print("Scan RFID tag to log attendance. Press Ctrl+C to exit.")
    
    try:
        while True:
            if ser.in_waiting > 0:
                # Read RFID tag data
                tag_id = ser.readline().decode('utf-8').strip()
                if tag_id:
                    log_attendance(tag_id)
                time.sleep(0.5)  # Prevent multiple reads of the same tag
    except KeyboardInterrupt:
        print("\nExiting program.")
    finally:
        if ser and ser.is_open:
            ser.close()
            print("Serial connection closed.")

if __name__ == "__main__":
    main()