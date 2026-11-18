import pytest

from smartsignal.counter import count_by_zone, locate_vehicle
from smartsignal.geometry import distance_to_pixel
from smartsignal.config import CAMERA_TO_STOP_LINE


def vehicle_at(stop_line_distance, cx=400, w=100, h=80):
    """Fake detection whose bottom edge sits at the given distance."""
    y = round(distance_to_pixel(stop_line_distance + CAMERA_TO_STOP_LINE))
    return {"bbox": (cx - w // 2, y - h, cx + w // 2, y)}


def test_zone_assignment():
    for d, zone in [(20, 1), (40, 2), (60, 3)]:
        z, dist = locate_vehicle(vehicle_at(d)["bbox"], median_x=None)
        assert z == zone
        assert dist == pytest.approx(d, abs=3)


def test_left_side_only():
    left, right = vehicle_at(20, cx=300), vehicle_at(20, cx=1500)
    r = count_by_zone([left, right], median_x=960)
    assert r["counts"][1] == 1
    r = count_by_zone([left, right], median_x=None)
    assert r["counts"][1] == 2


def test_empty_frame():
    r = count_by_zone([])
    assert sum(r["counts"].values()) == 0


def test_vehicle_past_stop_line_ignored():
    z, _ = locate_vehicle((0, 900, 100, 1079))
    assert z is None
