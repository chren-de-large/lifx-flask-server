from flask import Flask
import requests, jsonify

app = Flask(__name__)
TOKEN = "your_token"
HEADERS = {
    "Authorization": "Bearer %s" % TOKEN,
}

@app.route("/")
def main():
    return ""

@app.route("/travis", methods=["POST"])
def passed():
    if request.method == "POST":
        json_dict = request.get_json()
        success = json_dict['status_message']
        if success == "Passed":
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
    app.run()