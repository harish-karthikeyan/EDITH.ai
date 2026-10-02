import cv2


class CameraStream:

    def __init__(self, camera_url):
        self.camera_url = camera_url
        self.cap = None

    def connect(self):

        self.cap = cv2.VideoCapture(self.camera_url)

        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not self.cap.isOpened():
            self.cap.release()
            self.cap = None
            return False

        return True

    def get_frame(self):

        if self.cap is None:
            return None

        ret, frame = self.cap.read()

        if not ret:
            return None

        return frame

    def release(self):

        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def is_connected(self):

        return self.cap is not None and self.cap.isOpened()