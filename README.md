# ASLRT-Data-Generator

flipMediapipe.py: Flips landmarks on Mediapipe data files from left to right. Useful for left-handed signers.

generate\_all.py: Generates Mediapipe data files from a directory containing videos of the form (phrase).(trial number).(timestamp).mkv

generate\_mediapipe.py, mediapipePythonWrapper.py, rename\_files.py: Used by generate_all.py

mediapipeViz.py: Visualizes Mediapipe skeleton on specified video

KinectProcessor/get\_jsons.py: Generates Kinect data files from a directory containing videos of the form (phrase).(trial number).(timestamp).mkv. Requires libk4a1.3-dev.

Documentation within the scripts provides further information on usage.
