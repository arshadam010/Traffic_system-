import pytest

from smartsignal.config import CAMERA_TO_STOP_LINE, DISTANCE_ZONES, IMAGE_HEIGHT
from smartsignal.geometry import (
    distance_to_pixel,
    get_traffic_zone,
    pixel_to_camera_distance,
    pixel_to_stop_line_distance,
)


def test_pixel_distance_roundtrip():
    for d in [15, 25, 40, 60]:
        y = distance_to_pixel(d)
        if y is None:
            continue
        assert pixel_to_camera_distance(round(y)) == pytest.approx(d, rel=0.05)


def test_far_distances_are_higher_in_image():
    ys = [distance_to_pixel(d + CAMERA_TO_STOP_LINE) for d in DISTANCE_ZONES]
    ys = [y for y in ys if y is not None]
    assert ys == sorted(ys, reverse=True)


def test_out_of_range_pixels_return_none():
    assert pixel_to_camera_distance(-1) is None
    assert pixel_to_camera_distance(IMAGE_HEIGHT) is None
    assert pixel_to_stop_line_distance(-1) is None


def test_invalid_distance_to_pixel():
    assert distance_to_pixel(None) is None
    assert distance_to_pixel(0) is None


@pytest.mark.parametrize(
    "distance, zone",
    [(0, "ZONE_1"), (30, "ZONE_1"), (31, "ZONE_2"), (50, "ZONE_2"),
     (70, "ZONE_3"), (71, "ZONE_4"), (-1, "INVALID"), (None, "INVALID")],
)
def test_get_traffic_zone(distance, zone):
    assert get_traffic_zone(distance) == zone
