"""
Purpose: Connects the interface between python and C++ logic
Python --> sends data --> C++ --> returns decision --> Python continues
"""

import os
import subprocess


def classify_gesture_from_cpp(landmarks):
    exe_path = os.path.join("cpp logic", "gesture_classifier.exe")

    input_data = []
    for lm in landmarks:
        input_data.append(str(lm.x))
        input_data.append(str(lm.y))

    input_string = " ".join(input_data)

    result = subprocess.run(
        [exe_path],
        input=input_string,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return result.stdout.strip()