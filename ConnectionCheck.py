import serial
import time

ser = serial.Serial('/dev/ttyAMA0', baudrate=115200, timeout=1)

try:
    while True:

        ser.flushInput()
        ser.flushOutput()

        ser.write(b'2') 
        print("Sent value: 2")

        time.sleep(0.1)
        
        if ser.in_waiting > 0:
            received = ser.read().decode('utf-8')
            print(f"Received from input: {received}")
            
        time.sleep(4)
        
except KeyboardInterrupt:
    ser.close()