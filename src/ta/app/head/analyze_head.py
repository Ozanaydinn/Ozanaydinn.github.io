from head_pose_estimation import HeadPoseEstimation
from face_detect import FaceDetect
from face_landmark_detection import FaceLandmark

def analyze_head(frame):

    face_detector = FaceDetect()
    face_landmark_detector = FaceLandmark()
    head_pose_analyzer = HeadPoseEstimation(frame, face_detector, face_landmark_detector)


    head_pose_result = head_pose_analyzer.estimate_head_pose()

    result_dict = {
        "head_pose_result": head_pose_result
    }

    return result_dict