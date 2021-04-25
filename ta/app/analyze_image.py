from hand_gesture_detection import HandGesture
from head_pose_estimation import HeadPoseEstimation
from face_detect import FaceDetect
from face_landmark_detection import FaceLandmark


def analyze_image(frame):

    face_detector = FaceDetect()
    face_landmark_detector = FaceLandmark()
    hand_analyzer = HandGesture(frame)
    head_pose_analyzer = HeadPoseEstimation(frame, face_detector, face_landmark_detector)

    hand_result = hand_analyzer.recognize_hand()

    head_pose_result = head_pose_analyzer.estimate_head_pose()

    #phone_result = object_analyzer.search_phone()

    print("Hand_result: ",hand_result, " Head pose result: ", head_pose_result)
