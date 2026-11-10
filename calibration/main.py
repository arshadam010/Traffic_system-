
import cv2
from pathlib import Path

from camera_config import TARGET_DISTANCES
from distance_calculator import distance_to_pixel

BASE_DIR = Path(__file__).resolve().parents[1]
IMAGE_PATH = BASE_DIR / "samples" / "road.jpg"
OUTPUT_PATH = BASE_DIR / "samples" / "calibration_overlay.jpg"

image = cv2.imread(str(IMAGE_PATH))

if image is None:
    raise FileNotFoundError(
        f"Could not load road image: {IMAGE_PATH}"
    )

height, width = image.shape[:2]

if height != 1080:
    raise ValueError("Expected an image with height 1080 pixels.")

for distance in TARGET_DISTANCES:
    y = int(round(distance_to_pixel(distance)))

    if 0 <= y < height:
        cv2.line(
            image,
            (0, y),
            (width, y),
            (0, 0, 255),
            2
        )

        cv2.putText(
            image,
            f"{distance} metres",
            (30, max(y - 10, 25)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

cv2.imwrite(str(OUTPUT_PATH), image)

print(f"Calibration overlay saved at: {OUTPUT_PATH}")