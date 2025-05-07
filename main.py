
import cv2
import time
import os
import numpy as np
from itertools import cycle
from traffic_controller import TrafficController
from gui import TrafficGUI
from ambulance_detector import AmbulanceDetector
from vehicle_counter import VehicleCounter


class TrafficSystem:
    def __init__(self, input_sources):
        self.input_sources = input_sources
        self.detectors = [AmbulanceDetector() for _ in range(4)]
        self.counters = [VehicleCounter() for _ in range(4)]
        self.controller = TrafficController()
        self.gui = TrafficGUI()

        # Initialize input handlers
        self.frame_generators = []
        self.video_caps = []
        self.input_types = []  # True for image, False for video
        self._initialize_sources()

    def _initialize_sources(self):
        """Create frame generators for all input sources"""
        for src in self.input_sources:
            # Handle image inputs
            if isinstance(src, str) and os.path.isfile(src):
                if src.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img = cv2.imread(src)
                    if img is not None:
                        self.frame_generators.append(cycle([img]))
                        self.input_types.append(True)
                        continue

                # Handle video files
                cap = cv2.VideoCapture(src)
                if cap.isOpened():
                    self.video_caps.append(cap)
                    self.frame_generators.append(self._video_generator(cap))
                    self.input_types.append(False)
                else:
                    raise ValueError(f"Could not open file: {src}")

            # Handle webcam inputs
            elif isinstance(src, int):
                cap = cv2.VideoCapture(src)
                if cap.isOpened():
                    self.video_caps.append(cap)
                    self.frame_generators.append(self._video_generator(cap))
                    self.input_types.append(False)
                else:
                    raise ValueError(f"Could not open webcam index {src}")

            else:
                raise ValueError(f"Invalid input source: {src}")

    def _video_generator(self, cap):
        """Generator that loops video sources indefinitely"""
        while True:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            yield frame

    def run(self):
        try:
            while True:
                frames = []
                vehicle_counts = []
                ambulance_present = [False] * 4

                # Process all input sources
                for i, gen in enumerate(self.frame_generators):
                    frame = next(gen)

                    # Convert grayscale to color if needed
                    if len(frame.shape) == 2:
                        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

                    frames.append(frame)

                    # Vehicle counting
                    vehicle_count = self.counters[i].count_vehicles(frame)
                    vehicle_counts.append(vehicle_count)

                    # Ambulance detection
                    if self.detectors[i].detect_ambulance(frame):
                        ambulance_present[i] = True

                # Update traffic controller
                self.controller.calculate_green_times(vehicle_counts, ambulance_present)

                # Get light states
                light_states = self.controller.get_light_states()

                # Update GUI
                self.gui.display(frames, light_states, self.controller.timer, self.controller.ambulance_lane,
                                 self.input_types)

                # Break loop if ESC is pressed
                if cv2.waitKey(1) & 0xFF == 27:
                    break

        finally:
            # Release video captures and destroy windows
            for cap in self.video_caps:
                cap.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    # ========== CONFIGURATION ========== #
    INPUT_SOURCES = [
        "input/lane-1 (1).jpg",  # Test image
        "input/lane-2.jpg",  # Test video
        "input/lane-3 (1).jpg",  # Webcam
        "input/lane-4 (1).jpg"  # Test image

    ]

    # ======= VERIFICATION CHECKS ======= #
    for src in INPUT_SOURCES:
        if isinstance(src, str) and not os.path.exists(src):
            raise FileNotFoundError(f"Input source not found: {src}")

    # ========== START SYSTEM =========== #
    system = TrafficSystem(INPUT_SOURCES)
    system.run()