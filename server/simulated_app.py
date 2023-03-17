# required imports
from flask import Flask, render_template
from threading import Thread

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from queue import Queue
import time
import os

# setting up flask app
app = Flask(__name__, static_url_path='', static_folder='static')

# creating global variables for app functionality
start_recording_flag = False

# create global variables for fetching specified speaker data
speaker = None

# Global queue of received audio from server
received_audio_queue = Queue()

# Create function to set toggle button value
def get_toggle_button_value():

    #get global variable that holds recording button value
    global start_recording_flag

    #create string for button value
    toggle_button_value = ""

    #set toggle button value based on start recording flag
    if start_recording_flag == True:
        toggle_button_value = "Stop Recording"
    else:
        toggle_button_value = "Start Recording"
    
    #return the value of toggle button value
    return toggle_button_value


def get_source_path_value():

    if received_audio_queue.qsize() > 0 :
        result = received_audio_queue.get_nowait()
        output_name = result.headers["Content-Disposition"].split("=")[1].strip()
        # print(f"url_for('processed'): {url_for('processed')}")
        return os.path.join('processed', 'app_audio', output_name)
    else:
        return ''


# Home function
@app.route("/", methods=["POST", "GET"])
def home():
    toggle_button_value = get_toggle_button_value()
    audio_source_path = get_source_path_value()
    # audio_source_path = "/processed/app_audio/test.wav"

    return render_template('hello.html', toggle_button_value=toggle_button_value, audio_source_path=audio_source_path)


# Handle start and stop recording button press
@app.route("/toggle_recording", methods=["GET"])
def start_recording():
    
    # get global start_recording variable
    global start_recording_flag

    # setting the r.pi url for starting a recording
    start_recording_url = "http://10.0.0.64:5000/startRecording"
    stop_recording_url = "http://10.0.0.64:5000/stopRecording"
    
    # toggle the start_recording flag
    start_recording_flag = not(start_recording_flag)

    # set button value
    toggle_button_value = get_toggle_button_value()
    audio_source_path = get_source_path_value()


    print("start recording flag = " + str(start_recording_flag))

    # sending a get request to r.pi
    if start_recording_flag == True:
        result = requests.get(start_recording_url, verify=False)
    else:
        result = requests.get(stop_recording_url, verify=False)
    
    #return value for app handling

    return render_template('hello.html', toggle_button_value=toggle_button_value, audio_source_path=audio_source_path)


# TODO:: See if we can de-duplicate these functions... 
@app.route("/listen_red", methods=["GET"])
def listen_red_speaker():

    #get global variable for speaker specification
    global start_recording_flag
    global speaker
    global received_audio_queue
    speaker = "red"

    received_audio_queue.queue.clear()
    #set url for get request to inference server
    url = "https://127.0.0.1:8080/get_red_speaker"

    #send get request to inference server
    result = requests.get(url, verify=False)

    toggle_button_value = get_toggle_button_value()
    audio_source_path = get_source_path_value()
    return render_template('hello.html', toggle_button_value=toggle_button_value, audio_source_path=audio_source_path)


@app.route("/listen_blue", methods=["GET"])
def listen_blue_speaker():

    #get global variable for speaker specification
    global start_recording_flag
    global speaker
    global received_audio_queue
    speaker = "blue"

    received_audio_queue.queue.clear()
    #set url for get request to inference server
    url = "https://127.0.0.1:8080/get_blue_speaker"

    #send get request to inference server
    result = requests.get(url, verify=False)

    toggle_button_value = get_toggle_button_value()
    audio_source_path = get_source_path_value()
    return render_template('hello.html', toggle_button_value=toggle_button_value, audio_source_path=audio_source_path)



@app.route("/listen_orange", methods=["GET"])
def listen_orange_speaker():

    # get global variable for speaker specification
    global start_recording_flag
    global speaker
    global received_audio_queue
    speaker = "orange"

    received_audio_queue.queue.clear()
    # set url for get request to inference server
    url = "https://127.0.0.1:8080/get_orange_speaker"

    # send get request to inference server
    result = requests.get(url, verify=False)

    toggle_button_value = get_toggle_button_value()
    audio_source_path = get_source_path_value()
    return render_template('hello.html', toggle_button_value=toggle_button_value, audio_source_path=audio_source_path)



@app.route("/listen_green", methods=["GET"])
def listen_green_speaker():

    # get global variable for speaker specification
    global start_recording_flag
    global speaker
    global received_audio_queue
    speaker = "green"

    received_audio_queue.queue.clear()
    # set url for get request to inference server
    url = "https://127.0.0.1:8080/get_green_speaker"

    # send get request to inference server
    result = requests.get(url, verify=False)

    toggle_button_value = get_toggle_button_value()
    audio_source_path = get_source_path_value()
    return render_template('hello.html', toggle_button_value=toggle_button_value, audio_source_path=audio_source_path)



# function to get audio from inference server
def get_audio_from_server():

    # get global queue to place item into
    global received_audio_queue
    while True:

        time.sleep(1)

        # set url to perform get request from inference server
        url = "https://127.0.0.1:8080/send_audio"

        # perform get request
        result = requests.get(url, verify=False)

        print("the size of the queue is now = " + str(received_audio_queue.qsize()))

        # add result to queue
        if speaker is not None:
            # print(f"result: {result}")
            # # print(f"content: {result.content}")
            # print(f"headers: {result.headers}")

            # write audio to folder to test
            # output_path = "/home/kunalchandan/capstone/fydp_pi/fydp_pi/fast/server/processed/app_audio"
            if result.headers['Content-Type'] == 'audio/wav':
                # TODO:: Don't save the entire audio file into the queue
                # only save the file path that we are saving it into
                received_audio_queue.put(result)

                output_name = result.headers["Content-Disposition"].split("=")[1].strip()

                # full_output = os.path.join(output_path, output_name)

                open(os.path.join('static', 
                                  'processed', 
                                  'app_audio', 
                                  output_name), 'wb').write(result.content)

                # open(full_output, "wb").write(result.content)
        

def run_app():
    app.run(host='0.0.0.0', port=9090, ssl_context='adhoc')

if __name__ == "__main__":
    get_audio_thread = Thread(target=get_audio_from_server)
    get_audio_thread.start()

    app_thread = Thread(target=run_app)
    app_thread.start()
