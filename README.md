# AAE4011 Assignment 1 — Q3: ROS-Based Vehicle Detection from Rosbag

> **Student Name:** [WANG Xuanting] | **Student ID:** [23100379d] | **Date:** [16,3,2026]

---

## 1. Overview

*This project implements a real-time vehicle detection pipeline using the Robot Operating System (ROS). It subscribes to a compressed image stream from a pre-recorded UAV rosbag file and utilizes a deep learning model to detect and draw bounding boxes around vehicles in real time.*

## 2. Detection Method *(Q3.1 — 2 marks)*

*For this task, I selected YOLOv8 (specifically the YOLOv8 Nano model, yolov8n.pt).
I chose this architecture because the YOLO (You Only Look Once) family is highly optimized for real-time object detection. The Nano variant is extremely lightweight, striking an excellent balance between detection accuracy and inference speed. This makes it particularly suitable for processing high-framerate ROS image streams and for future deployment on resource-constrained UAV edge computers. The model is pre-trained on the COCO dataset, which natively includes vehicle classes (cars, buses, trucks, and motorcycles).*

## 3. Repository Structure

*catkin_ws/src/vehicle_detector/
├── CMakeLists.txt
├── package.xml
├── launch/
│   └── detector.launch          # Launch file to start the node
└── scripts/
    └── detector_node.py         # Main Python script containing the YOLOv8 logic*

## 4. Prerequisites

To run this package, the following software and libraries are required:

OS: Ubuntu 20.04 LTS;
Middleware: ROS Noetic;
Python: Python 3.8+;
Key Libraries: rospy, sensor_msgs, ultralytics (for YOLOv8), opencv-python (cv2), numpy

## 5. How to Run *(Q3.1 — 2 marks)*

*Please follow these step-by-step instructions to execute the pipeline:*

1. Clone/Setup the repository:
   Place the vehicle_detector package inside the src folder of your catkin workspace (e.g., ~/catkin_ws/src/).
2. Install dependencies:pip install ultralytics opencv-python numpy
3. Build the ROS package:cd ~/catkin_ws
                         catkin_make
                         source devel/setup.bash
4.  Launch the pipeline:
    Open a terminal and start the ROS core and the detection node:roscore &
                                                                  roslaunch vehicle_detector detector.launch
5.. Place and play the rosbag file:
    Open a new terminal, navigate to the directory where your rosbag is stored, and play it:cd [Path_To_Your_Bag_Directory]
                                                                                            rosbag play 2026-02-02-17-57-27.bag



## 6. Sample Results

*Include:*
Image Extraction Summary:
Topic Name: /hikcamera/image_2/compressed;
Message Type: sensor_msgs/CompressedImage;
Resolution: [2200*1740];
Detection Results:
The YOLOv8n model successfully identified vehicles with high confidence scores (typically >0.60) in real-time without noticeable latency.

## 7. Video Demonstration *(Q3.2 — 5 marks)*

**Video Link:** [YouTube (Unlisted)](https://youtu.be/q4Tdpo4_-04?feature=shared)


## 8. Reflection & Critical Analysis *(Q3.3 — 8 marks, 300–500 words)*

### (a) What Did You Learn? *(2 marks)*

*During this assignment, I gained practical experience in integrating modern deep learning frameworks with ROS middleware. Specifically, I learned how to efficiently handle sensor_msgs/CompressedImage topics. Instead of relying on standard cv_bridge (which can sometimes cause Python 3 compatibility issues in ROS Noetic), I learned to use numpy.frombuffer and cv2.imdecode to convert compressed byte arrays into OpenCV BGR formats. This method is highly bandwidth-efficient. Additionally, I learned how to filter specific class IDs in YOLO to ensure the system only detects vehicles rather than irrelevant objects.*

### (b) How Did You Use AI Tools? *(2 marks)*

*I utilized AI assistants (such as ChatGPT) to accelerate the development process. I used AI to generate the boilerplate ROS Subscriber code and to troubleshoot terminal errors, such as path resolution issues when the rosbag play command failed to locate the bag file. The main benefit was a significant reduction in debugging time and faster prototyping. However, a limitation I encountered was that AI sometimes provided outdated syntax (e.g., YOLOv5 code instead of YOLOv8) or hallucinated incorrect ROS topic names, requiring me to manually review and adjust the code to fit the exact assignment specifications.*

### (c) How to Improve Accuracy? *(2 marks)*

*1. Fine-tuning on Aerial Datasets: The pre-trained YOLOv8 model is trained on the COCO dataset, which consists mostly of ground-level perspectives. Since this task involves UAV footage, fine-tuning the model on drone-specific datasets (like VisDrone) would drastically improve the detection of small vehicles from a top-down perspective.
2. Image Enhancement Pre-processing: Applying techniques like Histogram Equalization or dynamic contrast adjustment before feeding the image to the model would help the system maintain high accuracy in poor lighting conditions or when vehicles are obscured by shadows.*

### (d) Real-World Challenges *(2 marks)*

*1. SWaP (Size, Weight, and Power) Constraints: Deploying this on an actual drone means running the code on a lightweight companion computer (e.g., Raspberry Pi). These edge devices have limited computational power, which can cause severe latency, dropping the detection frame rate and delaying critical autonomous flight decisions.
2. Vibration and Motion Blur: Drones experience high-frequency vibrations from rotors and rapid movements. This introduces severe motion blur into the camera feed, which can degrade image features, causing the bounding boxes to jitter or the model to lose track of the vehicles entirely. Hardware gimbals and faster shutter speeds are required to mitigate this.*

## 9. References

*1. Ultralytics. (2026). YOLOv8 Documentation. Retrieved from https://docs.ultralytics.com/
 2. ROS Wiki. (2026). rospy - ROS Wiki. Retrieved from http://wiki.ros.org/rospy
 3. OpenCV. (2026). OpenCV-Python Tutorials. Retrieved from https://docs.opencv.org/*
