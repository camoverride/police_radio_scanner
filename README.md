# Radio Scanner

## Setup

Python dependencies (python 3.9.6):
- `python -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`

Download Vosk model:
- `wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15`
- `unzip vosk-model-small-en-us-0.15`

Create database:
- `python create_db.py`

Create location for db files:
- `mkdir audio_recordings`


## Run

- `python stream_radio.py`


## TODO:

- add a front-end that performs analysis on all the words we collect. However, first get a database!
- then pass over this database to get corrections + summaries
- auto-start program

- try bigger model
- analysis of words (get lots of recordings first)
- filter out ads
- benchmark on pi
- https://www.broadcastify.com/listen/mid/25
