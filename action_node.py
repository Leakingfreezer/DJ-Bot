import math
import time


class DJActionNode:
    def __init__(self):
        self.volume = 50
        self.waveform_scale = 1.0
        self.turntable_position = 0.0
        self.is_playing = False
        self.last_action = "No action"

        self.volume_slider_zone = {
            "x1": 0.05,
            "x2": 0.15,
            "y1": 0.20,
            "y2": 0.85
        }

        self.waveform_zone = {
            "x1": 0.25,
            "x2": 0.85,
            "y1": 0.35,
            "y2": 0.60
        }

        self.turntable_zone = {
            "x1": 0.65,
            "x2": 0.95,
            "y1": 0.15,
            "y2": 0.55
        }

        self.hover_target = None
        self.last_pinch_distance = None
        self.last_index_x = None

        self.fist_start_time = None
        self.fist_triggered = False

    def execute(self, gesture, hand_data):
        if not hand_data["hand_detected"]:
            self.hover_target = None
            self.last_pinch_distance = None
            self.last_index_x = None
            self.fist_start_time = None
            self.fist_triggered = False
            self.last_action = "No hand detected"
            return self.last_action

        index_x = hand_data["index_tip_x"]
        index_y = hand_data["index_tip_y"]
        thumb_x = hand_data["thumb_tip_x"]
        thumb_y = hand_data["thumb_tip_y"]

        self.hover_target = self.get_active_target(index_x, index_y)

        if gesture == "point":
            self.fist_start_time = None
            self.fist_triggered = False

            if self.hover_target == "volume_slider":
                self.last_action = f"Point hovering volume slider at ({index_x:.2f}, {index_y:.2f})"
            elif self.hover_target == "waveform":
                self.last_action = f"Point hovering waveform at ({index_x:.2f}, {index_y:.2f})"
            elif self.hover_target == "turntable":
                self.last_action = f"Point hovering turntable at ({index_x:.2f}, {index_y:.2f})"
            else:
                self.last_action = f"Point detected at ({index_x:.2f}, {index_y:.2f})"

            self.last_pinch_distance = None
            self.last_index_x = None
            return self.last_action

        elif gesture == "fist":
            self.last_pinch_distance = None
            self.last_index_x = None

            if self.fist_start_time is None:
                self.fist_start_time = time.time()
                self.fist_triggered = False
                self.last_action = "Fist detected, hold to pause/unpause"
                return self.last_action

            held_time = time.time() - self.fist_start_time

            if held_time >= 2 and not self.fist_triggered:
                self.is_playing = not self.is_playing
                self.fist_triggered = True

                if self.is_playing:
                    self.last_action = "Fist held 4s -> playing"
                else:
                    self.last_action = "Fist held 4s -> paused"
            else:
                self.last_action = f"Holding fist... {held_time:.1f}s"

            return self.last_action

        elif gesture == "pinch":
            self.fist_start_time = None
            self.fist_triggered = False

            pinch_distance = self.get_distance(thumb_x, thumb_y, index_x, index_y)

            if self.hover_target == "waveform":
                self.update_waveform_from_pinch(pinch_distance)
                self.last_action = f"Pinch scaling waveform -> {self.waveform_scale:.2f}"

            elif self.hover_target == "turntable":
                self.update_turntable_from_x(index_x)
                self.last_action = f"Pinch nudging turntable -> {self.turntable_position:.2f}"

            elif self.hover_target == "volume_slider":
                self.update_volume_from_y(index_y)
                self.last_action = f"Pinch adjusting volume -> {self.volume}"

            else:
                self.last_action = "Pinch detected"

            self.last_pinch_distance = pinch_distance
            return self.last_action

        elif gesture == "two_finger":
            self.fist_start_time = None
            self.fist_triggered = False
            self.last_pinch_distance = None
            self.last_index_x = None
            self.last_action = "Two-finger gesture detected"
            return self.last_action

        else:
            self.fist_start_time = None
            self.fist_triggered = False
            self.last_pinch_distance = None
            self.last_index_x = None
            self.last_action = "No action"
            return self.last_action

    def get_active_target(self, x, y):
        if self.is_inside_zone(x, y, self.volume_slider_zone):
            return "volume_slider"
        if self.is_inside_zone(x, y, self.waveform_zone):
            return "waveform"
        if self.is_inside_zone(x, y, self.turntable_zone):
            return "turntable"
        return None

    def is_inside_zone(self, x, y, zone):
        return zone["x1"] <= x <= zone["x2"] and zone["y1"] <= y <= zone["y2"]

    def update_volume_from_y(self, index_y):
        mapped_volume = int((1.0 - index_y) * 100)
        self.volume = max(0, min(100, mapped_volume))

    def update_turntable_from_x(self, index_x):
        if self.last_index_x is not None:
            delta_x = index_x - self.last_index_x
            self.turntable_position += delta_x * 10
        self.last_index_x = index_x

    def update_waveform_from_pinch(self, pinch_distance):
        if self.last_pinch_distance is not None:
            if pinch_distance > self.last_pinch_distance:
                self.waveform_scale = min(2.0, self.waveform_scale + 0.03)
            elif pinch_distance < self.last_pinch_distance:
                self.waveform_scale = max(0.5, self.waveform_scale - 0.03)

    def get_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)