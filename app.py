from flask import Flask, jsonify, render_template, url_for
import random

from stream_radio import record_and_summarize
from database_utils import create_connection


conn = create_connection("recordings.db")



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_audio')
def get_audio():
    # results = record_and_summarize(audio_stream_url="https://broadcastify.cdnstream1.com/31423",
    #                         recording_duration=10, # 300s = 5min chunk to reduce calls to API 
    #                         audio_save_dir="audio_recordings",
    #                         database_conn=conn)
    # audio_url = results["path_to_audio_file"]

    # Generate the URL for the local audio file

    """
    set global variables in constantly running function. This function simply imports them
    """

    fn = random.choice(["test_1.wav", "test_2.wav", "test_3.wav"])
    audio_url = url_for('static', filename=f'audio/{fn}')
    return jsonify({"audio_url": audio_url})


if __name__ == "__main__":
    app.run(debug=True)
