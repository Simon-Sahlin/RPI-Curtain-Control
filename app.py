from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

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




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)