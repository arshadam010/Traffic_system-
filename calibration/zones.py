
import cv2
import numpy as np

from camera_config import (
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
    CAMERA_TO_STOP_LINE,
    DISTANCE_ZONES
)

from distance_calculator import distance_to_pixel


def get_zone_boundaries():
    """
    Convert stop-line distances into image pixel coordinates.
    """

    boundaries = []

    for distance in DISTANCE_ZONES:

        camera_distance = distance + CAMERA_TO_STOP_LINE

        pixel_y = distance_to_pixel(camera_distance)

        if pixel_y is not None:
            boundaries.append(int(round(pixel_y)))
        else:
            boundaries.append(None)

    return boundaries


def create_zone_masks(road_mask=None):
    """
    Create four image masks representing the distance zones.

    road_mask:
        Optional binary mask of the road.
        White (255) = road.
        Black (0) = not road.
    """

    boundaries = get_zone_boundaries()

    zone_masks = []

    # Image rows are ordered from top (far) to bottom (near).
    image_limits = [0] + boundaries + [IMAGE_HEIGHT]

    for i in range(4):

        y1 = image_limits[i]
        y2 = image_limits[i + 1]

        if y1 is None or y2 is None or y1 >= y2:
            zone_masks.append(np.zeros(
                (IMAGE_HEIGHT, IMAGE_WIDTH),
                dtype=np.uint8
            ))
            continue

        mask = np.zeros(
            (IMAGE_HEIGHT, IMAGE_WIDTH),
            dtype=np.uint8
        )

        cv2.rectangle(
            mask,
            (0, y1),
            (IMAGE_WIDTH - 1, y2 - 1),
            255,
            -1
        )

        if road_mask is not None:
            mask = cv2.bitwise_and(mask, road_mask)

        zone_masks.append(mask)

    return zone_masks


def draw_zones(frame, zone_masks):
    """
    Draw zone boundaries and labels for visual inspection.
    """

    output = frame.copy()

    labels = [
        "ZONE 4: >70m",
        "ZONE 3: 50-70m",
        "ZONE 2: 30-50m",
        "ZONE 1: 0-30m"
    ]

    for i, mask in enumerate(zone_masks):

        ys, xs = np.where(mask > 0)

        if len(ys) == 0:
            continue

        y = int((ys.min() + ys.max()) / 2)

        cv2.putText(
            output,
            labels[i],
            (30, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

    boundaries = get_zone_boundaries()

    for y in boundaries:
        if y is not None:
            cv2.line(
                output,
                (0, y),
                (IMAGE_WIDTH - 1, y),
                (0, 0, 255),
                2
            )

    return output
