"""How much of each distance zone is covered by vehicles."""
import cv2
import numpy as np

from smartsignal.config import IMAGE_HEIGHT, IMAGE_WIDTH, MEDIAN_X, OCCUPANCY_THRESHOLD
from smartsignal.zones import create_zone_masks


def road_mask_left_of(median_x):
    """Binary mask of the counted road area: columns left of the median."""
    if median_x is None:
        return None
    mask = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH), dtype=np.uint8)
    mask[:, int(median_x):] = 255
    return mask


def vehicles_union_mask(vehicles, frame_shape):
    """Union of all vehicle masks, resized to the calibration size.

    A vehicle without a segmentation mask falls back to its bounding box.
    """
    h, w = frame_shape[:2]
    union = np.zeros((h, w), dtype=np.uint8)
    for v in vehicles:
        if v.get("mask") is not None:
            union |= (v["mask"] > 0).astype(np.uint8)
        else:
            x1, y1, x2, y2 = v["bbox"]
            union[max(y1, 0):max(y2, 0), max(x1, 0):max(x2, 0)] = 1
    if (w, h) != (IMAGE_WIDTH, IMAGE_HEIGHT):
        union = cv2.resize(union, (IMAGE_WIDTH, IMAGE_HEIGHT), interpolation=cv2.INTER_NEAREST)
    return union


def check_zones(vehicles, frame_shape, median_x=MEDIAN_X, threshold=OCCUPANCY_THRESHOLD):
    """Check zones nearest-first and stop at the first one not filled.

    A zone is filled when vehicles cover MORE than `threshold` of its road
    area. Zones after the first unfilled one are not checked.

    Returns {"occupancy": {zone: fraction or None}, "filled": [zones],
             "last_filled_zone": int (0 if none)}
    where None means "not checked".
    """
    zone_masks = create_zone_masks(road_mask_left_of(median_x))
    union = vehicles_union_mask(vehicles, frame_shape) > 0

    occupancy = {z: None for z in range(1, len(zone_masks) + 1)}
    filled = []
    # create_zone_masks is ordered far -> near, so zone z is zone_masks[-z]
    for zone in range(1, len(zone_masks) + 1):
        zmask = zone_masks[-zone] > 0
        area = int(zmask.sum())
        fraction = float((union & zmask).sum()) / area if area else 0.0
        occupancy[zone] = fraction
        if fraction > threshold:
            filled.append(zone)
        else:
            break

    return {
        "occupancy": occupancy,
        "filled": filled,
        "last_filled_zone": filled[-1] if filled else 0,
    }
