import cv2
import numpy as np
from ultralytics import YOLO


# Upgrade from 'n' (nano) to 's' (small) or 'm' (medium) for dense Indian traffic
MODEL_PATH = "yolo11s-seg.pt"

# Vehicle classes in the COCO dataset
VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck"
}


class VehicleDetector:

    def __init__(self, model_path=MODEL_PATH):
        self.model = YOLO(model_path)
        self.target_classes = list(VEHICLE_CLASSES.keys())

    def detect(self, frame):
        """
        Detect vehicles and return their segmentation masks.
        """
        results = self.model.predict(
            frame,
            imgsz=1280,
            conf=0.15,
            iou=0.60,
            classes=self.target_classes,
            verbose=False
        )

        vehicles = []
        h, w = frame.shape[:2]

        for result in results:
            if result.boxes is None:
                continue

            has_masks = result.masks is not None

            for i, box in enumerate(result.boxes):
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                mask = None
                if has_masks:
                    raw_mask = result.masks.data[i].cpu().numpy()
                    resized_mask = cv2.resize(
                        raw_mask,
                        (w, h),
                        interpolation=cv2.INTER_NEAREST
                    )
                    mask = (resized_mask > 0.5).astype(np.uint8)

                vehicles.append({
                    "class": VEHICLE_CLASSES[class_id],
                    "confidence": confidence,
                    "bbox": (x1, y1, x2, y2),
                    "mask": mask
                })

        return vehicles

    def draw_detections(self, frame, vehicles):
        """
        Draw vehicle boxes and labels for visualization.
        """
        output = frame.copy()

        for vehicle in vehicles:
            x1, y1, x2, y2 = vehicle["bbox"]
            label = f'{vehicle["class"]} {vehicle["confidence"]:.2f}'

            cv2.rectangle(
                output,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                output,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        return output