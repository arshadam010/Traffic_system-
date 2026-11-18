import numpy as np
import pytest

from smartsignal.config import IMAGE_HEIGHT, IMAGE_WIDTH
from smartsignal.occupancy import check_zones
from smartsignal.zones import get_zone_boundaries
from smartsignal.config import CAMERA_TO_STOP_LINE, IMAGE_HEIGHT, IMAGE_WIDTH
from smartsignal.geometry import distance_to_pixel

SHAPE = (IMAGE_HEIGHT, IMAGE_WIDTH, 3)


STOP_LINE_Y = int(round(distance_to_pixel(CAMERA_TO_STOP_LINE)))


def zone_rows(zone):
    b = get_zone_boundaries()          # near -> far: [y30, y50, y70]
    limits = {1: (b[0], STOP_LINE_Y), 2: (b[1], b[0]), 3: (b[2], b[1]), 4: (0, b[2])}
    return limits[zone]

def fill(zone, fraction):
    """Fake vehicle covering `fraction` of the zone (full width)."""
    y1, y2 = zone_rows(zone)
    height = round((y2 - y1) * fraction)
    mask = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH), dtype=np.uint8)
    mask[y1:y1 + height, :] = 1
    return {"bbox": (0, y1, IMAGE_WIDTH, y1 + height), "mask": mask}


def test_empty_road_nothing_filled():
    r = check_zones([], SHAPE)
    assert r["filled"] == [] and r["last_filled_zone"] == 0
    assert r["occupancy"][1] == 0
    assert r["occupancy"][2] is None            # not checked after zone 1 failed


def test_checks_stop_at_first_unfilled_zone():
    # zones 1 and 2 filled, zone 3 empty -> zone 4 must not be checked even if full
    r = check_zones([fill(1, 0.5), fill(2, 0.5), fill(4, 1.0)], SHAPE)
    assert r["filled"] == [1, 2]
    assert r["last_filled_zone"] == 2
    assert r["occupancy"][3] == 0
    assert r["occupancy"][4] is None


def test_zone2_below_30_percent_stops_everything_after():
    r = check_zones([fill(1, 0.6), fill(2, 0.2), fill(3, 0.9)], SHAPE)
    assert r["filled"] == [1]
    assert r["occupancy"][3] is None and r["occupancy"][4] is None


def test_threshold_is_strictly_more_than_30_percent():
    assert check_zones([fill(1, 0.29)], SHAPE)["filled"] == []
    assert check_zones([fill(1, 0.35)], SHAPE)["filled"] == [1]


def test_all_zones_filled():
    r = check_zones([fill(z, 0.5) for z in (1, 2, 3, 4)], SHAPE)
    assert r["filled"] == [1, 2, 3, 4]


def test_median_limits_area():
    # vehicle fills right half only; with median at half the width, left side is empty
    v = fill(1, 1.0)
    v["mask"][:, IMAGE_WIDTH // 2:] = 0
    assert check_zones([v], SHAPE, median_x=IMAGE_WIDTH // 2)["filled"] == []
    assert check_zones([v], SHAPE, median_x=None)["filled"] == [1]
