
# AI-Powered Surveillance System

An intelligent surveillance system built using **YOLO**, **DeepSORT**, and custom rule-based logic to monitor CCTV feeds in real time. The system detects, tracks, and analyzes human activity to identify potential security threats and generate alerts.

## Features

* Real-time object detection using YOLO
* Multi-object tracking with DeepSORT
* Intrusion detection in restricted zones
* Loitering detection
* Unauthorized access monitoring
* Person tracking across frames
* Real-time alert generation
* Support for CCTV cameras and video files
* Scalable architecture for real-world deployment

## Tech Stack

* Python
* OpenCV
* YOLOv8
* DeepSORT
* NumPy
* PyTorch

## Project Workflow

1. Capture video stream from CCTV or video source
2. Detect objects using YOLO
3. Track detected objects using DeepSORT
4. Apply rule-based event analysis
5. Generate alerts for suspicious activities
6. Display processed video feed with annotations

## Security Events Detected

* Intrusion into restricted areas
* Loitering for extended periods
* Unauthorized entry
* Suspicious movement patterns
* Presence detection in monitored zones

## Installation

```bash
git clone https://github.com/yourusername/your-repository.git
cd your-repository

pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

For webcam:

```bash
python main.py --source 0
```

For video file:

```bash
python main.py --source video.mp4
```

## Future Improvements

* Email and SMS notifications
* Telegram and WhatsApp alerts
* Face recognition integration
* Weapon detection
* Vehicle detection and tracking
* Crowd monitoring
* Cloud deployment
* Web dashboard
* Multi-camera support
* Analytics and reporting system

## Applications

* Smart CCTV Monitoring
* Industrial Security
* Warehouse Surveillance
* Office Security
* Campus Monitoring
* Public Safety Systems

## Learning Outcomes

This project demonstrates practical implementation of:

* Computer Vision
* Object Detection
* Multi-Object Tracking
* Real-Time Video Processing
* Event-Driven Security Systems
* AI System Design

## License

This project is licensed under the MIT License.
