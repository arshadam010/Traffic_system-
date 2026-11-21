
CAMERA_HEIGHT = 10.0         # metres
CAMERA_TILT = 16.0           # degrees downward
VERTICAL_FOV = 45.0          # degrees
IMAGE_WIDTH = 2752
IMAGE_HEIGHT = 1536

CAMERA_TO_STOP_LINE = 13.0   # metres (must keep arctan(H/d) < TILT + FOV/2)

DISTANCE_ZONES = [30, 50, 75]

# --- Counting / signal settings ---------------------------------------
# Pixel column of the road's middle partition (median). Only vehicles whose
# centre is RIGHT of this column are counted. None = count the whole frame.
MEDIAN_X = 1300

# A zone counts as "filled" when vehicles cover MORE than this fraction of
# its road area. Zones are checked 1 -> 4 and checking stops at the first
# zone that is not filled.
OCCUPANCY_THRESHOLD = 0.10
