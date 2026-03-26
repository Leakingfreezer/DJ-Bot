import cv2 as cv
import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles

"""
Ultizing the mediapipe library and enabling hand tracking 
Args: 
Returns:
"""

#Initilize the hands model 
hands = mp_hands.Hands(
    static_image_mode = False #processing video frames
    max_num_hands = 2, #maxiumum numbers of hands to detect 
    min_detection_confidence = 0.5 #min confidence threshold for hand detection
)

#Openning the camera
cam = cv.VideoCapture(0)

while cam.isOpened():
    # Read a frame from the camera
    success, frame = cam.read()

    #If the frame is not available, print out error message
    if not success:
        print("Camera Frame not available")
        continue

    #Converting frame from BGR to RGB (required by Mediapipe)
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    #Processing the frame for hand tracking
    hands_detected = hands.process(frame)

    # Convert the frame back from RGB to BGR (required by OpenCV)
    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

    # If hands are detected, draw landmarks and connections on the frame
    if hands_detected.multi_hand_landmarks:
        for hand_landmarks in hands_detected.multi_hand_landmarks:
            drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                drawing_styles.get_default_hand_landmarks_style(),
                drawing_styles.get_default_hand_connections_style(),
            )

    # Display the frame with annotations
    cv.imshow("Show Video", frame)

    # Exit the loop if 'q' key is pressed
    if cv.waitKey(20) & 0xff == ord('q'):
        break

# Release the camera
    cam.release()