
import cv2
from pathlib import Path

from zones import create_zone_masks, draw_zones

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[1]

IMAGE_PATH = BASE_DIR / "samples" / "road.jpg"

image = cv2.imread(str(IMAGE_PATH))

if image is None:
    raise FileNotFoundError(f"Could not load image: {IMAGE_PATH}")

zone_masks = create_zone_masks()

output = draw_zones(image, zone_masks)

cv2.imshow("Traffic Distance Zones", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
