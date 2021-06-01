import argparse
import glob
import os
import shutil
import sys
from tqdm import tqdm

# MAY NEED TO EDIT custom_find_phrase depending on the original name of the video: currently implemented for user_wordone_wordtwo_..._trial#.mp4
def custom_find_phrase(video_name):
    # splits = video_name.split('_')
    # start = 0
    # end = len(splits) - 2

    # if splits[0] == 'trimmed': start = 1
    # while splits[end].isdigit(): end = end - 1

    # phrase = '_'.join(splits[start: end + 1])
    phrase = video_name.split('.')[0]
    return phrase

def find_phrase(video_name):
    phrase = video_name.split('.')[1]
    return phrase

def find_trial(phrase_directory):
    number = len(os.listdir(phrase_directory))
    return str(number).zfill(10) 

def rename_files(input_directory, session, output_directory, verbose):
    if verbose: print("Renaming Files...")

    filepaths = glob.glob(os.path.join(input_directory, '**'), recursive = True)
    filepaths = list(filter(lambda filepath: os.path.isfile(filepath), filepaths))

    output_session_directory = os.path.join(output_directory, session)
    print(output_session_directory)
    phrase = custom_find_phrase(filepaths[0].split('/')[-1])
    answer = input("For filename {}, is the following phrase in the correct format (y/n): {}  ".format(filepaths[0].split('/')[-1], phrase))
    if answer != 'y': sys.exit()

    if os.path.exists(output_session_directory):
        answer = input("Session exists (will try to append to session but may result in unexpected behavior). Continue (y/n)? ")
        if answer != 'y': sys.exit()
    else: os.makedirs(output_session_directory)

    for filepath in tqdm(filepaths):
        if verbose: print("Processing {}".format(filepath))
        filename = filepath.split('/')[-1]
        file_extention = filename.split('.')[-1]

        phrase = custom_find_phrase(filename)
        phrase_directory = os.path.join(output_session_directory, phrase)
        if not os.path.exists(phrase_directory): os.makedirs(phrase_directory)

        trial = find_trial(phrase_directory)
        trial_directory = os.path.join(phrase_directory, trial)
        if not os.path.exists(trial_directory): os.makedirs(trial_directory)

        new_filename = '.'.join((session, phrase, trial, file_extention))
        new_filepath = os.path.join(trial_directory, new_filename)
        shutil.copyfile(filepath, new_filepath)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_directory', type = str, default = '/mnt/ExtremeSSD/OriginalJSONFiles/08-10-20_p2_4K', help = 'The base directory that contains the files to be renamed and added to the copycat project.')
    parser.add_argument('--session', type = str, default = '04-xx-20_p3_4K', help = 'The name of the session for the dataset. Format: "<month-day-year>_<user>_<comment>".')
    parser.add_argument('--output_directory', type = str, default = '/mnt/ExtremeSSD/ProcessingPipeline/DATA/Videos', choices=['/mnt/ExtremeSSD/ProcessingPipeline/DATA/Videos', '/mnt/ExtremeSSD/ProcessingPipeline/DATA/Kinect_Data_July_2020'], help = 'The base directory where the files are renamed and saved to the copycat project. Mediapipe (video files) or Kinect (json files) respectively.')
    parser.add_argument('--verbose', type = bool, default = True, help = 'Whether or not to print information to the terminal.')
    args = parser.parse_args()

    """

    Parameters
    ----------
    input_directory : str
        The base directory that contains the files to be renamed and added to the copycat project.

    session : str
        The name of the session for the dataset. Format: "<month-day-year>_<user>_<comment>".

    output_directory : str
        The base directory where the files are renamed and saved to the copycat project. Mediapipe (video files) or Kinect (json files) respectively.

    verbose: str
        Whether or not to print information to the terminal.

    """
    rename_files(args.input_directory, args.session, args.output_directory, args.verbose)
