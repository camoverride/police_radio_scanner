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
