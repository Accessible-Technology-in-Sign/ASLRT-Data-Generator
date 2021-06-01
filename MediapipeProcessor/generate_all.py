import argparse

from rename_files import rename_files
from generate_mediapipe import generate_mediapipe

def generate_all(input_directory, pipeline, session, output_directory, output_frames_directory, output_mediapipe_directory, base_mediapipe_directory, verbose):

    if verbose: print("Generating for {} dataset".format(input_directory))

    rename_files(input_directory, session, output_directory, verbose)

    if pipeline == 'mediapipe':
    	# generate_frames(output_directory, session, output_frames_directory, verbose)
    	generate_mediapipe(output_directory, session, output_mediapipe_directory, verbose)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_directory', type = str, default = '../DATA/Videos', help = 'The base directory that contains the files to be renamed and added to the copycat project.')
    parser.add_argument('--pipeline', type = str, default = 'mediapipe', choices = ['mediapipe', 'kinect'], help = 'Whether to process mediapipe or kinect data.') 
    parser.add_argument('--session', type = str, default = '07-24-20_p6_4KDepth', help = 'The name of the session for the dataset. Format: "<month-day-year>_<user>_<comment>".')
    parser.add_argument('--output_directory', type = str, default = '../DATA/Videos', choices=['/media/thad/DataBackup/CopyCatDatasetWIP/RawProcessingPipeline/DATA/Videos', '/mnt/ExtremeSSD/ProcessingPipeline/DATA/Videos', '/mnt/ExtremeSSD/ProcessingPipeline/DATA/Kinect_Data_July_2020'], help = 'The base directory where the files are renamed and saved to the copycat project. Mediapipe (video files) or Kinect (json files) respectively.')
    
    parser.add_argument('--output_frames_directory', type = str, default = '../DATA/Frames', help = 'The base directory where the frames of the videos are created and saved to the copycat project. Unlikely to change. Kinect will not use this.')
    parser.add_argument('--output_mediapipe_directory', type = str, default = '../DATA/Mediapipe_Data_2020', help = 'The base directory where the mediapipe data of the videos are created and saved to the copycat project. Unlikely to change. Kinect will not use this.')
    parser.add_argument('--base_mediapipe_directory', type = str, default = '/path/to/mediapipe/install/directory', help = 'The base directory where the google mediapipe is located. Unlikely to change. Kinect will not use this.')
    parser.add_argument('--verbose', type = bool, required = False, default = True, help = 'Whether or not to print information to the terminal.')
    args = parser.parse_args()

    """

    Parameters
    ----------
    input_directory : str
        The base directory that contains the files to be renamed and added to the copycat project.

    pipeline : str
		Whether to process mediapipe or kinect data.

    session : str
        The name of the session for the dataset. Format: "<month-day-year>_<user>_<comment>".

    output_directory : str
        The base directory where the files are renamed and saved to the copycat project. Mediapipe (video files) or Kinect (json files) respectively.

    output_frames_directory : str
        DEPRECATED. The base directory where the frames of the videos are created and saved to the copycat project. Unlikely to change. Kinect will not use this.

    output_mediapipe_directory : str
        The base directory where the mediapipe data of the videos are created and saved to the copycat project. Unlikely to change. Kinect will not use this.

    base_mediapipe_directory : str
        The base directory where the google mediapipe is located. Unlikely to change. Kinect will not use this.

    verbose: str
        Whether or not to print information to the terminal.

    """
    generate_all(args.input_directory, args.pipeline, args.session, args.output_directory, args.output_frames_directory, args.output_mediapipe_directory, args.base_mediapipe_directory, args.verbose)
