

# 🚦 Advanced Traffic Management System with Ambulance Detection

This project implements an AI-powered **Smart Traffic Management System** capable of:

* Dynamically adjusting signal timings based on real-time vehicle density.
* Prioritizing **ambulances** using YOLOv8 object detection.
* Providing a **graphical interface** for real-time visualization of traffic flow and light status.

> Designed for urban traffic optimization and emergency vehicle prioritization using computer vision.

---

## 📁 Project Structure

```
├── main.py                      # Main driver script
├── gui.py                       # GUI for real-time traffic display
├── ambulance_detector.py        # YOLOv8-based ambulance detector
├── traffic_controller.py        # Core logic to manage traffic light timings
├── vehicle_counter.py           # Vehicle counting logic (assumed)
├── models/
│   └── ambulance_yolov8.pt      # Pre-trained YOLOv8 model for ambulance detection
├── input/
│   └── lane-1.jpg               # Sample input images/videos for each lane
│   └── lane-2.jpg
│   └── ...
├── README.md                    # Project documentation
```

---

## 🛠️ Features

* 🚗 **Vehicle Counting**: Uses classical methods (like contour detection) for estimating traffic density per lane.
* 🚨 **Ambulance Detection**: Automatically detects ambulances using a custom-trained YOLOv8 model and prioritizes the lane.
* ⏱️ **Adaptive Signal Timing**: Dynamically allocates green signal duration based on real-time vehicle density and emergency detection.
* 🖼️ **Graphical Interface**: Built with OpenCV to visualize lane previews, traffic signals, timers, and emergency alerts.

---

## 📦 Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

### Requirements

* `ultralytics` (for YOLOv8)
* `opencv-python`
* `numpy`

You can create a `requirements.txt` like this:

```txt
ultralytics
opencv-python
numpy
```

---

## 🚀 How to Run

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/traffic-management-system.git
cd traffic-management-system
```

2. **Download YOLOv8 Ambulance Model**
   Place your custom-trained YOLOv8 model for ambulance detection in the `models/` folder.

   ```
   models/ambulance_yolov8.pt
   ```

3. **Provide Input Sources**
   Update `INPUT_SOURCES` in `main.py` to point to your test images, videos, or webcam indices.

4. **Run the System**

```bash
python main.py
```

> Press `ESC` to stop the system gracefully.

---

## 📸 Sample GUI Output

* Live lane previews.
* Colored traffic light simulation.
* Timer under active green/yellow lights.
* Emergency message display for ambulance detection.

---

