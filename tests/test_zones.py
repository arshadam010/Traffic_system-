import numpy as np

from smartsignal.config import IMAGE_HEIGHT, IMAGE_WIDTH
from smartsignal.zones import create_zone_masks, get_zone_boundaries


def test_four_masks_with_image_shape():
    masks = create_zone_masks()
    assert len(masks) == 4
    assert all(m.shape == (IMAGE_HEIGHT, IMAGE_WIDTH) for m in masks)


def test_masks_do_not_overlap():
    masks = create_zone_masks()
    total = sum((m > 0).astype(int) for m in masks)
    assert total.max() <= 1


def test_road_mask_restricts_zones():
    road = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH), dtype=np.uint8)
    road[:, : IMAGE_WIDTH // 2] = 255  # left half only
    for m in create_zone_masks(road):
        assert not m[:, IMAGE_WIDTH // 2 :].any()


def test_boundaries_count():
    assert len(get_zone_boundaries()) == 3


def test_every_zone_has_rows_and_far_zone_is_on_top():
    masks = create_zone_masks()
    tops = []
    for m in masks:
        rows = np.where((m > 0).any(axis=1))[0]
        assert len(rows) > 0
        tops.append(rows.min())
    # masks[0] is the farthest zone (>70m): it must start highest in the image
    assert tops == sorted(tops)
