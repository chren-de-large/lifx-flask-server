from flask import Flask
import requests
from bearer import TOKEN

app = Flask(__name__)

HEADERS = {
    "Authorization": "Bearer %s" % TOKEN,
}

@app.route("/")
def main():
    return ""

@app.route("/start", methods=["POST"])
def passed():
    if request.method == "POST":
        data = {
            "power": "on",
            "color": "yellow saturation:1",
            "brightness": 1,
        }
        response = requests.post('https://api.lifx.com/v1/lights/all/state', data=data, headers=HEADERS)
    return success

@app.route("/travis", methods=["POST"])
def passed():
    if request.method == "POST":
        json_dict = request.get_json()
        success = json_dict['status_message']
        if success == "Passed" or success == "Fixed":
            data = {
                "period": 0.5,
                "cycles": 4,
                "color": "green",
            }
            response = requests.post('https://api.lifx.com/v1/lights/all/effects/pulse', data=data, headers=HEADERS)
        else:
            data = {
                "period": 0.1,
                "cycles": 10,
                "color": "red",
            }
            response = requests.post('https://api.lifx.com/v1/lights/all/effects/pulse', data=data, headers=HEADERS)
    return success

if __name__ == "__main__":
    app.run(host='0.0.0.0')