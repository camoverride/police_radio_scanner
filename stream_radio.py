#!/home/pi/police_radio_scanner/.venv/bin/python

from datetime import datetime
import os
import subprocess
import wave
import json
import subprocess
import threading
# import simpleaudio as sa
from vosk import Model, KaldiRecognizer, SetLogLevel
import time

from database_utils import create_connection, add_recording_to_db
from summarization import get_summary
from aws_utils import upload_file_to_s3

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


# def play_audio_file(file_path):
#     """
#     Plays an audio file using simpleaudio.

#     Args:
#         file_path (str): The path to the audio file.
#     """
#     # Load the audio file
#     wave_obj = sa.WaveObject.from_wave_file(file_path)
    
#     # Play the audio file
#     play_obj = wave_obj.play()
    
#     # Wait for the playback to finish before exiting
#     play_obj.wait_done()


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


def record_and_summarize(audio_stream_url : str,
                             recording_duration : int,
                             database_conn : str,
                             ) -> dict:
    """
    The main event loop that gets audio from `audio_stream_url` in
    `recording_duration` second chunks, saves it to `audio_save_dir`,
    and writes the information to a database.

    Returns a dict:
        {
            "path_to_audio_file": "www.audio.com/file_1.wav",
            "transcription": "We are some people talking, this is our conversation."
            "summary": "People talked."
        }
    """
    # Recording start time
    start_time = datetime.now()
    print(start_time)

    # Get the path to the audio file
    audio_file_path = "__tmp_audio.wav" # os.path.join(audio_save_dir, f"audio_{date_string}.wav")

    # Record audio
    print(f"   Recording ...")
    # TODO: output data instead of path
    record_audio_from_url(url=audio_stream_url,
                          num_secs=recording_duration,
                          output_file=audio_file_path)

    # Get transcription
    print(f"   Transcribing ...")
    # TODO: consume data instead of path
    transcription = perform_asr_on_file(audio_file_path)
    print(transcription)

    # Get the summary
    print(f"   Summarizing ...")
    summary = get_summary(transcription)
    print(summary)

    # Insert this information info the database
    print(f"   Inserting into database ...")
    add_recording_to_db(conn=database_conn,
                        filename=audio_file_path,
                        transcription=transcription,
                        summary=summary)
    
    # Get the date for file naming
    s3_file_name = f"police_audio_{start_time.strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3]}.wav"

    # Upload the file to S3
    s3_file_path = upload_file_to_s3(path_to_file=audio_file_path,
                                     file_name=s3_file_name,
                                     bucket="police-radio-data")

    # Play audio
    # print(f"   Playing: {audio_file_path}")
    # play_audio_file_async(audio_file_path)
    # print("--------------------")

    # Return a dict
    data = {"path_to_audio_file": s3_file_path,
            "transcription": transcription,
            "summary": summary}
    
    # `recording_length` seconds must have elapsed betwee the beginning of the recording and
    # when it gets played. Pause until `recording_length` secs have elapsed.
    while (datetime.now() - start_time).total_seconds() < recording_duration:
        time.sleep(0.1)

    return data



if __name__ == "__main__":

    # Create a database connection
    DATABASE_PATH = "recordings.db"
    conn = create_connection(DATABASE_PATH)

    while True:
        results = record_and_summarize(audio_stream_url="https://broadcastify.cdnstream1.com/31423",
                             recording_duration=60, # 300s = 5min chunk to reduce calls to API 
                             database_conn=conn)

        # Write the s3 path to info.txt
        print("   Writing to `data.json`")
        print("-------------------------------------------")

        # TODO: write to a json instead!
        # Write to a JSON file
        with open("data.json", "w") as json_file:
            json.dump(results, json_file, indent=4)

