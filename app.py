from flask import Flask
from flask import render_template
from flask import request
from motorController import MotorController
from scheduleManager import ScheduleManager

app = Flask(__name__)
motor = MotorController()
scheduleManager = ScheduleManager(motor, app)
scheduleManager.startWatch()


@app.teardown_appcontext
def shutdown_session(exception=None):
    print("SHUTTING DOWN")


@app.get("/")
def index():
    return render_template("index.html", 
        curtainPos= 32034,
        maxPos= 5500*16,
        tomorrowTime="09:00",
        lowerTime="22:30",
        mondayTime="09:00",
        tuesdayTime="08:00",
        wednesdayTime="08:00",
        thursdayTime="08:00",
        fridayTime="09:00",
        saturdayTime="10:00",
        sundayTime="10:00"
    )

@app.post("/")
def getData():
    print(request.json)
    return "Request Recived"

@app.post("/action")
def getAction():
    try:
        action = request.json["action"]
        print(request.json)
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
