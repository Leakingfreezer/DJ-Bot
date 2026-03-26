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

        #Initializing hand model: detect only max 2 hands and only take 0.5 confidence
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        hand_data = {
            "hand_detected": False,
            "wrist_y": None,
            "index_tip_y": None,
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
            hand_data["wrist_y"] = landmarks[0].y
            hand_data["index_tip_y"] = landmarks[8].y
            hand_data["middle_tip_y"] = landmarks[12].y

        return frame, hand_data
    
if __name__ == "__main__":
    cam = cv2.VideoCapture(0)

    mediapipe_node = MediaPipeNode()

    while True:
        success, frame = cam.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)

        processed_frame, hand_data = mediapipe_node.process(frame)
        cv2.imshow("MediaPipe Test", processed_frame)

        #Exit key
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    #Release the camera
    cam.release()
    cv2.destroyAllWindows()