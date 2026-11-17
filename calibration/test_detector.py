
import cv2
from detector import VehicleDetector

IMAGE_PATH = "samples/road.jpg"

image = cv2.imread(IMAGE_PATH)

if image is None:
    raise FileNotFoundError(IMAGE_PATH)

detector = VehicleDetector()

vehicles = detector.detect(image)

output = detector.draw_detections(image, vehicles)

print("Vehicles detected:", len(vehicles))

for vehicle in vehicles:
    print(
        vehicle["class"],
        "Confidence:",
        round(vehicle["confidence"], 2)
    )

cv2.imshow("Vehicle Detection", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
