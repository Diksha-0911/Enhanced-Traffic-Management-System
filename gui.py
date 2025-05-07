
import cv2
import numpy as np

class TrafficGUI:
    def __init__(self):
        self.window_name = "Advanced Traffic Management System"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        self.display_width = 1280
        self.display_height = 720
        self.preview_size = (300, 200)
        self.light_positions = [(200, 400), (500, 400), (800, 400), (1100, 400)]

    def draw_traffic_light(self, frame, position, state, timer):
        """Draws a 3-light traffic signal at given position based on lane state."""
        x, y = position
        light_radius = 15
        gap = 10

        # Draw housing (rectangle background)
        cv2.rectangle(frame, (x - 25, y - 50), (x + 25, y + 70), (50, 50, 50), -1)

        # Light Colors
        colors = {
            "red": (0, 0, 255),
            "yellow": (0, 255, 255),
            "green": (0, 255, 0),
            "off": (30, 30, 30)  # Dimmed color for OFF lights
        }

        # Set light status
        if state == "green":
            lights = ["off", "off", "green"]
        elif state == "yellow":
            lights = ["off", "yellow", "off"]
        else:  # red
            lights = ["red", "off", "off"]

        # Draw lights (top → bottom: red, yellow, green)
        for i, color_key in enumerate(lights):
            cy = y - 30 + i * (2 * light_radius + gap)
            cv2.circle(frame, (x, cy), light_radius, colors[color_key], -1)

        # Draw timer below lights (only for green and yellow)
        if state in ["green", "yellow"]:
            cv2.putText(frame, f"{timer}s", (x - 20, y + 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    def display(self, frames, light_states, timer, ambulance_lane, input_types):
        main_display = np.zeros((self.display_height, self.display_width, 3), dtype=np.uint8)

        # Draw input previews
        preview_positions = [(10, 10), (320, 10), (630, 10), (940, 10)]
        for i, (frame, pos) in enumerate(zip(frames, preview_positions)):
            if frame is not None:
                resized = cv2.resize(frame, self.preview_size)
                x, y = pos
                main_display[y:y + self.preview_size[1], x:x + self.preview_size[0]] = resized
                label = "Image" if input_types[i] else "Video"
                cv2.putText(main_display, f"Lane {i + 1} ({label})", (x + 5, y + 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        # Draw traffic lights for each lane
        for i, (x, y) in enumerate(self.light_positions):
            state = light_states[i]
            self.draw_traffic_light(main_display, (x, y), state, timer if state in ["green", "yellow"] else 0)

        # Emergency message if ambulance detected
        if ambulance_lane != -1:
            cv2.putText(main_display, f"🚑 AMBULANCE IN LANE {ambulance_lane + 1} - PRIORITY PASS 🚑",
                        (200, 680), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

        cv2.imshow(self.window_name, main_display)
        cv2.waitKey(1)

