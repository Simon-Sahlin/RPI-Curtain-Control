import os
import json

class DataManager:
    def __init__(self, motor, sched):
        self.motor = motor
        self.sched = sched
        self.filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

    def loadData(self):
        data = self.readData()
        print(data)
        self.motor.maxPos = data["maxPos"]
        self.sched.timers = data["times"]

    def readData(self):
        with open(self.filePath, 'r') as file:
            data = json.load(file)
        return data

    def writeData(self, data):
        with open(self.filePath, 'w') as outfile:
            json.dump(data, outfile)