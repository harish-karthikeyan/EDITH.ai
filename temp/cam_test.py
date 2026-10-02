import cv2

camera_url = "http://192.168.1.37:8080/"

cap = cv2.VideoCapture(camera_url)

while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera stream unavailable")
        break

    cv2.imshow("EDITH Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()