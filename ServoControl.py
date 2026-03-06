import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)

pwm = GPIO.PWM(2, 50)
pwm.start(0)

    duty_cycle = (speed + 1) * 5 + 2.5
    duty_cycle = max(2.5, min(12.5, duty_cycle))

    print(f"Setting speed to {speed}, Duty Cycle: {duty_cycle}%")
    pwm.ChangeDutyCycle(duty_cycle)

try:
    while True:
        set_speed(1)
        time.sleep(2)
        set_speed(0)
        time.sleep(2)
        set_speed(-1)
        time.sleep(2)
        set_speed(0)
        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting...")
    pwm.stop()
    GPIO.cleanup()