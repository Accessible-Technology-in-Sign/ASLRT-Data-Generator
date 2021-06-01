import sys
import os
import glob
import subprocess
import argparse
from tqdm import tqdm
import json

def find_phrase(video_name):
    phrase = video_name.split('.')[1]
    return phrase

def find_trial(video_name):
    trial = video_name.split('.')[2]
    return trial 

def generate_old_mediapipe(input_frames_directory, session, output_mediapipe_directory, base_mediapipe_directory, verbose):
    if verbose: print("Generating Mediapipe Data...")

    os.chdir(base_mediapipe_directory)

    build_mediapipe = 'bazel build -c opt --copt -DMESA_EGL_NO_X11_HEADERS mediapipe/copycat/multi_hand_tracking:multi_hand_tracking_gpu'

    output = subprocess.check_output(['bash','-c', build_mediapipe])

    input_session_directory = os.path.join(input_frames_directory, session)
    image_directories = glob.glob(os.path.join(input_session_directory, '*/*'))

    output_session_directory = os.path.join(output_mediapipe_directory, session)

    if os.path.exists(output_session_directory):
        answer = input("Session exists (may result in overwriting frame data). Continue (y/n)? ")
        if answer != 'y': sys.exit()
    else: os.makedirs(output_session_directory)

    for image_directory in tqdm(image_directories):
        if verbose: print("Processing {}".format(image_directory))

        phrase = image_directory.split('/')[-2]
        trial = image_directory.split('/')[-1]

        trial_directory = os.path.join(output_session_directory, phrase, trial)
        if not os.path.exists(trial_directory): os.makedirs(trial_directory)

        feature_filename = '.'.join((session, phrase, trial, 'data'))
        feature_filepath = os.path.join(trial_directory, feature_filename)

        runMediapipe = 'GLOG_logtostderr=1 \
                            bazel-bin/mediapipe/copycat/multi_hand_tracking/multi_hand_tracking_gpu \
                            --calculator_graph_config_file=mediapipe/copycat/graphs/multi_hand_tracking_and_face_detection_mobile.pbtxt \
                            --input_video_path="{}"/ \
                            --output_coords_path="{}"'.format(image_directory, feature_filepath)
        try:
            runOutput = subprocess.check_output(['bash','-c', runMediapipe])
        except:
            print("Done")


def generate_mediapipe(input_video_directory, session, output_mediapipe_directory, verbose):
    if verbose: print("Generating Mediapipe Data...")

    input_session_directory = os.path.join(input_video_directory, session)
    image_directories = glob.glob(os.path.join(input_session_directory, '*/*'))

    output_session_directory = os.path.join(output_mediapipe_directory, session)

    if os.path.exists(output_session_directory):
        answer = input("Session exists (may result in overwriting frame data). Continue (y/n)? ")
        if answer != 'y': sys.exit()
    else: os.makedirs(output_session_directory)

    for image_directory in tqdm(image_directories):
        if verbose: print("Processing {}".format(image_directory))

        phrase = image_directory.split('/')[-2]
        trial = image_directory.split('/')[-1]

        trial_directory = os.path.join(output_session_directory, phrase, trial)
        if not os.path.exists(trial_directory): os.makedirs(trial_directory)

        feature_filename = '.'.join((session, phrase, trial, 'data'))
        feature_filepath = os.path.join(trial_directory, feature_filename)
        runMediapipe = 'python3 mediapipePythonWrapper.py \
                            --video_path="{}" \
                            --feature_filepath="{}"'.format(glob.glob(os.path.join(image_directory, '*.mkv'))[0], feature_filepath)
        try:
            runOutput = subprocess.check_output(['bash','-c', runMediapipe])
        except:
            print("Done")

        # mediapipe_features(glob.glob(os.path.join(image_directory, '*.mkv'))[0], feature_filepath)
        if verbose: print("Processed {}".format(image_directory))

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_video_directory', type = str, default = '/mnt/ExtremeSSD/ProcessingPipeline/DATA/Frames', help = 'The base directory that contains formatted copycat videos. Unlikely to change.')
    parser.add_argument('--session', type = str, default = '07-24-20_p6_4KDepth', help = 'The name of the session for the videos. Format: "<month-day-year>_<user>_<comment>".')
    parser.add_argument('--output_mediapipe_directory', type = str, default = '/mnt/ExtremeSSD/ProcessingPipeline/DATA/Mediapipe_Data_July_2020', help = 'The base directory where the mediapipe data of the videos are created and saved to the copycat project. Unlikely to change.')
    parser.add_argument('--base_mediapipe_directory', type = str, default = '/path/to/mediapipe/directory/', help = 'The base directory where the google mediapipe is located. Unlikely to change.')
    parser.add_argument('--verbose', type = bool, required = False, default = True, help = 'Whether or not to print information to the terminal.')
    args = parser.parse_args()

    """

    Parameters
    ----------
    input_frames_directory : str
        The base directory where the frames of the videos are created and saved to the copycat project. Unlikely to change.

    session : str
        The name of the session for the videos. Format: "<month-day-year>_<user>_<comment>".

    output_mediapipe_directory : str
        The base directory where the mediapipe data of the videos are created and saved to the copycat project. Unlikely to change.

    base_mediapipe_directory : str
        The base directory where the google mediapipe is located. Unlikely to change.

    verbose : str
        Whether or not to print information to the terminal.

    """
    generate_mediapipe(args.input_video_directory, args.session, args.output_mediapipe_directory, args.verbose)