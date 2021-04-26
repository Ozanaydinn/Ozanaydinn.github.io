from hand_gesture_detection import HandGesture

def analyze_hand(frame):

    hand_analyzer = HandGesture(frame)

    hand_result = hand_analyzer.recognize_hand()

    result_dict = {
        "hand_result": hand_result,
    }

    return result_dict
    