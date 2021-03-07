# Here - Motion Tracking Sources

# Requirements
```
tensorflow => 2.2.0
opencv
mediapipe
numpy
```

## analyze_image.py

#### Methods

- **analyze_image()**
    - Analyzes the given image by passing the image
      through all image processing models.

## face_detect.py

#### Methods

- **init_model()**
    - Initializes the model
    - Returns a pre-trained OpenCV2 Caffe DNN model

- **find_faces(frame, model)**
    - Find the faces inside a given frame using the sent model
    - Returns a list of startX,Y and endX,Y coordinates for each
      of the faces found in the given frame

- **draw_faces_on_frame(frame, faces)**
    - Draws bounding rectangles around given faces on the given
      frame 

## face_landmark_detection.py

#### Methods

- **init_model()**
    - Initializes the model
    - Returns a pre-trained tensorflow model

- **assert_square_box(box)**
    - Converts the given box into a square box

- **detect_landmarks(frame, model, face)**
    - Detects the 68 landmarks on the given face using the given
      model.

## hand_gesture_detection.py

#### Methods

- **recognize_hand(image)**
    - Loads the image.
    - Recognizes the hand landmarks on the given frame
    - Calls recognize_hand_gesture.

- **recognize_hand_gesture(landmarks)**
    - Recognizes the hand gestures from the given landmarks.
