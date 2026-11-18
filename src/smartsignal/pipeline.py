"""Frame -> detections -> zone occupancy -> green time."""
import cv2

from smartsignal import engine
from smartsignal.config import MEDIAN_X, OCCUPANCY_THRESHOLD
from smartsignal.counter import count_by_zone
from smartsignal.occupancy import check_zones
from smartsignal.zones import get_zone_boundaries

ZONE_NAMES = {1: "0-30m", 2: "30-50m", 3: "50-70m", 4: ">70m"}


def analyze(frame, detector, median_x=MEDIAN_X, threshold=OCCUPANCY_THRESHOLD):
    """Run the whole chain on one frame.

    Zones are checked 1 -> 4; the first zone that is not filled (>30% by
    default) stops the check. Green time is that of the farthest filled
    zone, or zone 1's time if even zone 1 is not filled.
    """
    h, w = frame.shape[:2]
    vehicles = detector.detect(frame)

    zones = check_zones(vehicles, frame.shape, median_x, threshold)
    counted = count_by_zone(vehicles, w, h, median_x)

    # Only report counts for zones that were actually checked.
    counts = {z: (counted["counts"][z] if zones["occupancy"][z] is not None else None)
              for z in zones["occupancy"]}

    green_zone = max(zones["last_filled_zone"], 1)
    return {
        "occupancy": zones["occupancy"],
        "filled": zones["filled"],
        "counts": counts,
        "counted": counted["counted"],
        "total_detected": len(vehicles),
        "green_zone": green_zone,
        "green_time_s": engine.green_time_for_zone(green_zone),
    }


def draw_result(frame, result, median_x=MEDIAN_X):
    """Overlay zone lines, vehicles, occupancy per zone and green time."""
    out = frame.copy()
    h, w = out.shape[:2]
    scale = h / 1080

    for y in get_zone_boundaries():
        if y is not None:
            yy = int(y * scale)
            cv2.line(out, (0, yy), (w - 1, yy), (0, 0, 255), 2)
    if median_x is not None:
        cv2.line(out, (int(median_x), 0), (int(median_x), h - 1), (255, 0, 0), 2)

    for v, zone, _ in result["counted"]:
        if result["occupancy"][zone] is None:
            continue  # zone not checked
        x1, y1, x2, y2 = v["bbox"]
        colour = (0, 0, 255) if zone in result["filled"] else (0, 255, 0)
        cv2.rectangle(out, (x1, y1), (x2, y2), colour, 2)

    lines = [f"Green time: {result['green_time_s']} s (zone {result['green_zone']})"]
    for z in (4, 3, 2, 1):
        occ = result["occupancy"][z]
        if occ is None:
            lines.append(f"Zone {z} ({ZONE_NAMES[z]}): not checked")
        else:
            flag = "  FILLED" if z in result["filled"] else ""
            lines.append(f"Zone {z} ({ZONE_NAMES[z]}): {occ:.0%}, {result['counts'][z]} veh{flag}")
    for i, text in enumerate(lines):
        cv2.putText(out, text, (30, 40 + 36 * i), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (0, 255, 255), 2)
    return out
