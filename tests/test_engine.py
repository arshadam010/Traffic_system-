import shutil

import pytest

pytestmark = pytest.mark.skipif(shutil.which("gcc") is None, reason="gcc not installed")


def test_engine_matches_table():
    from smartsignal import engine
    assert engine.calculate_green_time(10) == 15
    assert engine.calculate_green_time(40) == 25
    assert engine.calculate_green_time(60) == 35
    assert engine.calculate_green_time(100) == 45
    assert engine.calculate_green_time(-1) == -1


def test_green_time_for_zone():
    from smartsignal import engine
    assert [engine.green_time_for_zone(z) for z in (1, 2, 3, 4)] == [15, 25, 35, 45]
    assert engine.green_time_for_zone(0) == -1
