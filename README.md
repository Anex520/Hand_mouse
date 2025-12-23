**Hand Mouse — Python Hand-Tracking Cursor Control**



Hand Mouse is a lightweight Python application that allows you to control your computer’s mouse cursor using hand gestures through a webcam. It is designed to work on low-end laptops while automatically becoming more accurate on higher-performance systems.



The project uses MediaPipe Hands for real-time hand landmark detection and converts finger movement into smooth, trackpad-style cursor control without requiring any GPU or machine-learning training.



**Features**



* Real-time hand tracking using a standard webcam



* Stable relative cursor movement (no screen jumping)



* Left-click gesture using thumb and index finger



* Pause / resume control gesture



* Optimized for weak hardware (low CPU usage)



* Works even better on high-performance laptops



* No system modification, runs only when launched



**How It Works**



The cursor moves relative to your finger movement, similar to a laptop touchpad.

This approach provides higher stability and accuracy, especially on older computers, while scaling naturally with better cameras and faster CPUs.



**Requirements**



* Python 3.10 or 3.11



* OpenCV



* MediaPipe



* PyAutoGUI



* Webcam



**Use Cases**



Accessibility and hands-free computer control



Experimental human–computer interaction projects



Learning computer vision and gesture recognition



Fun and educational AI projects



Notes



This project does not replace your system mouse driver and does not run in the background.

Press ESC at any time to exit safely.

