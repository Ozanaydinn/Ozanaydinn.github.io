import mediapipe as mp
import numpy as np
import sys

class HandGesture:

  def __init__(self, image):
    self.image = image

  def recognize_hand_gesture(self, landmarks):
    thumbState = 'UNKNOWN'
    indexFingerState = 'UNKNOWN'
    middleFingerState = 'UNKNOWN'
    ringFingerState = 'UNKNOWN'
    littleFingerState = 'UNKNOWN'
    recognizedHandGesture = None

    pseudoFixKeyPoint = landmarks[2]['x']
    if (landmarks[3]['x'] < pseudoFixKeyPoint and landmarks[4]['x'] < landmarks[3]['x']):
      thumbState = 'CLOSE'    
    elif (pseudoFixKeyPoint < landmarks[3]['x'] and landmarks[3]['x'] < landmarks[4]['x']):
      thumbState = 'OPEN'    

    pseudoFixKeyPoint = landmarks[6]['y']
    if (landmarks[7]['y'] < pseudoFixKeyPoint and landmarks[8]['y'] < landmarks[7]['y']):
      indexFingerState = 'OPEN'    
    elif (pseudoFixKeyPoint < landmarks[7]['y'] and landmarks[7]['y'] < landmarks[8]['y']):
      indexFingerState = 'CLOSE'    

    pseudoFixKeyPoint = landmarks[10]['y']
    if (landmarks[11]['y'] < pseudoFixKeyPoint and landmarks[12]['y'] < landmarks[11]['y']):
      middleFingerState = 'OPEN'    
    elif (pseudoFixKeyPoint < landmarks[11]['y'] and landmarks[11]['y'] < landmarks[12]['y']):
      middleFingerState = 'CLOSE'

    pseudoFixKeyPoint = landmarks[14]['y']
    if (landmarks[15]['y'] < pseudoFixKeyPoint and landmarks[16]['y'] < landmarks[15]['y']):
      ringFingerState = 'OPEN'    
    elif (pseudoFixKeyPoint < landmarks[15]['y'] and landmarks[15]['y'] < landmarks[16]['y']):
      ringFingerState = 'CLOSE'
    
    pseudoFixKeyPoint = landmarks[18]['y']
    if (landmarks[19]['y'] < pseudoFixKeyPoint and landmarks[20]['y'] < landmarks[19]['y']):
      littleFingerState = 'OPEN'    
    elif (pseudoFixKeyPoint < landmarks[19]['y'] and landmarks[19]['y'] < landmarks[20]['y']):
      littleFingerState = 'CLOSE'
      
    if (thumbState == 'OPEN' and indexFingerState == 'OPEN' and middleFingerState == 'OPEN' and ringFingerState == 'OPEN' and littleFingerState == 'OPEN'):
      recognizedHandGesture = 5 # "FIVE"   
    elif (thumbState == 'CLOSE' and indexFingerState == 'OPEN' and middleFingerState == 'CLOSE' and ringFingerState == 'CLOSE' and littleFingerState == 'CLOSE'):
      recognizedHandGesture = 1 # "ONE"    
    else:
      recognizedHandGesture = 0 # "UNKNOWN"

    result_dict = {
      "thumbState": thumbState,
      "indexFingerState": indexFingerState,
      "middleFingerState": middleFingerState,
      "ringFingerState": ringFingerState,
      "littleFingerState": littleFingerState,
      "recognizedHandGesture": recognizedHandGesture
    }
    
    return result_dict

  def recognize_hand(self):
    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5)
        
    # Read an image, flip it around y-axis for correct handedness output (see
    # above).
    self.image = np.array(self.image)
    self.image = self.image[:,:,:3]
    # Convert the BGR image to RGB before processing.
    results = hands.process(self.image)

    if results.multi_hand_landmarks:
        
      image_hight, image_width, _ = self.image.shape

      hand_gestures = []

      for hand_landmarks in results.multi_hand_landmarks:
        keypoints = []

        for data_point in hand_landmarks.landmark:
          keypoints.append({'x': data_point.x, 'y': data_point.y, 'z': data_point.z})

        hand_gestures.append(self.recognize_hand_gesture(keypoints))
    else: 
      return "No Hand found"

    hands.close()

    return hand_gestures
