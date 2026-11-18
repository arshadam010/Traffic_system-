import argparse

import cv2

from smartsignal.config import MEDIAN_X
from smartsignal.detector import VehicleDetector
from smartsignal.pipeline import analyze, draw_result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("image")
    p.add_argument("--median-x", type=int, default=MEDIAN_X,
                   help="pixel column of the road median; only the right side is used")
    p.add_argument("--no-show", action="store_true", help="print only, no window")
    args = p.parse_args()

    frame = cv2.imread(args.image)
    if frame is None:
        raise FileNotFoundError(args.image)

    result = analyze(frame, VehicleDetector(), args.median_x)

    for z in (1, 2, 3, 4):
        occ = result["occupancy"][z]
        if occ is None:
            print(f"Zone {z}: not checked")
        else:
            state = "FILLED" if z in result["filled"] else "not filled"
            print(f"Zone {z}: {occ:.0%} covered, {result['counts'][z]} vehicles -> {state}")
    print(f"Green time: {result['green_time_s']} s (based on zone {result['green_zone']})")

    if not args.no_show:
        cv2.imshow("SmartSignal", draw_result(frame, result, args.median_x))
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
