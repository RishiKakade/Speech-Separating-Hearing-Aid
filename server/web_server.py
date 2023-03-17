# required imports
import logging
from flask import Flask, request, render_template
from threading import Thread
import requests
import time
from queue import Queue
import queue
import socket
import struct
import urllib3
import pickle
import sounddevice as sd
from threading import Thread, Semaphore
import sys

semaphore = Semaphore(1)
selected_color = 'red'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(filename='web_server_log.txt',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')


# setting up fake queue
path_to_files = "/home/kunalchandan/capstone/fydp_pi/fydp_pi/fast/server/processed/input_stream/"

PI_URL = "http://192.168.0.102:5000"
INFERENCE_SERVER_URL = "https://192.168.0.100:8080"
INFERENCE_SERVER_IP = "192.168.0.100"

color_data = {
    "red": {"received": Queue(), "filename": ""},
    "blue": {"received": Queue(), "filename": ""},
    "orange": {"received": Queue(), "filename": ""},
    "green": {"received": Queue(), "filename": ""}
}

angle_string = "None, None, None, None"
client_sockets = []

# setting up flask app
app = Flask(__name__, static_url_path='', static_folder='static')

# creating global variables
rpi_is_recording = False

# Web Client to Web Server Interactions

# -----------------------------------------------
#
#
# HTTPS REQUESTS BETWEEN UI and SERVER --> START
#
#
# -----------------------------------------------

# Launch UI


@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
    return render_template('home.html')

# Start Recording on R.Pi


@app.route("/start_recording", methods=["GET"])
def start_recording_on_rpi():

    # getting global variable to store recording state and pi_url
    global rpi_is_recording
    global PI_URL

    if rpi_is_recording == True:
        return "already recording"

    # set the urls for the raspberry pi start recording and sending start request
    start_recording_url = f"{PI_URL}/startRecording"
    result = requests.get(start_recording_url, verify=False)

    # setting global rpi recording flag
    rpi_is_recording = True
    print(f"UITESTING: rpi_is_recording flag is now {rpi_is_recording}")
    return "successfully started recording"

# Stop Recording on R.Pi


@app.route("/stop_recording", methods=["GET"])
def stop_recording_on_rpi():

    # getting global variable to store recording state and pi_url
    global rpi_is_recording
    global PI_URL

    # set the urls for the raspberry pi (start and stop recording)
    stop_recording_url = f"{PI_URL}/stopRecording"
    result = requests.get(stop_recording_url, verify=False)

    rpi_is_recording = False
    print(f"UITESTING: rpi_is_recording flag is now {rpi_is_recording}")
    return "successfully started recording"

# Set Speaker Color


@app.route("/set_speaker_color", methods=["POST"])
def set_speaker_color():

    # get global variable to store speaker color
    global selected_color

    # get post request payload
    result = eval(request.data)
    color = result["body"]

    # semaphore.acquire()
    selected_color = color
    print(f"UITESTING: selected color is now {selected_color}")
    # semaphore.release()

    # server return message
    return "successfully set speaker color to"

# Run App


def run_web_server():
    app.run(host='0.0.0.0', port=9091, ssl_context='adhoc')

# -----------------------------------------------
#
#
# HTTPS REQUESTS BETWEEN UI and SERVER --> END
#
#
# -----------------------------------------------

def listener_angles():
    # create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_ip = INFERENCE_SERVER_IP
    port = 6960
    socket_address = (host_ip,port)
    client_socket.connect(socket_address)
    print('CONNECTED TO ANGLE SOCKET AT ',socket_address,'...')

    while (True):
        # receive the response
        response_bytes = client_socket.recv(1024)

        # decode the bytes to a string
        response_str = response_bytes.decode('utf-8')

        # print the response data
        print(f"RECEIVED ANGLES: {response_str}")
   


def listener_worker(color):
    # audio_data_q = []
    global color_data
    port_dict = {"red": 6969, "blue": 6970, "green": 6971, "orange": 6972}

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sockets.append(client_socket)
    # IP Address of Inference Server
    # TODO: Set in global
    host_ip = INFERENCE_SERVER_IP
    port = port_dict[color]

    socket_address = (host_ip, port)
    client_socket.connect(socket_address)
    print("CLIENT CONNECTED TO", socket_address)
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        t1 = time.time()
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)  # 4K
            if not packet:
                break
            data += packet

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        print(len(packed_msg_size))
        if len(packed_msg_size) == 8:
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4*1024)

            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)

            # not sure if this would exceed some size limit or smthg
            # audio_data_q.append(frame)
            t2 = time.time()
            print(f"Took {t2 - t1} seconds to download audio")
            color_data[color]["received"].put(frame)
            size = color_data[color]["received"].qsize()
            print(f"Length of queue is {size}")

            # Audio Consumer?
            # semaphore.acquire()
            # if selected_color == color:
            #     sd.play(audio_data_q.pop(0), 44100)
            # semaphore.release()


# Audio Player
def audio_worker():
    global color_data

    print("Started Audio Thread")

    while True:
        curr_speaker = selected_color
        if curr_speaker is not None:
            # print(f"CURRENT SPEAKER: {curr_speaker}")
            if not color_data[curr_speaker]["received"].empty():
                content = color_data[curr_speaker]["received"].get()
                color_data[curr_speaker]["received"].task_done()
                # print(f"Content type: {type(content)} \nContent data: ")
                t1 = time.time()
                sd.play(content, 44100)
                sd.wait()
                t2 = time.time()
                print(
                    f"Played {t2-t1} seconds of audio, Frame Size {len(content)}")
                # if (t2-t1) < 0.5:
                #     # Restart the audio consumer? Is this a good idea?
                #     raise sd.BufferError(f"Did not play audio in an appropriate amount of time took {t2-t1} seconds")
                # print(({"red", "blue", "orange", "green"} - {curr_speaker}))

                for color in ({"red", "blue", "orange", "green"} - {curr_speaker}):
                    try:
                        color_data[color]["received"].get_nowait()
                    except queue.Empty:
                        pass


def audio_player():
    while True:
        try:
            audio_worker()
        except Exception as e:
            print(e)


if __name__ == "__main__":

    web_server_thread = Thread(target=run_web_server)
    web_server_thread.start()

    listener_threads = []
    colors = ["red", "blue", "orange", "green"]

    for c in colors:
        color_thread = Thread(target=listener_worker, args=(c,))
        listener_threads.append(color_thread)
        color_thread.start()
    
#    angle_thread = Thread(target=listener_angles)
#    angle_thread.start()
#    listener_threads.append(angle_thread)

    audio_player_thread = Thread(target=audio_player)
    audio_player_thread.start()

    print(f"NUM_THREADS: {len(listener_threads)}") # 1 for each colour (4) and 1 for the angle = 5 
    try:
        pass
        # while True:
        #     val = input("Enter a color: ")
        #     semaphore.acquire()
        #     selected_color = val
        #     semaphore.release()
    except (KeyboardInterrupt, SystemExit):
        print("Exiting...")
        for t in listener_threads:
            t.join()
        for cs in client_sockets:
            cs.close()
        sys.exit()
