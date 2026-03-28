#python nodes/gesture.py

"""
Purpose: 
1. Get frame
2. Run MediaPipe → get hand data
3. Send hand data → C++ gesture classifier
4. Get gesture label
5. Send gesture → action node
6. Display result

"""

import cv2

from mediapipe_node import MediaPipeNode
from action_node import DJActionNode
from utils.cpp_interface import classify_gesture_from_cpp
import ws_bridge


# Initialize everything needed for the pipeline
def initialize_system():
    camera = cv2.VideoCapture(0)
    mediapipe_node = MediaPipeNode()
    action_node = DJActionNode()

    ws_bridge.start()  # starts WebSocket server for dj_ui.html

    return camera, mediapipe_node, action_node


# Reads frame from camera and flips it
def get_frame(camera):
    success, frame = camera.read()

    if not success:
        return None

    frame = cv2.flip(frame, 1)
    return frame


# Determines gesture using C++ classifier
def get_gesture(hand_data):
    if not hand_data["hand_detected"]:
        return "none"

    gesture = classify_gesture_from_cpp(hand_data["landmarks"])
    return gesture


# Displays debug info on screen
def display_info(frame, gesture, action_text, action_node, hand_data):
    cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.putText(frame, f"Action: {action_text}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(frame, f"Hover: {action_node.hover_target}", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    cv2.putText(frame, f"Volume: {action_node.volume}", (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    cv2.putText(frame, f"Waveform: {action_node.waveform_scale:.2f}", (10, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    cv2.putText(frame, f"Turntable: {action_node.turntable_position:.2f}", (10, 180),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    cv2.putText(frame, f"Playing: {action_node.is_playing}", (10, 210),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    if hand_data["hand_detected"]:
        cv2.putText(
            frame,
            f"Index: ({hand_data['index_tip_x']:.2f}, {hand_data['index_tip_y']:.2f})",
            (10, 240),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )


# Main loop
def run_pipeline():
    camera, mediapipe_node, action_node = initialize_system()

    last_action = "No action"

    while True:
        frame = get_frame(camera)

        if frame is None:
            print("Camera error")
            break

        # Step 1: detect hand + landmarks
        processed_frame, hand_data = mediapipe_node.process(frame)

        # Step 2: classify gesture
        gesture = get_gesture(hand_data)

        # Step 3: run action logic
        last_action = action_node.execute(gesture, hand_data)

        # Step 4: show output
        display_info(processed_frame, gesture, last_action, action_node, hand_data)

        # Step 5: push state to React UI
        ws_bridge.broadcast({
            "gesture":             gesture,
            "last_action":         last_action,
            "hover_target":        action_node.hover_target,
            "is_playing":          action_node.is_playing,
            "volume":              action_node.volume,
            "waveform_scale":      action_node.waveform_scale,
            "turntable_position":  action_node.turntable_position,
            "index_x":             hand_data.get("index_tip_x"),
            "index_y":             hand_data.get("index_tip_y"),
        })

        cv2.imshow("DJ Bot Pipeline", processed_frame)

        # Exit key
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_pipeline()