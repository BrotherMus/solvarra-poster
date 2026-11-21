"""SOLVARRA, Isle of the Sunbell: writes the travel poster to /output/entry.png.

The poster is drawn as SVG in src/poster.html and rendered once by build.py
(headless Edge/Chrome) into entry.png; the sandbox has no browser and no network,
so this program checks that render and copies it into place.
"""
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "entry.png"
OUT_DIR = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT", "/output"))
LIMIT = 1_048_576


def main() -> None:
    data = SRC.read_bytes()
    if not (data[:8] == b"\x89PNG\r\n\x1a\n" or data[:3] == b"\xff\xd8\xff"):
        sys.exit("entry.png is not a PNG or JPEG")
    if len(data) > LIMIT:
        sys.exit(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "entry.png"
    out.write_bytes(data)
    os.chmod(out, 0o644)
    print(f"wrote {out} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
