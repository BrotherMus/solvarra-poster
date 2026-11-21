"""Render src/poster.html to entry.png (1024x1024) with headless Edge or Chrome.

Run locally: python build.py
The committed entry.png is what main.py writes in the sandbox (which has no browser).
"""
import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src" / "poster.html"
OUT = ROOT / "entry.png"
LIMIT = 1_048_576

CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    shutil.which("chromium") or "",
    shutil.which("google-chrome") or "",
]


def browser() -> str:
    for c in CANDIDATES:
        if c and os.path.exists(c):
            return c
    sys.exit("no Edge/Chrome found")


def main() -> None:
    tmp = ROOT / ".shot.png"
    subprocess.run([
        browser(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=1", "--window-size=1024,1024",
        "--virtual-time-budget=3000", f"--screenshot={tmp}", SRC.as_uri(),
    ], check=True, capture_output=True)
    data = tmp.read_bytes()
    tmp.unlink()
    if len(data) > LIMIT:
        # fall back to a high-quality JPEG (the gate takes PNG or JPEG) to stay under 1 MiB
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(data)).convert("RGB")
        for q in (95, 92, 90, 88, 85):
            buf = io.BytesIO()
            img.save(buf, "JPEG", quality=q, optimize=True, subsampling=0)
            if buf.tell() <= LIMIT:
                data = buf.getvalue()
                break
    OUT.write_bytes(data)
    print(f"wrote {OUT.name}: {len(data)} bytes")


if __name__ == "__main__":
    main()
