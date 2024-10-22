from gpiozero import LED, Button
import time
import datetime as dt

upBut = Button(24)
downBut = Button(23)

clickDelay = 0.35

class ButtonManager:

    def __init__(self, motor, app):
        self.lastClick = 0
        self.motor = motor
        self.app = app
        self.pressed = False
        upBut.when_pressed = lambda : self.buttonPressed(0)
        downBut.when_pressed = lambda : self.buttonPressed(1)

    def buttonPressed(self, dir):
        if (not self.pressed):
            self.pressed = True
            with self.app.app_context():
                btnStr = "up button" if dir == 0 else "down button"
                print("Button press detected on " + btnStr)
                self.motor.stopMotor()

                # Move to bound if double press
                if (time.time() - self.lastClick < clickDelay):
                    time.sleep(0.1)
                    print("Double press detected on " + btnStr)
                    self.motor.moveMotor(dir)
                    self.pressed = False
                    return
                self.lastClick = time.time()

                # Base case: move motor
                self.motor.moveMotor(999 if dir == 1 else -999)
                while True:
                    #Break if released
                    if (not upBut.is_pressed):
                        print(btnStr.capitalize() + " released")
                        self.motor.stopMotor()
                        self.pressed = False
                        break

                    # Reset position if other button is pressed
                    if (downBut.is_pressed if dir == 0 else upBut.is_pressed):
                        print("Resetting position at " + ("top" if dir == 0 else "bottom"))
                        self.motor.stopMotor()
                        time.sleep(1)
                        newPos = 0 if dir == 0 else self.motor.maxPos
                        self.motor.curPos = newPos
                        self.motor.moveMotor(0.01 + newPos)
                        time.sleep(0.5)
                        self.motor.stopMotor()
                        self.motor.moveMotor(newPos)
                        self.pressed = False
                        print("Done resetting...")
                        return

                    time.sleep(0.1)