from flask import Flask, request
import requests, json
from bearer import TOKEN

app = Flask(__name__)

HEADERS = {
    "Authorization": "Bearer %s" % TOKEN,
}

color = 'white'
powerState = 'off'

def getState():
    response = requests.get('https://api.lifx.com/v1/lights/all', data={}, headers=HEADERS)
    hue = response.json()[0]['color']['hue']
    saturation = response.json()[0]['color']['saturation']
    kelvin = response.json()[0]['color']['kelvin']
    color_string = "hue:"+str(hue)+" saturation:"+str(saturation)+" kelvin:"+str(kelvin)
    powerState = response.json()[0]['power']

@app.route("/")
def main():
    getState()
    return ""

@app.route("/travis", methods=["POST"])
def passed():
    payload = json.loads(request.form['payload'])
    success = payload['status_message']
    if success == "Pending":
        getState()
        data = {
           "power": "on",
            "color": "yellow",
            "brightness": 1,
        }
        response = requests.post('https://api.lifx.com/v1/lights/all/state', data=data, headers=HEADERS)
        return success
    else:
        requests.post('https://api.lifx.com/v1/lights/all/effects/pulse', data={"color":color}, headers=HEADERS)
        if success == "Passed" or success == "Fixed":
            data = {
                "power": "on",
                "period": 0.5,
                "cycles": 6,
                "color": "green",
            }
            response = requests.post('https://api.lifx.com/v1/lights/all/effects/pulse', data=data, headers=HEADERS)
        else:
            data = {
                "power": "on",
                "period": 0.1,
                "cycles": 12,
                "color": "red",
            }
            response = requests.post('https://api.lifx.com/v1/lights/all/effects/pulse', data=data, headers=HEADERS)
    return success
if __name__ == "__main__":
    app.run()