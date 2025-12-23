import cv2
import mediapipe as mp
import pyautogui
import time
import math

# ================== SETTINGS ==================
pyautogui.FAILSAFE = False

SENSITIVITY = 1.3      # cursor speed
SMOOTHING = 0.8        # stability (higher = smoother)
FPS_DELAY = 0.03       # CPU control (~30 FPS)

CLICK_DISTANCE = 25    # pixels (thumb + index)
PAUSE_DISTANCE = 20    # fist detection
# ==============================================

# Camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

prev_x, prev_y = None, None
cur_x, cur_y = pyautogui.position()
paused = False
click_ready = True

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]

        # Landmarks
        index = hand.landmark[8]
        thumb = hand.landmark[4]
        middle = hand.landmark[12]

        h, w, _ = frame.shape
        ix, iy = int(index.x * w), int(index.y * h)
        tx, ty = int(thumb.x * w), int(thumb.y * h)
        mx, my = int(middle.x * w), int(middle.y * h)

        # Distances
        click_dist = math.hypot(ix - tx, iy - ty)
        pause_dist = math.hypot(ix - mx, iy - my)

        # -------- PAUSE / RESUME (fist) --------
        if pause_dist < PAUSE_DISTANCE:
            paused = not paused
            time.sleep(0.5)  # debounce

        # -------- CURSOR MOVEMENT --------
        if not paused:
            if prev_x is not None:
                dx = (ix - prev_x) * SENSITIVITY
                dy = (iy - prev_y) * SENSITIVITY

                cur_x += dx * SMOOTHING
                cur_y += dy * SMOOTHING

                pyautogui.moveTo(cur_x, cur_y, duration=0)

        # -------- CLICK (thumb + index) --------
        if click_dist < CLICK_DISTANCE and click_ready and not paused:
            pyautogui.click()
            click_ready = False
        if click_dist > CLICK_DISTANCE + 10:
            click_ready = True

        prev_x, prev_y = ix, iy
    else:
        prev_x, prev_y = None, None

    # Status text
    status = "PAUSED" if paused else "ACTIVE"
    cv2.putText(frame, status, (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (0, 0, 255) if paused else (0, 255, 0), 2)

    cv2.imshow("Hand Mouse - ESC to exit", frame)

    time.sleep(FPS_DELAY)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
