class DJActionNode: 
    def __init__(self):
        self.volume = 50 
        self.is_playing = True
        self.turntable_position = 0
        self.last_action = "No action"
    
    def execute(self, gesture):
        if gesture == "point":
            self.volume = min(100, self.volume + 5)
            self.last_action = f"Volume up -> {self.volume}"
            return self.last_action
        
        elif gesture == "pinch":
    
    