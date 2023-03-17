# required imports
from flask import Flask, request, send_file

import sys
import os
import time
import numpy as np

from queue import Queue
import queue
from threading import Thread

import pyaudio
import wave
import soundfile as sf
import pickle
import socket
import struct

import logging
logging.basicConfig(filename='async_server_log.txt', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

sys.path.append("/home/kunalchandan/capstone/fydp_pi/fydp_pi/fast/server/Cone-of-Silence")
import inference

sys.path.append("/home/kunalchandan/capstone/fydp_pi/fydp_pi/fast/server/ConvTasNet/asteroid/")
from asteroid.models import ConvTasNet

#setting path to write input data to
input_data_path = "/home/kunalchandan/capstone/fydp_pi/fydp_pi/fast/server/processed/"

#initialize app
app = Flask(__name__)

#global variables

#global queue to store input files
g_queue = Queue()

color_buffer = {
"red":    Queue(),
"blue":   Queue(),
"orange": Queue(),
"green":  Queue(),
}
angle_buffer = {
"red":    Queue(),
"blue":   Queue(),
"orange": Queue(),
"green":  Queue(),
}

curr_angle_dict = {
    "red": None, 
    "blue": None,
    "orange": None,
    "green": None
}

prev_angle_dict = {
    "red": None, 
    "blue": None,
    "orange": None,
    "green": None
}

# Global variable to specify which speaker to send
speaker = None

# Ssave the incoming audio data into a wav file
def save_audio_data(fname, channels, format, sample_rate, frames):
    p = pyaudio.PyAudio()
    wf = wave.open(fname, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()


def run_ConvTasNet(filename):
    '''Overwrites @filename with what passes through ConvTasNet'''
    model = ConvTasNet.from_pretrained("mhu-coder/ConvTasNet_Libri1Mix_enhsingle")
    model.separate(filename, resample=True, force_overwrite=True)



# Run inference on audio input
def worker():

    # get global variables for output files and index
    global color_buffer
    global write_index
    global most_recent_file

    prev_output_angles = [None, None, None, None]

    # infinite loop - should always be running inference on latest audio input
    while True:
        # get latest audio input from queue
        input_file_name = g_queue.get()
        logging.info("inference_new_chunk")

        # Apply Cone of Silence on audio input
        output_files, output_angles = inference.main(input_file_name, prev_output_angles)
        prev_output_angles = output_angles
        logging.info("inference_cos")
        
        # Apply ConvTasNet to each output channel
        for output_file in output_files:
            if output_file is not None and os.path.exists(output_file):
                run_ConvTasNet(output_file)
        logging.info("inference_convtas")

        # TODO:: Run compression on each wav file
        logging.info("inference_compression")

        color_buffer["red"   ].put(output_files[0])
        color_buffer["blue"  ].put(output_files[1])
        color_buffer["orange"].put(output_files[2])
        color_buffer["green" ].put(output_files[3])

        # testing the most recent red file
        most_recent_file = output_files[0]

        curr_angle_dict["red"   ] = output_angles[0]
        curr_angle_dict["blue"  ] = output_angles[1]
        curr_angle_dict["orange"] = output_angles[2]
        curr_angle_dict["green" ] = output_angles[3]

        logging.info("inference_write_to_color_buffer")
        # incrementing the write_index counter (must wrap around)
        if os.path.isfile(input_file_name):
            os.remove(input_file_name)
        logging.info("inference_removing_chunk_file")

        # enqueued task is complete - other threads can now access the queue
        g_queue.task_done()
        logging.info("inference_end")

        # TODO:: Maybe clear all except latest?
        # Currently clearing queue if too large
        if g_queue.qsize() > 5:
            g_queue.queue.clear()


@app.route("/get_speaker_angles", methods=["GET"])
def get_speaker_angles():
    colors = ['red', 'blue', 'orange', 'green']
    return ", ".join([str(angle_buffer[color].get()) for color in colors])


# Send audio back to web-server
@app.route("/send_audio", methods=["GET"])
def send_audio_data():
    logging.info("chunk_http_tx_to_WS_start")
    # getting global variables
    global color_buffer
    global write_index

    # getting user passed color
    color = request.args.get('color')

    # If inference is not complete yet give something back
    try:
        fname = color_buffer[color].get(block=False)
    except queue.Empty:
        fname = ''

    data_path = f"/home/kunalchandan/capstone/fydp_pi/fydp_pi/fast/server/processed/{fname}"
    print("Data full path: " + data_path)

    if os.path.isfile(data_path):
        # TODO: File type may change
        logging.info("chunk_http_tx_to_WS_end")
        return send_file(data_path, mimetype="audio/wav")
    else:
        return "Not a valid path, fuck off", 200
    


# TODO Rename to save_file_to_inference_server
# Process and store incoming audio stream in queue
@app.route('/processChunk', methods=['POST'])
def receive_chunk():
    logging.info("chunk_http_rx_from_pi_start")
    num_channels = 5

    # Reshape PyAudio ByteStream into numpy array for COS
    logging.info("chunk_convert_bytes_start")
    audio_chunk = np.frombuffer(request.data, dtype=np.int32)
    chunk_length = len(audio_chunk)//num_channels
    assert chunk_length == int(chunk_length)
    audio_chunk = np.reshape(audio_chunk, (num_channels, chunk_length))
    logging.info("chunk_convert_bytes_end")

    # Save AUDIO DATA takes 3ms to run
    logging.info("chunk_write_start")
    input_file_name = f"{input_data_path}/input_stream/{int(time.time())%1000}.wav"
    save_audio_data(fname=input_file_name, 
                    channels=num_channels, 
                    format=pyaudio.paInt32, 
                    sample_rate=16000, 
                    frames=audio_chunk)
    logging.info("chunk_write_end")
    
    # placing audio input into queue
    g_queue.put(input_file_name)
    logging.info("chunk_http_rx_from_pi_end")
    # debugging statements
    # print(f"Length of global queue: {g_queue.qsize()}")
    # print(audio_chunk.shape)

    # required to complete post request
    return f'Audio chunk received {int(time.time())}'
    

def run_flask_server():
    app.run(host='0.0.0.0', port=8080, ssl_context='adhoc')


def web_socket_launcher(color):
    while True:
        try: 
            web_sockets(color)
        except Exception as e:
            print(e)

def angle_socket():

    global prev_angle_dict
    global curr_angle_dict

    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host_ip = '192.168.0.100'
    port = 6960
    backlog = 5
    socket_address = (host_ip,port)
    print('STARTING ANGLE SOCKET AT',socket_address,'...')
    server_socket.bind(socket_address)
    server_socket.listen(backlog)

    while(True):
        client_socket,addr = server_socket.accept()

        if (client_socket):
            while (True):
                if (prev_angle_dict != curr_angle_dict):
                    print("DICKS DON't MATCH")
                    colors = ['red', 'blue', 'orange', 'green']
                    angle_str = ", ".join([str(curr_angle_dict[color].get()) for color in colors])
                    message_bytes = angle_str.encode('utf-8')
                    # send the data over the socket
                    server_socket.sendall(message_bytes)
                    prev_angle_dict = curr_angle_dict
        else:
            break

    # close the socket
    server_socket.close()

def web_sockets(color):
    port_dict = {"red": 6969, "blue": 6970, "green": 6971, "orange": 6972}
    global length_of_array
    last_file_sent = None

    # setting up the web socket
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # Allows us to reuse the sockets, removes OS ERROR thing that requires us to kill PID
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host_ip = '192.168.0.100'
    port = port_dict[color]
    backlog = 5
    socket_address = (host_ip,port)
    print('STARTING SERVER AT',socket_address,'...')
    server_socket.bind(socket_address)
    server_socket.listen(backlog)

    while(True):
        client_socket,addr = server_socket.accept()
        # print('GOT CONNECTION FROM:',addr)

        if client_socket:
            while(True):
                
                directory = f'/home/kunalchandan/capstone/fydp_pi/fydp_pi/fast/server/processed/processed_{color}/'
                files = os.listdir(directory)
                files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
                try:
                    latest_file = os.path.join(directory, files[-1])
                except IndexError:
                    continue

                file_name = latest_file

                if file_name != last_file_sent:                    

                    #################### TODO: REMOVE SLEEP#####################################
                    #
                    #
                    time.sleep(4)
                    #
                    #
                    #################### TODO: REMOVE SLEEP#####################################

                    # if(os.path.exists(file_name)):
                    data, fs = sf.read(file_name, dtype='float32')
                    # print(f"just read data from {file_name}")
                    print(f"SENDING FRAME SIZE: {len(data)}")
                    # data, fs = sf.read("/home/kunalchandan/capstone/fydp_pi/fydp_pi/fast/server/processed/input_stream/132.wav", dtype='float32')
                    a = pickle.dumps(data)
                    message = struct.pack("Q",len(a))+a
                    client_socket.sendall(message)
                    last_file_sent = file_name

                    # os.remove(file_name)
                    # else:
                    #     print(f"{file_name} doesn't exist, skipping this file")
                else:
                    pass
                    # print(f"{color} color buffer empty")
        else:
            break

    client_socket.close()


if __name__ == "__main__":

    # create thread to run flask app
    server_thread = Thread(target=run_flask_server)
    server_thread.start()

    # create thread to run inference worker
    inference_thread = Thread(target=worker)
    inference_thread.start()

    colors = ["red", "blue", "orange", "green"]

    thread_list = []
    for c in colors:
        web_socket_thread = Thread(target=web_socket_launcher, args=(c,))
        thread_list.append(web_socket_thread)
        web_socket_thread.start()

    angle_thread = Thread(target=angle_socket)
    angle_thread.start()
    thread_list.append(angle_thread)

    print(f"NUM_IS_THREADS: {len(thread_list)}")

    try:
        pass
    except (KeyboardInterrupt, SystemExit):
        print("Exiting...")
        for t in thread_list:
            t.join()
 


