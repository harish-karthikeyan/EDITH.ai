from ultralytics import YOLO
import torch


DATASET = r"E:\Projects\EDITH.ai\Animal2.v1i.yolov8\data.yaml"
OUTPUT = r"E:\Projects\EDITH.ai\models"


def main():

    print("====================================")
    print("      EDITH WILDLIFE TRAINING")
    print("====================================")

    print("GPU:", torch.cuda.get_device_name(0))
    print("CUDA:", torch.cuda.is_available())

    # Load pretrained YOLO model
    model = YOLO("yolo26n.pt")

    # Train
    model.train(
        data=DATASET,
        epochs=30,
        imgsz=640,
        batch=4,
        device=0,
        workers=2,
        project=OUTPUT,
        name="edith_wildlife"
    )

    print("\n====================================")
    print("      TRAINING COMPLETED")
    print("====================================")

    print("Model saved inside:")
    print(OUTPUT + r"\edith_wildlife")


if __name__ == "__main__":
    main()