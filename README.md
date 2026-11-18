# Bengaluru SmartSignal

Adaptive traffic-signal prototype. A camera looks down a road; vehicles are
detected with YOLO, assigned to distance zones measured from the stop line,
and the queue length decides how long the green light stays open.

```
camera frame ─► detector (YOLO11-seg) ─► zones (0-30 / 30-50 / 50-70 / >70 m) ─► green time (C engine)
```

## Project layout

```
src/smartsignal/      Python package
  config.py           camera height, tilt, FOV, image size, zone distances
  geometry.py         pixel row <-> ground distance, zone classification
  zones.py            builds the four zone masks / overlay
  detector.py         YOLO vehicle detector (car, motorcycle, bus, truck)
  counter.py          vehicles -> zone counts, left-side filter
  occupancy.py        % of each zone covered by vehicles; sequential zone check
  engine.py           Python bridge to the C green-time engine (ctypes)
  pipeline.py         analyze(frame) -> zone occupancy, counts, green time; overlay drawing
scripts/              runnable demos (need a sample image)
  calibrate.py        draws distance lines on samples/road.jpg
  show_zones.py       shows zones over samples/road.jpg
  detect_image.py     runs detection on an image
  run_signal.py       FULL pipeline on one image
engine/               C green-time logic
  include/green_time.h
  src/green_time.c    queue length -> zone -> green seconds
  src/cli.c           small command-line demo
  tests/              C tests
tests/                Python tests (pytest)
samples/              put road.jpg (1920x1080) here
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Put a 1920x1080 road photo at `samples/road.jpg`. The YOLO weights
(`yolo11n-seg.pt`) download automatically on first detection.

## Run

```bash
PYTHONPATH=src python scripts/calibrate.py     # saves samples/calibration_overlay.jpg
PYTHONPATH=src python scripts/show_zones.py
PYTHONPATH=src python scripts/detect_image.py samples/road.jpg
PYTHONPATH=src python scripts/run_signal.py samples/road.jpg --median-x 960

make engine && ./build/smartsignal_cli          # C demo
make test                                       # Python + C tests
```

## Green-time table

| Zone | Queue length | Green time |
|------|--------------|-----------|
| 1    | 0-30 m       | 15 s      |
| 2    | 30-50 m      | 25 s      |
| 3    | 50-70 m      | 35 s      |
| 4    | > 70 m       | 45 s      |

## How the pipeline decides

1. YOLO finds vehicles and their segmentation masks.
2. Only the road area left of `--median-x` (or `MEDIAN_X` in `config.py`) is used; with no value, the whole frame.
3. Zones are checked **nearest first** (zone 1, 2, 3, 4). A zone is *filled* when vehicle masks cover **more than 30%** of its road area (`OCCUPANCY_THRESHOLD`).
4. At the first zone that is **not** filled, checking stops: later zones are not checked. For example, if zone 2 is under 30%, zones 3 and 4 are ignored.
5. Green time comes from the farthest filled zone (15/25/35/45 s). If even zone 1 is not filled, the minimum (zone 1's 15 s) is used.
6. Vehicle counts are reported only for zones that were checked.

## Roadmap

- [ ] Detect the median automatically (for now set `--median-x` by hand)
- [ ] Single source of truth for zone distances (currently duplicated in `config.py` and `green_time.c`)
