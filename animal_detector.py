from ultralytics import YOLO


class AnimalDetector:

    def __init__(self, model_path="yolo26n.pt"):

        print("Loading EDITH Vision Model...")

        self.model = YOLO(model_path)

        print("EDITH Vision Model: READY")

    def detect(self, frame):

        results = self.model.predict(
            source=frame,
            conf=0.35,
            verbose=False
        )

        return results[0]