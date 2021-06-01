import cv2
import mediapipe as mp
import argparse
import json

def mediapipe_features(video_path, feature_filepath):
  mp_drawing = mp.solutions.drawing_utils
  mp_holistic = mp.solutions.holistic
  holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.1)
  cap = cv2.VideoCapture(video_path)
  curr_frame = 0
  features = {}
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      # print("Video Processing Done")
      break
    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # DON'T FLIP THE IMAGE!!
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = holistic.process(image)
    # Available features:
    # results.face_landmarks
    # results.left_hand_landmarks
    # results.right_hand_landmarks
    # results.pose_landmarks
    curr_frame_features = {"pose":{}, "landmarks":{0:{}, 1:{}}}
    available_features = [results.left_hand_landmarks, results.right_hand_landmarks, results.pose_landmarks]
    feature_location = [curr_frame_features["landmarks"][0], curr_frame_features["landmarks"][1], curr_frame_features["pose"]]
    for index, curr_feature in enumerate(available_features):
      feature_num = 0
      if curr_feature is None:
        feature_location[index] = "None"
      else:
        for curr_point in curr_feature.landmark:
          feature_location[index][feature_num] = [curr_point.x, curr_point.y, curr_point.z]
          feature_num += 1
    features[curr_frame] = curr_frame_features
    curr_frame += 1
  holistic.close()
  cap.release()
  with open(feature_filepath, "w") as outfile:  
    json.dump(features, outfile, indent=4)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--video_path', type = str, default = '', help = 'The video which needs to be processed')
  parser.add_argument('--feature_filepath', type = str, default = '', help = 'The file where features should be stored')
  args = parser.parse_args()
  mediapipe_features(args.video_path, args.feature_filepath)

