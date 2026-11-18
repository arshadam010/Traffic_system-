
CAMERA_HEIGHT = 6.0          # metres
CAMERA_TILT = 30.0           # degrees downward
VERTICAL_FOV = 60.0          # degrees
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080

CAMERA_TO_STOP_LINE = 10.0   # metres

DISTANCE_ZONES = [30, 50, 70]

# --- Counting / signal settings ---------------------------------------
# Pixel column of the road's middle partition (median). Only vehicles whose
# centre is LEFT of this column are counted. None = count the whole frame.
MEDIAN_X = 960

# A zone counts as "filled" when vehicles cover MORE than this fraction of
# its road area. Zones are checked 1 -> 4 and checking stops at the first
# zone that is not filled.
OCCUPANCY_THRESHOLD = 0.30
