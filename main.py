import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # suppress TensorFlow/MediaPipe logs

import cv2
import mediapipe as mp
from picamera2 import Picamera2
from time import sleep, time
import RPi.GPIO as GPIO   # <-- GPIO import

# -------------------------
# GPIO SETUP
# -------------------------
RELAY_PIN = 17   # CHANGE THIS to the pin you're using
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)

# prevent repeated triggering
geeked_triggered = False

# -------------------------
# Configuration
# -------------------------
EAR_THRESHOLD = 0.28
COUNTDOWN_SECONDS = 5

# -------------------------
# Initialize Picamera2
# -------------------------
picam2 = Picamera2()
video_config = picam2.create_preview_configuration(
    main={"format": "XRGB8888", "size": (320, 240)}
)
picam2.configure(video_config)
picam2.start()
sleep(1)

# -------------------------
# Initialize Mediapipe Face Mesh
# -------------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# -------------------------
# Eye Aspect Ratio
# -------------------------
def eye_aspect_ratio(landmarks, left=True):
    if left:
        top = landmarks[159]
        bottom = landmarks[145]
        left_pt = landmarks[33]
        right_pt = landmarks[133]
    else:
        top = landmarks[386]
        bottom = landmarks[374]
        left_pt = landmarks[362]
        right_pt = landmarks[263]

    v_dist = abs(top.y - bottom.y)
    h_dist = ((left_pt.x - right_pt.x)**2 + (left_pt.y - right_pt.y)**2)**0.5
    if h_dist == 0:
        return 0
    return v_dist / h_dist

# -------------------------
# Compute iris center
# -------------------------
def iris_center(iris_landmarks, w, h):
    x = int(sum([lm.x for lm in iris_landmarks]) / 4 * w)
    y = int(sum([lm.y for lm in iris_landmarks]) / 4 * h)
    return x, y

# -------------------------
# Main loop
# -------------------------
cv2.namedWindow("Iris Tracker", cv2.WINDOW_NORMAL)

eyes_closed_time = None

while True:
    frame = picam2.capture_array()
    frame = cv2.flip(frame, 0)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    status_text = "No face"
    status_color = (0, 165, 255)

    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = face_landmarks.landmark
            h, w, _ = frame.shape

            left_EAR = eye_aspect_ratio(landmarks, left=True)
            right_EAR = eye_aspect_ratio(landmarks, left=False)

            if left_EAR < EAR_THRESHOLD and right_EAR < EAR_THRESHOLD:
                if eyes_closed_time is None:
                    eyes_closed_time = time()
                elapsed = time() - eyes_closed_time
                remaining = max(0, COUNTDOWN_SECONDS - int(elapsed))

                if elapsed >= COUNTDOWN_SECONDS:
                    status_text = "GEEKED"
                    status_color = (0, 0, 255)

                    # -------------------------
                    # GEEKED ACTION: Trigger Relay
                    # -------------------------
                    if not geeked_triggered:
                        geeked_triggered = True
                        GPIO.output(RELAY_PIN, GPIO.HIGH)  # turn ON relay
                        sleep(1)                           # keep ON 1 second
                        GPIO.output(RELAY_PIN, GPIO.LOW)   # turn OFF relay

                else:
                    status_text = f"{remaining} sec..."
                    status_color = (0, 165, 255)

            else:
                eyes_closed_time = None
                status_text = "Locked In"
                status_color = (0, 255, 0)
                geeked_triggered = False   # reset when eyes open

            # Draw points
            for idx in [33, 133, 159, 145, 362, 263, 386, 374]:
                lm = landmarks[idx]
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 2, (0, 255, 0), -1)

            left_iris_landmarks = [landmarks[i] for i in [474, 475, 476, 477]]
            right_iris_landmarks = [landmarks[i] for i in [469, 470, 471, 472]]
            lx, ly = iris_center(left_iris_landmarks, w, h)
            rx, ry = iris_center(right_iris_landmarks, w, h)
            cv2.circle(frame, (lx, ly), 5, (255, 0, 0), 2)
            cv2.circle(frame, (rx, ry), 5, (255, 0, 0), 2)

    # Overlay
    overlay = frame.copy()
    alpha = 0.6
    cv2.rectangle(overlay, (5, 5), (300, 45), (0, 0, 0), -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    cv2.putText(frame, status_text, (10, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2, cv2.LINE_AA)

    frame_resized = cv2.resize(frame, (800, 600))
    cv2.imshow("Iris Tracker", frame_resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
face_mesh.close()
picam2.stop()
GPIO.cleanup()

