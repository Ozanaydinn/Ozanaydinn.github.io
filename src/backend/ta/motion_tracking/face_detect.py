import cv2
import numpy as np

def init_model():
    model = cv2.dnn.readNetFromCaffe("ta/motion_tracking/models/deploy.prototxt.txt",
                "ta/motion_tracking/models/res10_300x300_ssd_iter_140000.caffemodel")
    print(type(model))

    return model

def find_faces(frame, model):
    
    # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the detections and
    # predictions
    faces = []
    model.setInput(blob)
    detections = model.forward()

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]
        
        if confidence < 0.7 :
            continue
        # compute the (x, y)-coordinates of the bounding box for the
        # object
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        faces.append([startX, startY, endX, endY])

    return faces

def draw_faces_on_frame(frame, faces):

    for startX, startY, endX, endY in faces:

        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 3)