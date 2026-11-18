import math

from smartsignal.config import (
    CAMERA_HEIGHT,
    CAMERA_TILT,
    VERTICAL_FOV,
    IMAGE_HEIGHT,
    CAMERA_TO_STOP_LINE,
    DISTANCE_ZONES,
)


def pixel_to_camera_distance(pixel_y):
    """
    Estimate horizontal ground distance from the
    camera's ground projection to a point on the road.
    """
    if not 0 <= pixel_y < IMAGE_HEIGHT:
        return None

    normalized_y = (2 * (pixel_y + 0.5) / IMAGE_HEIGHT) - 1
    pixel_angle = math.degrees(
        math.atan(normalized_y * math.tan(math.radians(VERTICAL_FOV / 2)))
    )

    angle_down = CAMERA_TILT + pixel_angle

    if angle_down <= 0.1 or angle_down >= 89.9:
        return None

    distance = CAMERA_HEIGHT / math.tan(math.radians(angle_down))
    return distance if math.isfinite(distance) else None


def distance_to_pixel(distance):
    """
    Convert a horizontal ground distance from the camera
    into its corresponding vertical pixel coordinate (pixel_y).
    """
    if distance is None or distance <= 0:
        return None

    angle_down = math.degrees(math.atan(CAMERA_HEIGHT / distance))
    pixel_angle = angle_down - CAMERA_TILT

    half_fov = VERTICAL_FOV / 2
    if not (-half_fov <= pixel_angle <= half_fov):
        return None

    normalized_y = math.tan(math.radians(pixel_angle)) / math.tan(
        math.radians(half_fov)
    )
    pixel_y = ((normalized_y + 1) * IMAGE_HEIGHT / 2) - 0.5

    if not 0 <= pixel_y < IMAGE_HEIGHT:
        return None

    return pixel_y


def pixel_to_stop_line_distance(pixel_y):
    """
    Estimate vehicle distance from the stop line.
    """
    camera_distance = pixel_to_camera_distance(pixel_y)
    if camera_distance is None:
        return None

    return camera_distance - CAMERA_TO_STOP_LINE


def get_traffic_zone(distance):
    """
    Classify the distance from the stop line using DISTANCE_ZONES.
    """
    if distance is None or distance < 0:
        return "INVALID"

    for idx, threshold in enumerate(DISTANCE_ZONES, start=1):
        if distance <= threshold:
            return f"ZONE_{idx}"

    return f"ZONE_{len(DISTANCE_ZONES) + 1}"