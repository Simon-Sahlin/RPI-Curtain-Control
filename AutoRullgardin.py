print("Setting up...")
from gpiozero import LED, Button
import RPi.GPIO as GPIO
import time
import datetime as dt
import traceback #error handling

RaiseTimes = [7,30, #Monday
              8,00, #Tuesday
              9,0, #Wednesday
              9,0, #Thursday
              8,0, #Friday
              10,30, #Saturday
              10,30, #Sunday
              22,0] #Lowering

upBut = Button(24)
downBut = Button(23)

DIR = 20
STEP = 21

ENB = 26
SLP = 16

MS1 = 6
MS2 = 13
MS3 = 19

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


delay = 1/(2000*16)

upPos = 0
downPos = 5500*16
curPos = downPos

moving = False
lastClick = 0
clickDelay = 0.35
  
def Cleanup():
    print("Cleaning")

    GPIO.output(STEP, 0)
    GPIO.output(DIR, 0)

    GPIO.output(ENB, 0)
    GPIO.output(SLP, 0)

    GPIO.output(MS1, 0)
    GPIO.output(MS2, 0)
    GPIO.output(MS3, 0)

def Step(dir):
    global curPos
    curPos += dir
    GPIO.output(STEP, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    time.sleep(delay)

def Move(to):
    moving = True
    if (to < 0 or to > 1):
        print("Value has to be a % between 0 and 1")
        return
    toPos = int(to*(downPos-upPos))
    direction = toPos - curPos
    distance = abs(direction)
    if (direction < 0):
        GPIO.output(DIR, 0)
        direction = -1
    elif (direction > 0):
        GPIO.output(DIR, 1)
        direction = 1
    else:
        print("Motor was already in the position requested")
    
    GPIO.output(ENB, 1)
    GPIO.output(SLP, 1)

    time.sleep(0.100)

    for i in range(distance):
        Step(direction)
        #if (curPos % 500 == 0):
        #    print(curPos)
        if (downBut.is_pressed or upBut.is_pressed):
            print("bruh")
            break
        
    time.sleep(0.100)
        
    GPIO.output(ENB, 0)
    GPIO.output(SLP, 0)
    moving = False

def UpButtonPressed():
    if (not moving):
        global lastClick
        global curPos
        if (time.time() - lastClick < clickDelay):
            print("Double click! (Up)")
            time.sleep(1)
            Move(0)
            return
        lastClick = time.time()
        
        print("UpPressed")
        GPIO.output(ENB, 1)
        GPIO.output(SLP, 1)

        GPIO.output(DIR, 0)
        while True:
            Step(-1)
            if (not upBut.is_pressed):
                GPIO.output(ENB, 0)
                GPIO.output(SLP, 0)
                print("Ended buttonpress at: ", curPos)
                break
            if (downBut.is_pressed):
                print("Resetting at top")
                time.sleep(1)
                curPos = upPos
                Move(0.01)
                Move(0)
                break
        
        

def DownButtonPressed():
    if (not moving):
        global lastClick
        global curPos
        if (time.time() - lastClick < clickDelay):
            print("Double click! (Down)")
            time.sleep(1)
            Move(1)
            return
        lastClick = time.time()
        
        print("DownPressed")
        GPIO.output(ENB, 1)
        GPIO.output(SLP, 1)

        GPIO.output(DIR, 1)
        while True:
            Step(1)
            if (not downBut.is_pressed):
                GPIO.output(ENB, 0)
                GPIO.output(SLP, 0)
                print("Ended buttonpress at: ", curPos)
                break
            if (upBut.is_pressed):
                print("Resetting at bottom")
                time.sleep(1)
                curPos = downPos
                Move(downPos*0.99)
                Move(downPos)
                break

def ReadValues():
    time = dt.datetime.now().time()
    print("[",time,"] Reading values...")
    file = open("/home/pi/Desktop/Rullgardin/data.txt","r")
    values = file.read().split()
    for x in range(len(values)):
        RaiseTimes[x] = int(values[x])
        #print(RaiseTimes[x])
    file.close()
    print("[",time,"] Values updated")

try:
    upBut.when_pressed = UpButtonPressed
    downBut.when_pressed = DownButtonPressed

    curPos = 0
    time.sleep(1)
    Move(0)
    time.sleep(1)
    Move(0.1)
    time.sleep(1)
    Move(0)

    print("Setup Done")
    while True:  
        ReadValues()  
        weekday = dt.datetime.today().weekday()
    
        if dt.datetime.now().time() > dt.time(RaiseTimes[weekday * 2], RaiseTimes[weekday * 2 + 1]) and dt.datetime.now().time() < dt.time(RaiseTimes[weekday * 2], RaiseTimes[weekday * 2 + 1] + 1):
            print ("The clock has passed the specified time on day: ", weekday)
            wakeUpSteps = 5
            wakeUpTime = 300
            wakeUpPower = 3
            for i in range(1, wakeUpSteps+1):
                Move(1 - ((i/wakeUpSteps)**wakeUpPower ))
                time.sleep(wakeUpTime/wakeUpSteps)
            time.sleep(60)
            
        elif dt.datetime.now().time() > dt.time(RaiseTimes[14], RaiseTimes[15]) and dt.datetime.now().time() < dt.time(RaiseTimes[14], RaiseTimes[15] + 1):
            print ("The clock has passed the specified time on LOWERING")
            Move(1)
            time.sleep(60)

        time.sleep(60)
        

except Exception:
    print("\nCRASH LOL")
    Cleanup()
    traceback.print_exc()
 
 
except KeyboardInterrupt:
    Cleanup()
    print("\nEnding Program")

