from datetime import datetime
import os
import subprocess
import wave
import json
import subprocess
import threading
import simpleaudio as sa
from vosk import Model, KaldiRecognizer, SetLogLevel
import time

from create_db import create_connection, add_recording_to_db

# Set the environment variable to suppress Vosk logs
SetLogLevel(-1)



def record_audio_from_url(url, num_secs, output_file):
    """
    Records audio from the given URL for the specified number of seconds and saves it to the output file.

    Args:
        url (str): The URL to record audio from.
        num_secs (int): The number of seconds to record.
        output_file (str): The file to save the recorded audio to.
    """
    command = [
        'ffmpeg',
        '-y',  # Overwrite output file if it exists
        '-i', url,
        '-t', str(num_secs),
        '-acodec', 'pcm_s16le',
        '-ar', '44100',
        '-ac', '1',
        output_file
    ]
    subprocess.run(command, capture_output=True, text=True, check=True)


def perform_asr_on_file(audio_file, model_path="vosk-model-small-en-us-0.15"):
    """
    Reads an audio file and performs ASR on it using Vosk, returning the transcribed text.
    """
    
    # Load the Vosk model
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 44100)
    
    # Read the audio file
    wf = wave.open(audio_file, "rb")
    
    # Check if the audio file is in the correct format
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 44100:
        print("Audio file must be WAV format mono PCM.")
        return ""
    
    result_text = ""
    
    # Process the audio file
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_json = json.loads(result)
            result_text += result_json.get("text", "") + " "
    
    result = recognizer.FinalResult()
    result_json = json.loads(result)
    result_text += result_json.get("text", "")
    
    return result_text.strip()


def play_audio_file(file_path):
    """
    Plays an audio file using simpleaudio.

    Args:
        file_path (str): The path to the audio file.
    """
    # Load the audio file
    wave_obj = sa.WaveObject.from_wave_file(file_path)
    
    # Play the audio file
    play_obj = wave_obj.play()
    
    # Wait for the playback to finish before exiting
    play_obj.wait_done()


def play_audio_file_async(file_path):
    """
    Plays an audio file using simpleaudio in a separate thread.

    Args:
        file_path (str): The path to the audio file.
    """
    def audio_thread():
        # Load the audio file
        wave_obj = sa.WaveObject.from_wave_file(file_path)
        
        # Play the audio file
        play_obj = wave_obj.play()
        
        # Wait for the playback to finish
        play_obj.wait_done()

    # Create and start the thread
    thread = threading.Thread(target=audio_thread)
    thread.start()



if __name__ == "__main__":
    # Create a database connection
    conn = create_connection("recordings.db")

    # Determine where to save the audio files
    audio_save_dir = "audio_recordings"

    # How long should a recording be?
    recording_length = 60

    # The data URL
    url = "https://broadcastify.cdnstream1.com/31423"
    # url = "http://streams.kqed.org/kqedradio"
    # url = "https://broadcastify.cdnstream1.com/40685" # King County Fire and Police South

    # Main event loop.
    while True:
        # Record the start time
        start_time = datetime.now()
        print(start_time)

        # Get the date for file naming.
        date_string = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        # Get the path to the audio file.
        audio_file_name = os.path.join(audio_save_dir, f"audio_{date_string}.wav")

        # Record audio
        print(f"   Recording ...")
        record_audio_from_url(url, recording_length, audio_file_name)

        # Get transcription
        print(f"   Transcribing ...")
        transcription = perform_asr_on_file(audio_file_name)
        print(transcription)

        # Insert this information info the database
        print(f"   Inserting into database ...")
        add_recording_to_db(conn=conn,
                            filename=audio_file_name,
                            transcription=transcription)

        # `recording_length` seconds must have elapsed betwee the beginning of the recording and
        # when it gets played. Pause until `recording_length` secs have elapsed.
        while (datetime.now() - start_time).total_seconds() < 60:
            time.sleep(0.1)
            
        # Play audio
        print(f"   Playing: {audio_file_name}")
        play_audio_file_async(audio_file_name)
        print("--------------------")
