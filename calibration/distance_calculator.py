
import math

from camera_config import (
    IMAGE_HEIGHT,
    CAMERA_HEIGHT,
    CAMERA_PITCH,
    VERTICAL_FOV
)


def calculate_focal_length():
    fov = math.radians(VERTICAL_FOV)

    return IMAGE_HEIGHT / (2 * math.tan(fov / 2))


def distance_to_pixel(distance):
    focal_length = calculate_focal_length()

    angle = math.degrees(
        math.atan(CAMERA_HEIGHT / distance)
    )

    beta = angle - CAMERA_PITCH

    center_y = IMAGE_HEIGHT / 2

    pixel_y = (
        center_y
        + focal_length * math.tan(math.radians(beta))
    )

    return pixel_y


def pixel_to_distance(pixel_y):
    focal_length = calculate_focal_length()

    center_y = IMAGE_HEIGHT / 2

    beta = math.degrees(
        math.atan((pixel_y - center_y) / focal_length)
    )

    angle = CAMERA_PITCH + beta

    if angle <= 0:
        return float("inf")

    distance = CAMERA_HEIGHT / math.tan(
        math.radians(angle)
    )

    return distance
