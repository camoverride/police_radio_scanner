# Police Radio Scanner

## Setup

Python dependencies (python 3.9.6):
- `python -m venv .venv`
- `source .venv/bin/activate`
- `sudo apt-get update`
- `sudo apt-get install libasound2-dev`
- `pip install -r requirements.txt`

Download Vosk model:
- `wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip`
- `unzip vosk-model-small-en-us-0.15.zip`

Create database:
- `python create_db.py`

Create location for db files:
- `mkdir audio_recordings`


## Run

Test:
- `nohup python stream_radio.py &`

Production mode:

Start a service with *systemd*. This will start the program when the computer starts and revive it when it dies. Copy the contents of `police_radio_stream.service` to `/etc/systemd/system/police_radio_stream.service` (via `sudo vim /etc/systemd/system/police_radio_stream.service`).

Start the service using the commands below.

- `sudo systemctl daemon-reload`
- Start it on boot: `sudo systemctl enable police_radio_stream.service` 
- Start it right now: `sudo systemctl start police_radio_stream.service`
- Stop it right now: `sudo systemctl stop police_radio_stream.service`
- Get logs: `sudo journalctl -u police_radio_stream | tail`



NOTE: takes about 71 seconds to record/transcribe 60 seconds of audio on RPi 4.


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
