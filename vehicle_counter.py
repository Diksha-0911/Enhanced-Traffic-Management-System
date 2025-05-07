
import cv2
import numpy as np
from ultralytics import YOLO

class VehicleCounter:
    def __init__(self, is_static_image=False):
        self.is_static_image = is_static_image
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50)
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        self.static_model = YOLO("yolov8n.pt") if is_static_image else None

    def count_vehicles(self, frame):
        if self.is_static_image:
            return self._count_static(frame)
        else:
            return self._count_video(frame)

    def _count_video(self, frame):
        fg_mask = self.bg_subtractor.apply(frame)
        _, thresh = cv2.threshold(fg_mask, 250, 255, cv2.THRESH_BINARY)
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, self.kernel, iterations=2)
        contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return sum(1 for cnt in contours if cv2.contourArea(cnt) > 500)

    # def _count_static(self, frame):
    #     results = self.static_model(frame, verbose=False)
    #     return sum(1 for r in results[0] if r.names[int(r.boxes.cls)] in ['car', 'truck', 'bus'])

    def _count_static(self, frame):
        results = self.static_model(frame, verbose=False)
        boxes = results[0].boxes
        names = results[0].names
        count = 0
        for box in boxes:
            if names[int(box.cls)] in ['car', 'truck', 'bus']:
                count += 1
        return count
