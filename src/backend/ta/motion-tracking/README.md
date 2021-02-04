# Here - Motion Tracking Sources



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

