import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from gesture import GestureDetector
from controller import Controller


# -----------------------------
# MediaPipe Hand Landmarker
# -----------------------------

base_options = python.BaseOptions(
    model_asset_path="models/hand_landmarker.task"
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=2,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7,
)

detector = vision.HandLandmarker.create_from_options(options)

gesture_detector = GestureDetector()
controller = Controller()


# -----------------------------
# Camera
# -----------------------------

cap = cv2.VideoCapture(0)

timestamp = 0

while True:

    success, frame = cap.read()

    if not success:
        print("Could not access camera")
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    # Convert BGR -> RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # Convert to MediaPipe image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    timestamp += 1

    # Detect hand
    result = detector.detect_for_video(
        mp_image,
        timestamp
    )


    # -----------------------------
    # Hand detected
    # -----------------------------

    for hand in result.hand_landmarks:

        height, width, _ = frame.shape


        # -----------------------------
        # Draw landmarks
        # -----------------------------

        for landmark in hand:

            x = int(landmark.x * width)
            y = int(landmark.y * height)

            cv2.circle(
                frame,
                (x, y),
                5,
                (0, 255, 0),
                -1
            )


        # -----------------------------
        # Index finger
        # -----------------------------

        index_tip = hand[8]

        index_x = int(index_tip.x * width)
        index_y = int(index_tip.y * height)

        cv2.circle(
            frame,
            (index_x, index_y),
            10,
            (255, 0, 0),
            -1
        )


        # -----------------------------
        # Move cursor
        # -----------------------------

        controller.move_cursor(
            index_tip.x,
            index_tip.y
        )


        # -----------------------------
        # Detect pinch
        # -----------------------------

        pinch_started = gesture_detector.detect_pinch(hand)

        if pinch_started:

            controller.click()

            cv2.putText(
                frame,
                "CLICK",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )


        # -----------------------------
        # Detect scroll direction
        # -----------------------------

        direction = gesture_detector.detect_index_direction(hand)

        if direction == "up":

            controller.scroll(
                "up",
                amount=200
            )

            cv2.putText(
                frame,
                "SCROLL UP",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        elif direction == "down":

            controller.scroll(
                "down",
                amount=200
            )

            cv2.putText(
                frame,
                "SCROLL DOWN",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )


    # -----------------------------
    # Show camera
    # -----------------------------

    cv2.imshow(
        "Hand Scroll",
        frame
    )


    # -----------------------------
    # Press Q to quit
    # -----------------------------

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# -----------------------------
# Cleanup
# -----------------------------

cap.release()

detector.close()

cv2.destroyAllWindows()