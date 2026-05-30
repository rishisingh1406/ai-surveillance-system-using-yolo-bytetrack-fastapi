import cv2
import time
from ultralytics import YOLO

# =====================================
# CONFIG
# =====================================

VIDEO_SOURCE = 0          # Webcam
LOITER_TIME = 15          # Seconds in restricted zone
LONG_STAY_HOURS = 5       # Continuous tracking time

# Restricted Zone
ZONE_X1 = 200
ZONE_Y1 = 100
ZONE_X2 = 500
ZONE_Y2 = 400

# =====================================
# LOAD MODEL
# =====================================

model = YOLO("yolov8n.pt")

# =====================================
# MEMORY
# =====================================

intrusion_alerted = set()
loiter_alerted = set()
long_stay_alerted = set()

# Track zone entry time
zone_entry_time = {}

# Track total time person exists
person_first_seen = {}

# =====================================
# ALARM FUNCTION
# =====================================

def beep(freq=1000, duration=500):
    try:
        import winsound
        winsound.Beep(freq, duration)
    except:
        pass

# =====================================
# VIDEO CAPTURE
# =====================================

cap = cv2.VideoCapture(VIDEO_SOURCE)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # =====================================
    # DRAW RESTRICTED ZONE
    # =====================================

    cv2.rectangle(
        frame,
        (ZONE_X1, ZONE_Y1),
        (ZONE_X2, ZONE_Y2),
        (0, 0, 255),
        2
    )

    cv2.putText(
        frame,
        "RESTRICTED ZONE",
        (ZONE_X1, ZONE_Y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

    # =====================================
    # YOLO + BYTETRACK
    # =====================================

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        verbose=False
    )

    if (
        len(results) > 0
        and results[0].boxes is not None
        and results[0].boxes.id is not None
    ):

        boxes = results[0].boxes

        for box in boxes:

            cls_id = int(box.cls[0])
            track_id = int(box.id[0])

            # PERSON ONLY
            if cls_id != 0:
                continue

            # =====================================
            # LONG STAY TRACKING
            # =====================================

            if track_id not in person_first_seen:
                person_first_seen[track_id] = time.time()

            total_time_seen = (
                time.time()
                - person_first_seen[track_id]
            )

            if (
                total_time_seen >= LONG_STAY_HOURS * 3600
                and track_id not in long_stay_alerted
            ):

                print(
                    f"🚨 LONG STAY ALERT! "
                    f"Person {track_id} present "
                    f"for {LONG_STAY_HOURS} hours"
                )

                long_stay_alerted.add(track_id)

                beep(2000, 1000)

            # =====================================
            # BOUNDING BOX
            # =====================================

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            # =====================================
            # CENTER POINT
            # =====================================

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

           

            # =====================================
            # CHECK RESTRICTED ZONE
            # =====================================

            inside_zone = (
                ZONE_X1 <= center_x <= ZONE_X2
                and
                ZONE_Y1 <= center_y <= ZONE_Y2
            )

            if inside_zone:

                cv2.putText(
                    frame,
                    "INTRUSION ALERT",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

                # =====================================
                # INTRUSION ALERT
                # =====================================

                if track_id not in intrusion_alerted:

                    print(
                        f"🚨 INTRUSION ALERT! "
                        f"Person {track_id} entered zone"
                    )

                    intrusion_alerted.add(track_id)

                    beep(1500, 500)

                # =====================================
                # ZONE TIMER
                # =====================================

                if track_id not in zone_entry_time:
                    zone_entry_time[track_id] = time.time()

                time_in_zone = (
                    time.time()
                    - zone_entry_time[track_id]
                )

                # =====================================
                # LOITERING ALERT
                # =====================================

                if (
                    time_in_zone >= LOITER_TIME
                    and track_id not in loiter_alerted
                ):

                    print(
                        f"🚨 LOITERING ALERT! "
                        f"Person {track_id} stayed "
                        f"{int(time_in_zone)} sec in zone"
                    )

                    loiter_alerted.add(track_id)

                    beep(1000, 800)

            else:

                # Reset zone timer when leaving zone
                if track_id in zone_entry_time:
                    del zone_entry_time[track_id]

            # =====================================
            # LABELS
            # =====================================

            hours = int(total_time_seen // 3600)
            minutes = int((total_time_seen % 3600) // 60)

            if track_id in zone_entry_time:

                zone_seconds = int(
                    time.time()
                    - zone_entry_time[track_id]
                )

                label = (
                    f"ID:{track_id} "
                    f"Zone:{zone_seconds}s "
                    f"{hours}h {minutes}m"
                )

            else:

                label = (
                    f"ID:{track_id} "
                    f"{hours}h {minutes}m"
                )

            # =====================================
            # DRAW PERSON
            # =====================================

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    # =====================================
    # DISPLAY
    # =====================================

    cv2.imshow(
        "YOLO Security System",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# =====================================
# CLEANUP
# =====================================

cap.release()
cv2.destroyAllWindows()