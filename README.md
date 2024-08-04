# Police Radio Scanner

What are the cops up to tonight?

Real-time analysis of police radio conversations in Seattle.


## Setup

Python dependencies (python 3.9.6):
- `python -m venv .venv`
- `source .venv/bin/activate`
- `sudo apt-get update`
- `sudo apt-get install libasound2-dev`
- `pip install -r requirements.txt`

FFMPEG:
- `sudo apt-get install ffmpeg`

Download Vosk model:
- `wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip`
- `unzip vosk-model-small-en-us-0.15.zip`

Create database:
- `python databse_utils.py`

Export credentials for S3 and OpenAI API:
- `export AWS_ACCESS_KEY_ID= access key`
- `export AWS_SECRET_ACCESS_KEY= secret key`
- `export AWS_DEFAULT_REGION=us-west-2`
- `export OPENAI_API_KEY= open ai key`


## Run

Start the restful API, which will return data to the front-end:
- `nohup python restful_api.py &`

Start `stream_radio.py`, containing the function `record_and_summarize`, which is responsible for many tasks: recording audio, saving it to s3, getting the transcription/summary, updating the recordings database, and updating `data.json`, which contains the most recent database entry.
- `nohup python stream_radio.py &`








<!-- 
Production mode:

Start a service with *systemd*. This will start the program when the computer starts and revive it when it dies

- `mkdir -p ~/.config/systemd/user`
- `~/.config/systemd/user/police_radio_scanner.service`
- paste in the contents of `police_radio_scanner.service`

Start the service using the commands below.

- `systemctl --user daemon-reload`
- `systemctl --user enable police_radio_scanner.service`
- `systemctl --user start police_radio_scanner.service`

Start it on boot: `sudo loginctl enable-linger pi`

Get the logs: `journalctl --user -u police_radio_scanner.service`

NOTE: takes about 71 seconds to record/transcribe 60 seconds of audio on RPi 4. -->


## Inspect Database

- `sudo apt install sqlite3`
- `sqlite3 recordings.db`
- `SELECT * FROM recordings LIMIT 10;`


## Settings

Adjust volume:
- `alsamixer`


## TODO:

- add a front-end that performs analysis on all the words we collect. However, first get a database!
- then pass over this database to get corrections + summaries
- auto-start program

- try bigger model
- analysis of words (get lots of recordings first)
- filter out ads
- benchmark on pi
- https://www.broadcastify.com/listen/mid/25
