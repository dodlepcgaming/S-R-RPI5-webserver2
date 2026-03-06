import serial
import time

# Set up the UART connection
# /dev/serial0 is the default alias for the UART pins on Pi 5
ser = serial.Serial('/dev/ttyAMA0', baudrate=115200, timeout=1)

try:
    while True:

        ser.flushInput()
        ser.flushOutput()

        # To send the number 2 as a character:
        ser.write(b'2') 
        print("Sent value: 2")

        time.sleep(0.1)
        
        # To check for a return value (Input):
        if ser.in_waiting > 0:
            received = ser.read().decode('utf-8')
            print(f"Received from input: {received}")
            
        time.sleep(4)
        
except KeyboardInterrupt:
    ser.close()