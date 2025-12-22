# Lock_In_Device
Real-time eye tracking using Raspberry Pi and MediaPipe

# What the Lock_In_Device does
Eyes open:
The system displays “Locked In”, indicating normal operation.
![image alt]([image_url](https://github.com/jtranislockedin-rgb/Lock_In_Device/blob/main/Locked-In.jpg?raw=true))

Eyes closed:
A 5-second countdown begins and is displayed on the screen.
![image alt]([image_url](https://github.com/jtranislockedin-rgb/Lock_In_Device/blob/main/Countdown.jpg?raw=true))

Eyes reopen during countdown:
The countdown is immediately canceled, and the display resets to “Locked In.”

Countdown reaches zero:
A predefined output is triggered.
In my implementation, this output activates a relay module, which in turn activates an external device.
![image alt]([image_url](https://github.com/jtranislockedin-rgb/Lock_In_Device/blob/main/Geeked.jpg?raw=true))

# How It Works
- Camera captures real-time video input
- MediaPipe detects facial landmarks and eye state
- Eye-open/eye-closed state is continuously evaluated
- A timer-based logic controls display output and relay activation

# Hardware used
Raspberry Pi 4 or 5 (Powerful enough to run MediaPipe libraries)
Pi Camera
Output device of choice when eyes are closed

# Software Used
- Python 3
- MediaPipe
- OpenCV
- Raspberry Pi OS

# Disclaimer
This project is for educational and experimental purposes only.
The author is not responsible for misuse or unsafe implementations.

