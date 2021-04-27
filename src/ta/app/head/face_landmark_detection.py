import cv2
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras

class FaceLandmark:
    def init_model(self):
        model = keras.models.load_model("models/pose_model", compile=False)
        return model    

    def assert_square_box(self, box):
        '''
        box[0] -> leftmost x coord.
        box[1] -> topmost y coord.
        box[2] -> rightmost x coord.
        box[3] -> bottom y coord.
        '''

        width = box[2] - box[0]
        height = box[3] - box[1]

        diff = width - height
        amount_to_expand = int(abs(diff)/2)

        if diff == 0:
            return box
        elif diff > 0:

            box[1] -= amount_to_expand
            box[3] += amount_to_expand

            if diff % 2 == 1:
                box[3] += 1
        else:
            box[0] -= amount_to_expand
            box[2] += amount_to_expand

            if diff % 2 == 1:
                box[2] += 1
        
        assert((box[2] - box[0]) == (box[3] - box[1]))

        return box

    def detect_landmarks(self, frame, model, face):

        offset = int(abs((face[3] - face[1]) * 0.1))

        face[1] += offset
        face[3] += offset
        
        drawing_square_box = self.assert_square_box(face)

        height, width = frame.shape[:2]

        for i in range(4):
            if i == 2 and drawing_square_box[i] > width:
                drawing_square_box[i] = width
            elif i == 3 and drawing_square_box[i] > height:
                drawing_square_box[i] = height 
            elif drawing_square_box[i] < 0:
                drawing_square_box[i] = 0

        face_frame = cv2.cvtColor(cv2.resize(frame[drawing_square_box[1]: drawing_square_box[3],
                                drawing_square_box[0]: drawing_square_box[2]], (128,128)), cv2.COLOR_BGR2RGB)

        preds = model.signatures["predict"](tf.constant([face_frame], dtype=tf.uint8))

        landmarks = np.reshape(np.array(preds['output']).flatten()[:136], (-1,2))

        landmarks *= (drawing_square_box[2]- drawing_square_box[0])

        landmarks[:, 0] += drawing_square_box[0]
        landmarks[:, 1] += drawing_square_box[1]

        landmarks = landmarks.astype(np.uint)

        return landmarks
    

