"""Python bridge to the C green-time engine (engine/src/green_time.c)."""
import ctypes
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_LIB_NAME = "green_time.dll" if sys.platform == "win32" else (
    "libgreen_time.dylib" if sys.platform == "darwin" else "libgreen_time.so"
)
LIB_PATH = ROOT / "build" / _LIB_NAME

_lib = None


def _build():
    gcc = shutil.which("gcc") or shutil.which("cc")
    if gcc is None:
        raise RuntimeError("C compiler (gcc) not found; install it or run `make lib`.")
    LIB_PATH.parent.mkdir(exist_ok=True)
    subprocess.run(
        [gcc, "-shared", "-fPIC", "-O2", f"-I{ROOT / 'engine' / 'include'}",
         str(ROOT / "engine" / "src" / "green_time.c"), "-o", str(LIB_PATH)],
        check=True,
    )


def _load():
    global _lib
    if _lib is None:
        if not LIB_PATH.exists():
            _build()
        lib = ctypes.CDLL(str(LIB_PATH))
        for fn in (lib.classify_queue, lib.calculate_green_time):
            fn.argtypes = [ctypes.c_double]
            fn.restype = ctypes.c_int
        lib.green_time_for_zone.argtypes = [ctypes.c_int]
        lib.green_time_for_zone.restype = ctypes.c_int
        _lib = lib
    return _lib


def classify_queue(queue_length_m):
    return _load().classify_queue(float(queue_length_m))


def calculate_green_time(queue_length_m):
    """Green time in seconds for a queue length in metres (-1 if invalid)."""
    return _load().calculate_green_time(float(queue_length_m))


def green_time_for_zone(zone):
    """Green time in seconds for zone 1-4 (-1 if invalid)."""
    return _load().green_time_for_zone(int(zone))
