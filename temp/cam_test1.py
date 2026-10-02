import sys
import cv2

sys.path.insert(0, r"E:\Projects\EDITH.ai")

from camera.stream import CameraStream


CAMERA_URL = "http://192.168.1.37:8080/"

camera = CameraStream(CAMERA_URL)

if not camera.connect():
    print("❌ Camera connection failed")
    exit()

print("✅ EDITH Camera Connected")

while True:

    frame = camera.get_frame()

    if frame is None:
        print("❌ Frame unavailable")
        break

    cv2.imshow("EDITH.ai - Live Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()