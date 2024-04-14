import json
from math import pi
import board
from busio import I2C
import adafruit_pca9685

i2c = I2C(board.SCL, board.SDA)
pwmhat = adafruit_pca9685.PCA9685(i2c)
pwmhat.frequency = 50

config = {}

while True:
    servo_name = input("Servo name (x to exit): ")
    if servo_name == "x":
        break
    servo_port = int(input("Port: "))
    config[servo_name] = {"port": servo_port, "pwm_vals": [], "ang_vals": []}
    while True:
        prev_val = 0
        angle = input("Servo angle (multiple of pi) (x to continue): ")
        if angle == "x":
            break
        angle = float(angle)*pi
        while True:
            servo_val = input("Guess (s to save): ")
            if servo_val == "s":
                config[servo_name]["pwm_vals"] += [prev_val]
                config[servo_name]["ang_vals"] += [angle]
                break
            servo_val = int(servo_val)
            pwmhat.channels[servo_port].duty_cycle = servo_val
            prev_val = servo_val

old_config = {}
try:
    with open("servos.json", "r") as file:
        old_config = json.load(file)
except:
    pass
old_config.update(config)
with open("servos.json", "w") as file:
    json.dump(old_config, file)
