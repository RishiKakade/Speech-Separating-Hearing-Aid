from flask import Flask, request
import subprocess

import threading

import os
import sys
import argparse  # Argment parser

from collections import deque 
import numpy as np

import time
import librosa  # Music and audio analysis

import pyaudio
import sounddevice as sd
import requests 
app = Flask(__name__)
recording_now = False

def gen_header(sr, bits_per_sample, channels):
    datasize = 2000*10**6
    o = bytes("RIFF",'ascii')
    o += (datasize + 36).to_bytes(4,'little')
    o += bytes("WAVE",'ascii')
    o += bytes("fmt ",'ascii')
    o += (16).to_bytes(4,'little')
    o += (1).to_bytes(2,'little')
    o += (channels).to_bytes(2,'little')
    o += (sr).to_bytes(4,'little')
    o += (sr * channels * bits_per_sample // 8).to_bytes(4,'little')
    o += (channels * bits_per_sample // 8).to_bytes(2,'little')
    o += (bits_per_sample).to_bytes(2,'little')
    o += bytes("data",'ascii')
    o += (datasize).to_bytes(4,'little')
    return o


def stream_chunks():
    # when started, starts writing audio data to np array. 
    # streams audio in chunk until RECORD_SECONDS

    p = pyaudio.PyAudio()
    CHUNK = 1024
    FORMAT = pyaudio.paInt32
    BITS_PER_SAMPLE = 32
    CHANNELS = 5
    RATE = 16000
    wav_header = gen_header(RATE, BITS_PER_SAMPLE, CHANNELS)

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording started.")

    first_run = True
    global recording_now
    while recording_now:
        if first_run:
            data = wav_header + stream.read(CHUNK)
            first_run = False
        else:
            data = stream.read(CHUNK)

        result = requests.post( url="https://192.168.2.12:6000/processChunk",
                                auth=("fydp", "kierstenoverton2000$"),
                                data=data)


@app.route("/startRecording", methods=["GET"])
def start_recording():
    global recording_now
    recording_now = True
    thread = threading.Thread(target=stream_chunks)
    thread.start()
    return "Streaming started", 200


@app.route("/stopRecording", methods=["GET"])
def stop_recording():
    global recording_now
    if recording_now:
        recording_now = False
    return "Streaming stopped", 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
