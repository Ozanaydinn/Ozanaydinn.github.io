from hand_gesture_detection import recognize_hand_gesture
from head_pose_estimation import estimate_head_pose
from object_detection import search_phone


def analyze_image(frame):

    
    hand_result = recognize_hand_gesture(frame)
    head_pose_result = estimate_head_pose(frame)
    phone_result = search_phone(frame)

    print("Hand_result: " + hand_result + " Head Pose Result: " + head_pose_result + " Phone result: " + phone_result)
