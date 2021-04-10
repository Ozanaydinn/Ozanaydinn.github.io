from ta.motion_tracking.hand_gesture_detection import recognize_hand_gesture
from ta.motion_tracking.head_pose_estimation import estimate_head_pose
from ta.motion_tracking.object_detection import search_phone


def analyze_image(frame):

    
    hand_result = recognize_hand_gesture(frame)
    estimate_head_pose(frame)
    phone_result = search_phone(frame)

    print("Hand_result: " + hand_result + " Phone result: " + phone_result)
