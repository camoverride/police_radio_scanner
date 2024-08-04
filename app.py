import json
from flask import Flask, jsonify, render_template



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_audio")
def get_audio():

    # `data.json` is where the latest audio information is recorded.
    with open("data.json", "r") as json_file:
        data = json.load(json_file)

    # Return this data to the front-end every time the audio player restarts
    # TODO: make sure audio player loops infinitely
    return jsonify({"audio_url": data["path_to_audio_file"],
                    "summary": data["summary"]})



if __name__ == "__main__":
    app.run(debug=True)
