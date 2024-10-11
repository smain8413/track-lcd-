import spotipy
from spotipy.oauth2 import SpotifyOAuth
import serial
import time
import atexit


# Spotify API credentials
SPOTIPY_CLIENT_ID = # create a new app and use its client id
SPOTIPY_CLIENT_SECRET = # make a new app and use its client secret
SPOTIPY_REDIRECT_URI = 'http://localhost:5173/callback'


def write(text):
    try:
        to_write = bytes(text, "ASCII")
    except UnicodeError:
        print(f"Warning: \"{text}\" had to be encoded in utf-8")
        to_write = bytes(text, "utf-8")

    arduino.write(to_write)


def read():
    return arduino.readline().strip().decode("utf-8")


def get_current_track_name():
    # Get current playing track information
    current_track = sp.current_playback()

    if not current_track:
        print("No track is currently playing.")
        return
    else:
        try:
            return current_track['item']['name']
        except TypeError:
            return


def get_current_track_artist():
    # Get current playing track information
    current_track = sp.current_playback()

    try:
        return current_track['item']['artists'][0]['name']
    except TypeError:
        return


def write_track(track):
    if track is None:
        towrite = "No tracks playing"
    else:
        towrite = str(track)  # Taking input from user

    print(f"Sending: {towrite}")
    write(towrite)
    time.sleep(.1)


def on_exit():
    write("quit")
    quit()


atexit.register(on_exit)

mode = input("Open chrome and input:\nA) Track and artist\nB) Track only\nC) Artist only\n").lower()
while mode not in ["a", "b", "c"]:
    mode = input("invalid input, try again!\n").lower()

# Set up Spotify API authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='user-read-currently-playing user-read-playback-state'))

# for i in range(10):
#    try:
time.sleep(.33)
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=3)
#    except PermissionError:
# print("COM3 not open, trying again")


while True:
    time.sleep(.075)
    output = read()
    print(output)
    time.sleep(.05)
    print(read())

    while str(output) != '1':
        time.sleep(.25)
        output = read()
        print(output, end='')
    if mode == "a":
        write_track(f"{get_current_track_name()}-{get_current_track_artist()}")
    elif mode == "b":
        write_track(get_current_track_name())
    elif mode == "c":
        write_track(get_current_track_artist())
