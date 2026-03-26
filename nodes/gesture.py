import cv2 as cv
import mediapipe as mp

mp_hands = mp.solutions.hands
drawing = mp.solutions.drawing_utils
drawing_styles = mp.solutions.drawing_styles

"""
Ultizing the mediapipe library and enabling hand tracking 
Show does it work: Opens up the mediapipe and reads the frame, will convert the frame from BGR to RGB 
then process the frame for hand detection and tracking. The frame converts back to RGB to BGR for OpenCV.
If hands are detected, will see if it matches or touches the "virtual screen" dj deck interface for logic interactions.
If the user presses the key 'q', this program will close
"""

#Opening the camera
cap = cv.VideoCapture(0)

#Initializing hand model
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:
    while True:
        #Reading a frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Could not read webcam.")
            break

        frame = cv.flip(frame, 1)
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    drawing_styles.get_default_hand_landmarks_style(),
                    drawing_styles.get_default_hand_connections_style()
                )

        cv.imshow("Hand Tracking", frame)

        #Press the "q" key to escape
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

#Release the camera
cap.release()
cv.destroyAllWindows()