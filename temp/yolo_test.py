import sys
import cv2

sys.path.insert(0, r"E:\Projects\EDITH.ai")

from ai.animal_detector import AnimalDetector


CAMERA_URL = "http://192.168.1.37:8080/"


detector = AnimalDetector()

cap = cv2.VideoCapture(CAMERA_URL)

if not cap.isOpened():
    print("❌ Camera connection failed")
    exit()

print("📡 Camera connected")
print("🧠 EDITH is watching...")
print("Press Q to quit")


while True:

    ret, frame = cap.read()

    if not ret:
        print("❌ Frame lost")
        break

    result = detector.detect(frame)

    annotated_frame = result.plot()

    cv2.imshow("EDITH AI - Wildlife Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()