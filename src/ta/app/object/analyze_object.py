from object_detection import yolo
import numpy as np
import cv2

def analyze_object(image):
    
    result = { "phone": False, "person": 0}

    image = np.array(image)
    image = image[:,:,:3]
    image = cv2.resize(image, (320, 320))
    image = image.astype(np.float32)
    image = np.expand_dims(image, 0)
    image = image / 255
    class_names = [c.strip() for c in open("models/classes.TXT").readlines()]
    boxes, scores, classes, nums = yolo(image)
    count=0
    for i in range(nums[0]):
        if int(classes[0][i] == 0):
            result["person"] += 1
        if int(classes[0][i] == 67):
            result["phone"] = True

    result_dict = {
        "object_result": result
    }

    return result_dict