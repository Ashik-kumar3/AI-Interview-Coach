class LiveAnalysis:

    def __init__(self):

        self.eye_contact = 0
        self.head_stability = 0
        self.posture = 0
        self.confidence = 0

        self.previous_nose_x = None
        self.previous_nose_y = None


analysis = LiveAnalysis()