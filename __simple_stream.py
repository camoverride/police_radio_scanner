import vlc
import time

def stream_and_play_audio(url):
    try:
        # Create an instance of VLC player
        player = vlc.MediaPlayer(url)

        # Start playing the audio stream
        player.play()

        # Allow some time for the stream to start
        time.sleep(5)  # Wait 5 seconds for the player to start

        # Check if the audio is playing
        playing = player.is_playing()
        if playing:
            print("Audio is playing...")
        else:
            print("Failed to start playing audio. Checking for potential issues...")
            state = player.get_state()
            print(f"Player state: {state}")

        # Keep the script running while the audio is playing
        input("Press Enter to stop the playback...\n")
        player.stop()
    except Exception as e:
        print(f"An error occurred: {e}")

# URL of the radio feed
url = "http://streams.kqed.org/kqedradio"
url = "https://broadcastify.cdnstream1.com/31423"

# Call the function
stream_and_play_audio(url)
