from flask import Flask
from flask import render_template
from flask import request
import datetime as dt
from motorController import MotorController
from scheduleManager import ScheduleManager
from dataManager import DataManager

app = Flask(__name__)
motor = MotorController()
scheduleManager = ScheduleManager(motor, app)
scheduleManager.startWatch()
dataManager = DataManager(motor, scheduleManager)
dataManager.loadData()


@app.get("/")
def index():
    return render_template("index.html", 
        curtainPos = motor.curPos,
        maxPos = motor.maxPos,
        tomorrowTime = scheduleManager.timers[(dt.datetime.today().weekday() + 1) % 7],
        timers = scheduleManager.timers
    )

@app.post("/")
def getData():
    try:
        print(request.json)
        motor.curPos = int(request.json["currentPos"])
        motor.maxPos = int(request.json["maxPos"])
        scheduleManager.timers = request.json["times"]

        dataManager.writeData(request.json)

        return "Request Recived"
    except Exception as e:
        print(e)
        return str(e), 400

@app.post("/action")
def getAction():
    try:
        print(request.json)
        action = request.json["action"]
        if (action == "moveTo"):
            position = float(request.json['value'])
            motor.stopMotor()
            response = motor.moveMotor(position)
            return response, 200
        elif (action == "stop"):
            response = motor.stopMotor()
            return response, 200
        else:
            raise Exception("Invalid Action")
    except Exception as e:
        print(e)
        return str(e), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)




# import time


# motorController = MotorController()



# print(motorController.moveMotor(0))
# time.sleep(5)
# print(motorController.stopMotor())
