print("Setting up...")
from gpiozero import LED, Button
import RPi.GPIO as GPIO
import time
from threading import Thread, Lock
from flask import jsonify


# -------------------------------- GPIO SETUP -------------------------------- #
DIR = 20
STEP = 21

ENB = 26
SLP = 16

MS1 = 6
MS2 = 13
MS3 = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(SLP, GPIO.OUT)
GPIO.setup(MS1, GPIO.OUT)
GPIO.setup(MS2, GPIO.OUT)
GPIO.setup(MS3, GPIO.OUT)
  
GPIO.output(ENB, 0)
GPIO.output(SLP, 0)

# Microstep Resolution: 1   2   4   8   16
GPIO.output(MS1, 1) #   L   H   L   H   H
GPIO.output(MS2, 1) #   L   L   H   H   H
GPIO.output(MS3, 1) #   L   L   L   L   H

def Cleanup():
    print("Cleaning")
    GPIO.output(STEP, 0)
    GPIO.output(DIR, 0)
    GPIO.output(ENB, 0)
    GPIO.output(SLP, 0)
    GPIO.output(MS1, 0)
    GPIO.output(MS2, 0)
    GPIO.output(MS3, 0)


# ---------------------------------- VALUES ---------------------------------- #
delay = 1/(2000*16)

# -------------------------------- MOTOR LOGIC ------------------------------- #

class MotorController:
    def __init__(self):
        self.maxPos = 5500*16
        self.curPos = 0
        self.moving = False
        self.movementThread = None
        self.lock = Lock()

    def moveMotor(self, to):
        with self.lock:
            if self.moving:
                print("Motor is already moving")
                return
        if (to < 0 or to > 1):
            print("WARNING: Input values not between 0-1 is out of set bounds")

        self.movementThread = Thread(target=self.__move, args=(to,))
        self.movementThread.start()
        return jsonify({
            'message': 'Motor movement started',
            'position': to
        })

    def stopMotor(self):
        with self.lock:
            self.moving = False
        return jsonify({
            'message': 'Motor stopped',
            'position': (self.curPos/self.maxPos)
        })

    def __move(self, to):
        toPos = int(to*self.maxPos)
        direction = toPos - self.curPos
        distance = abs(direction)
        if (direction < 0):
            GPIO.output(DIR, 0)
            direction = -1
        elif (direction > 0):
            GPIO.output(DIR, 1)
            direction = 1
        else:
            print("Motor was already in the position requested")
            return
        

        with self.lock:
            self.moving = True
        GPIO.output(ENB, 1)
        GPIO.output(SLP, 1)

        time.sleep(0.100)

        for i in range(distance):
            self.__step(direction)
            with self.lock:
                if not self.moving:
                    break
            
        time.sleep(0.100)
            
        GPIO.output(DIR, 0)
        GPIO.output(ENB, 0)
        GPIO.output(SLP, 0)
        with self.lock:
            self.moving = False

    def __step(self, dir):
        self.curPos += dir
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(delay)