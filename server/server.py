from flask import Flask, request

import sys
import numpy as np

sys.path.append("/home/kunalchandan/capstone/fydp_pi/fydp_pi/fast/server/Cone-of-Silence")
import inference

app = Flask(__name__)

@app.route('/processChunk', methods=['POST'])
def receive_chunk():
    num_channels = 5

    # Reshape PyAudio ByteStream into numpy array for COS
    audio_chunk = np.fromstring(request.data, dtype=np.int32)
    chunk_length = len(audio_chunk)//num_channels
    assert chunk_length == int(chunk_length)
    audio_chunk = np.reshape(audio_chunk, (num_channels, chunk_length))
    
    return 'Audio chunk received'


def run_inference():
    # Run inference
        
    inference.main(audio_chunk)

    return 'Audio chunk received'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000, ssl_context='adhoc')



