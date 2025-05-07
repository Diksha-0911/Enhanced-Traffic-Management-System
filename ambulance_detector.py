
from ultralytics import YOLO
import os


class AmbulanceDetector:
    def __init__(self, model_path="models/ambulance_yolov8.pt", conf_threshold=0.4):
        # Verify model path exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Ambulance model not found at: {os.path.abspath(model_path)}")

        self.model = YOLO(model_path)
        self.class_name = 'ambulance'
        self.conf_threshold = conf_threshold

    def detect_ambulance(self, frame):
        results = self.model(frame, verbose=False, conf=self.conf_threshold)
        for result in results:
            for box in result.boxes:
                if result.names[int(box.cls)] == self.class_name:
                    return True
        return False