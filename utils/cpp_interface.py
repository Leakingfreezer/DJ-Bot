"""
Purpose: Connects the interface between python and C++ logic
Python --> sends data --> C++ --> returns decision --> Python continues
"""

import subprocess
import os


def classify_gesture_from_cpp(landmarks):
    #Finding the exact exe path
    exe_path = os.path.join("cpp logic", "gesture_classifier.exe")

    #Converting landmarks to numbers --> x y
    input_data = []

    for lm in landmarks:
        input_data.append(str(lm.x))
        input_data.append(str(lm.y))

    #Send data and turn into one string
    input_string = " ".join(input_data)

    #Running the C++ Program
    result = subprocess.run(
        [exe_path],
        input=input_string,
        capture_output=True,
        text=True
    )

    #Check for errors, if C++ crashes --> show error
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    
    #Finally, return the gesture label
    return result.stdout.strip()
