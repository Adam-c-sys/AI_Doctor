"""
模块名称: pose_detector_demo.py
修改人: 同学 B
修改说明: 引入 warnings 模块，过滤并忽略来自 google.protobuf 的 SymbolDatabase 废弃警告
"""
import cv2
import mediapipe as mp
import numpy as np

import warnings
# 忽略特定的 Deprecated UserWarning，防止控制台刷屏
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf")
# ===================================================================

from angle_calculator import calculate_angle

def main():
    # 1. 初始化 MediaPipe Pose 模型
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    
    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[错误] 无法打开摄像头，请检查权限或设备连接")
        return

    print("[提示] 正在启动摄像头，请按 'q' 键退出程序")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame, 
                results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS
            )

            landmarks = results.pose_landmarks.landmark
            
            try:
                left_hip = [int(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * w),
                            int(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * h)]
                
                left_knee = [int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * w),
                             int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * h)]
                
                left_ankle = [int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * w),
                              int(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * h)]

                knee_angle = calculate_angle(left_hip, left_knee, left_ankle)

                if knee_angle < 120.0:
                    text_color = (0, 255, 0)
                    status_text = "Squatting: Active"
                else:
                    text_color = (0, 0, 255)
                    status_text = "Stand/Preparing"

                cv2.putText(frame, f"Knee Angle: {int(knee_angle)} deg", 
                            (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)
                cv2.putText(frame, status_text, 
                            (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2, cv2.LINE_AA)
                
                cv2.circle(frame, tuple(left_knee), 8, (255, 0, 0), -1)

            except Exception as e:
                pass

        cv2.imshow('AI Health Team - Pose Demo', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    pose.close()

if __name__ == "__main__":
    main()