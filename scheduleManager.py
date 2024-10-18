import time
import datetime as dt
from threading import Thread, Lock


class ScheduleManager:
    def __init__(self, motor, app):
        self.motor = motor
        self.app = app
        self.timers = [
            "01:00",
            "02:00",
            "03:00",
            "04:00",
            "05:00",
            "06:00",
            "07:00",
            "08:00"
        ]
        self.watchThread = None


    def startWatch(self):
        print("Starting schedule managager watch")
        if self.watchThread is None:
            self.watchThread = Thread(target=self.watch, daemon=True)
            self.watchThread.start()

    def watch(self):
        with self.app.app_context():
            while True:
                now = dt.datetime.now().strftime("%H:%M")
                waitTime = 60 - dt.datetime.now().time().second
                # print("Current Time is: " + str(dt.datetime.now().time()))

                if (now == self.timers[dt.datetime.today().weekday()]):
                    self.motor.moveMotor(0)
                    time.sleep(waitTime)

                if (now == self.timers[7]):
                    self.motor.moveMotor(1)
                    time.sleep(waitTime)

                time.sleep(waitTime % 5 + 5)