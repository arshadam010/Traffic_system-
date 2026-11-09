
from camera_config import TARGET_DISTANCES
from distance_calculator import (
    distance_to_pixel,
    pixel_to_distance
)

print("Bengaluru SmartSignal - Camera Calibration")
print("------------------------------------------")

for distance in TARGET_DISTANCES:

    pixel = distance_to_pixel(distance)

    recovered_distance = pixel_to_distance(pixel)

    print(
        f"Distance: {distance:3} m | "
        f"Pixel row: {pixel:7.2f} | "
        f"Verified distance: {recovered_distance:.2f} m"
    )
