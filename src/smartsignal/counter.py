"""Assign detected vehicles to distance zones and count them."""
from smartsignal.config import DISTANCE_ZONES, IMAGE_HEIGHT, MEDIAN_X
from smartsignal.geometry import get_traffic_zone, pixel_to_stop_line_distance

NUM_ZONES = len(DISTANCE_ZONES) + 1


def locate_vehicle(bbox, frame_width=None, frame_height=None, median_x=MEDIAN_X):
    """Return (zone, distance_m) for one vehicle, or (None, None) if it
    should not be counted.

    A vehicle's position is the bottom-centre of its box (where its wheels
    touch the road). Not counted when:
      * it is right of the median (median_x set),
      * it has already passed the stop line (negative distance),
      * its row cannot be mapped to a ground distance.
    """
    x1, y1, x2, y2 = bbox
    cx = (x1 + x2) / 2

    if median_x is not None and cx < median_x:
        return None, None

    y = y2
    if frame_height and frame_height != IMAGE_HEIGHT:
        y = y2 * IMAGE_HEIGHT / frame_height
    y = min(max(y, 0), IMAGE_HEIGHT - 1)

    distance = pixel_to_stop_line_distance(y)
    if median_x is not None and cx < median_x:
        return None, None

    zone_name = get_traffic_zone(distance)
    if zone_name == "INVALID":
        return None, None
    zone = int(zone_name.split("_")[1])

    return zone, distance


def count_by_zone(vehicles, frame_width=None, frame_height=None, median_x=MEDIAN_X):
    """Count vehicles per zone.

    Returns {"counts": {1: n, ..., 4: n}, "counted": [(vehicle, zone, distance_m)]}.
    """
    counts = {z: 0 for z in range(1, NUM_ZONES + 1)}
    counted = []
    for v in vehicles:
        zone, distance = locate_vehicle(v["bbox"], frame_width, frame_height, median_x)
        if zone is None:
            continue
        counts[zone] += 1
        counted.append((v, zone, distance))
    return {"counts": counts, "counted": counted}
