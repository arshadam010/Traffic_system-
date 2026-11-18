"""Run YOLO vehicle detection on one image and show the result.

Usage: python scripts/detect_image.py [path/to/image.jpg]
"""
import sys
from pathlib import Path

import cv2

from smartsignal.detector import VehicleDetector

BASE_DIR = Path(__file__).resolve().parents[1]
image_path = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE_DIR / "samples" / "road.jpg"

image = cv2.imread(str(image_path))
if image is None:
    raise FileNotFoundError(f"Could not load image: {image_path}")

detector = VehicleDetector()
vehicles = detector.detect(image)
output = detector.draw_detections(image, vehicles)

print("Vehicles detected:", len(vehicles))
for vehicle in vehicles:
    print(vehicle["class"], "Confidence:", round(vehicle["confidence"], 2))

cv2.imshow("Vehicle Detection", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
