# Lock_In_Device
Real-time eye tracking using Raspberry Pi and MediaPipe

# The Problem
Research consistently shows that drowsy or fatigued driving is a major yet often overlooked danger on the road. Nearly 9% of all car accidents—amounting to hundreds of thousands of crashes each year—are linked to driver fatigue, resulting in over 6,000 deaths annually. What makes these numbers especially alarming is that, unlike many other causes of traffic accidents, drowsy driving is entirely preventable.

# Introducing the Lock_In_Device
![Locked In device](https://github.com/jtranislockedin-rgb/Lock_In_Device/blob/main/images/Locked-In%20device.jpg?raw=true)

# How It Works
- Camera captures real-time video input
- MediaPipe detects facial landmarks and eye state
- Eye-open/eye-closed state is continuously evaluated
- A timer-based logic controls display output and relay activation

# Lock_In_Device display states
Eyes open:
The system displays “Locked In”, indicating normal operation.
![Locked In display](https://github.com/jtranislockedin-rgb/Lock_In_Device/blob/main/images/Locked-In.jpg?raw=true)

Eyes closed:
A 5-second countdown begins and is displayed on the screen.
![Countdown display](https://github.com/jtranislockedin-rgb/Lock_In_Device/blob/main/images/Countdown.jpg?raw=true)

Eyes reopen during countdown:
The countdown is immediately canceled, and the display resets to “Locked In.”

Countdown reaches zero:
A predefined output is triggered.
In my implementation, this output activates a relay module, which in turn activates an external device.
![Relay activation](https://github.com/jtranislockedin-rgb/Lock_In_Device/blob/main/images/Geeked.jpg?raw=true)

# Hardware used
- Raspberry Pi 4 or 5 (Powerful enough to run MediaPipe libraries)
- Pi Camera
- Output device of choice when eyes are closed

# Software Used
- Python 3
- MediaPipe
- OpenCV
- Raspberry Pi OS

# Disclaimer
This project is for educational and experimental purposes only.
The author is not responsible for misuse or unsafe implementations.

