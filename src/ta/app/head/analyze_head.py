from head_pose_estimation import estimate_head_pose

def analyze_head(frame):

    head_pose_result = estimate_head_pose(frame)

    result_dict = {
        "head_pose_result": head_pose_result
    }

    return result_dict