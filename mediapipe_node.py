import cv2
import mediapipe as mp

"""
Ultizing the mediapipe library and enabling hand tracking 
Show does it work: Opens up the mediapipe and reads the frame, will convert the frame from BGR to RGB 
then process the frame for hand detection and tracking. The frame converts back to RGB to BGR for OpenCV.
If hands are detected, will see if it matches or touches the "virtual screen" dj deck interface for logic interactions.
If the user presses the key 'q', this program will close
Returns: Raw data to the gesture classifier to idenitify what type of function to then execuate
Example Return:
hand_data = {
            "hand_detected": False,
            "wrist_y": None,
            "index_tip_y": None,
            "middle_tip_y": None
        }
"""

class MediaPipeNode:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        hand_data = {
            "hand_detected": False,
            "landmarks": None,
            "wrist_x": None,
            "wrist_y": None,
            "thumb_tip_x": None,
            "thumb_tip_y": None,
            "index_tip_x": None,
            "index_tip_y": None,
            "middle_tip_x": None,
            "middle_tip_y": None
        }

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            self.mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS
            )

            landmarks = hand_landmarks.landmark

            hand_data["hand_detected"] = True
            hand_data["landmarks"] = landmarks

            hand_data["wrist_x"] = landmarks[0].x
            hand_data["wrist_y"] = landmarks[0].y

            hand_data["thumb_tip_x"] = landmarks[4].x
            hand_data["thumb_tip_y"] = landmarks[4].y

            hand_data["index_tip_x"] = landmarks[8].x
            hand_data["index_tip_y"] = landmarks[8].y

            hand_data["middle_tip_x"] = landmarks[12].x
            hand_data["middle_tip_y"] = landmarks[12].y

        return frame, hand_data