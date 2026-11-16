import cv2
from pathlib import Path

from camera_config import IMAGE_WIDTH, IMAGE_HEIGHT, DISTANCE_ZONES
from distance_calculator import distance_to_pixel

BASE_DIR = Path(__file__).resolve().parents[1]
IMAGE_PATH = BASE_DIR / "samples" / "road.jpg"
OUTPUT_PATH = BASE_DIR / "samples" / "calibration_overlay.jpg"

image = cv2.imread(str(IMAGE_PATH))

if image is None:
    raise FileNotFoundError(f"Could not load road image: {IMAGE_PATH}")

height, width = image.shape[:2]

if (width, height) != (IMAGE_WIDTH, IMAGE_HEIGHT):
    raise ValueError(
        f"Expected image dimensions {IMAGE_WIDTH}x{IMAGE_HEIGHT}, got {width}x{height}."
    )

for distance in DISTANCE_ZONES:
    raw_y = distance_to_pixel(distance)
    if raw_y is None:
        continue

    y = int(round(raw_y))
    if 0 <= y < height:
        cv2.line(image, (0, y), (width, y), (0, 0, 255), 2)
        cv2.putText(
            image,
            f"{distance} metres",
            (30, max(y - 10, 25)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
        )

cv2.imwrite(str(OUTPUT_PATH), image)
print(f"Calibration overlay saved at: {OUTPUT_PATH}")