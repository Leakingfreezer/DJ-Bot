#include <iostream>
#include <vector>
#include <string>
#include <cmath>

/**
 * Takes the raw data from mediapide node and intrepets it to be classified actions.
 * Recieves landmark values --> check rules --> outputs a gesture label to run to the action.py
 * Returns: Clean numbers for the action_node
 * Important functions/logic explained:
 * isFingerUp function takes the landmarks detected and checks if visibly the finger is up by comparing
 * the tip position to the bottom join. MediaPipe data works
 * by taging each point on the finger as numbers
 */

//Initializing/storing position variables
struct Landmark {
    float x;
    float y;
};

class GestureClassifier {
public: 
    std::string classify(const std::vector<Landmark>& landmarks) {
        if (landmarks.size() < 21) {
            return "none";
        }

        bool indexUp = isFingerUp(landmarks[8], landmarks[6]);
        bool middleUp = isFingerUp(landmarks[12], landmarks[10]);
        bool ringUp = isFingerUp(landmarks[16], landmarks[14]);
        bool pinkyUp = isFingerUp(landmarks[20], landmarks[18]);

        bool pinching = isPinching(landmarks[4], landmarks[8]);

        if (pinching) {
            return "pinch";
        }

        if (indexUp && !middleUp && !ringUp && !pinkyUp) {
            return "point";
        }

        if (indexUp && middleUp && !ringUp && !pinkyUp) {
            return "two_finger";
        }

        if (!indexUp && !middleUp && !ringUp && !pinkyUp) {
            return "fist";
        }

        return "none";

    }

private:
    bool isFingerUp(const Landmark& tip, const Landmark& pip) {
        return tip.y < pip.y;
    }

    bool isPinching(const Landmark& thumbTip, const Landmark& indexTip) {
        float dx = thumbTip.x - indexTip.x;
        float dy = thumbTip.y - indexTip.y;
        float distance = std::sqrt(dx * dx + dy * dy);

        return distance < 0.05f;
    }
};

int main() { 
    std::vector<Landmark> landmarks(21); 

    //Looping through all landmarks to check if they are identified
    for (int i = 0; i<21; i++) {
        std::cin >> landmarks[i].x >> landmarks[i].y;
    }

    GestureClassifier classifier;
    std::cout << classifier.classify(landmarks) << std::endl;

    return 0;
}