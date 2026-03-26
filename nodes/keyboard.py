import pygame 
import time 

class KeyboardNode: 
    def __init__(self):
        self.key_map = {
            pygame.K_1: "kick",
            pygame.K_2: "snare",
            pygame.K_3: "hihat",
            pygame.K_4: "clap",
            pygame.K_5: "pause_track",
            pygame.K_6: "play_track",
            pygame.K_7: "echo", 
            pygame.K_8: "filter"
            
        }
        self.key_down_times = {}

        def process_event(self, event):
            if event.type == pygame.KEYDOWN: 
                if event.key not in self.key_down_times:
                    self.key_down_times[event.key] = time.time()

            elif event.type == pygame.KEYUP:
                if event.key in self.key_down_times:
                    press_duration = time.time() - self.key_down_times[event.key]
                    del self.key_down_times[event.key]

                    action = self.key_map.get(event.key)
                    if action:
                        return {
                            "key": pygame.key.name(event.key),
                            "action": action,
                            "duration": round(press_duration, 3),
                            "intensity": self.classify_intensity(press_duration),
                        }
            return None

