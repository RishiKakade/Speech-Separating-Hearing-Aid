import os
import sys

import argparse

from voice_tracking import remap_voice_angles

sys.path.append("/home/kunalchandan/capstone/fydp_pi/fydp_pi/fast/server/Cone-of-Silence/cos/inference/")
import separation_by_localization

def run_ConeOfSilence(input_file_name):
    channels   = 4
    fs         = 44100 # 44100
    radius     = .03231
    model_path  = "/home/kunalchandan/capstone/fydp_pi/fydp_pi/fast/server/Cone-of-Silence/checkpoints/realdata_4mics_.03231m_44100kHz.pt" 
    output_path = "/home/kunalchandan/capstone/fydp_pi/fydp_pi/fast/server/processed/"

    #creating argument class object
    args = argparse.Namespace(debug=False, 
                                duration=10,
                                # audio_data=input_data,
                                input_file=input_file_name,
                                mic_radius=radius, 
                                model_checkpoint=model_path, 
                                moving=True, 
                                n_channels=channels, 
                                output_dir=output_path, 
                                sr=fs, 
                                use_cuda=True
                                )

    output_files, output_angles = separation_by_localization.main(args)
    return (output_files, output_angles)


def main(input_file_name, prev_angle_list):
    # Apply Cone of Silence to output
    output_files, output_angles = run_ConeOfSilence(input_file_name)
    # Do voice tracking
    output_angles, mapping_indices = remap_voice_angles(prev_angle_list, output_angles)
    new_output_files = [output_files[i] for i in mapping_indices]

    return new_output_files, output_angles

