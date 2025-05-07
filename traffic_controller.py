
class TrafficController:
    def __init__(self, lanes=4):
        # Timing parameters (seconds)
        self.green_duration = 10
        self.yellow_duration = 3
        self.min_green = 5
        self.max_green = 15

        # State tracking
        self.lanes = lanes
        self.current_green = 0
        self.phase = "green"  # green → yellow → red
        self.timer = self.green_duration
        self.emergency_mode = False
        self.ambulance_lane = -1

    def calculate_green_times(self, vehicle_counts, ambulance_present):
        if any(ambulance_present):
            self.emergency_mode = True
            self.ambulance_lane = ambulance_present.index(True)
            self.current_green = self.ambulance_lane
            self.phase = "green"
            self.timer = self.max_green
            return

        if self.emergency_mode:
            self.emergency_mode = False
            self.phase = "yellow"
            self.timer = self.yellow_duration

        # Phase transitions
        if self.phase == "green":
            if self.timer <= 0:
                self.phase = "yellow"
                self.timer = self.yellow_duration
        elif self.phase == "yellow":
            if self.timer <= 0:
                self.current_green = (self.current_green + 1) % self.lanes
                self.phase = "green"
                self.timer = self.calculate_green_duration(vehicle_counts)
        self.timer -= 1

    def calculate_green_duration(self, counts):
        total = sum(counts)
        if total == 0:
            return self.green_duration
        return min(self.max_green,
                   max(self.min_green,
                       int((counts[self.current_green] / total) * self.green_duration * 2)))

    def get_light_states(self):
        states = []
        for i in range(self.lanes):
            if i == self.current_green:
                states.append(self.phase)
            else:
                states.append("red")
        return states