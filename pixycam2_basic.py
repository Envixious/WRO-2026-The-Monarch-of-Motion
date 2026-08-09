"""Basic PixyCam2 reader (USB) in Python.

This script uses the `pixy2` Python module to grab line/object detection
frames and prints summary info.

Notes:
- You may need to install a Pixy2 Python wrapper that provides `pixy2`.
  Common installs are done via pip depending on your setup.
- PixyCam2 typically outputs block/object detections (signature blocks).

Run:
  python pixycam2_basic.py

If your machine has multiple USB devices, you may need to modify the
initialization code to select the correct Pixy device.
"""

from __future__ import annotations

import sys
import time


def main() -> int:
    try:
        import pixy2  # type: ignore
    except Exception:
        print(
            "Failed to import pixy2 Python module. Install it for your PixyCam2 setup.",
            file=sys.stderr,
        )
        raise

    cam = pixy2.Pixy2()

    # Initialize Pixy. Different wrappers expose different init patterns.
    # This matches the common libpixy2 Python style.
    try:
        cam.init()
    except AttributeError:
        # Some wrappers auto-init.
        pass

    print("PixyCam2 started. Press Ctrl+C to stop.")

    last_print = 0.0
    try:
        while True:
            # get blocks/objects
            try:
                blocks = cam.get_blocks()
            except Exception:
                # Some wrappers use different method names
                blocks = None

            now = time.time()
            # Print at a manageable rate
            if now - last_print >= 0.05:
                last_print = now

                if not blocks:
                    print("no blocks")
                    continue

                # blocks is usually a list of objects with fields like signature,x,y,width,height
                # We'll print generically.
                summary = []
                for b in blocks:
                    # handle dict-like or attribute-like blocks
                    sig = getattr(b, "signature", None) if not isinstance(b, dict) else b.get("signature")
                    x = getattr(b, "x", None) if not isinstance(b, dict) else b.get("x")
                    y = getattr(b, "y", None) if not isinstance(b, dict) else b.get("y")
                    w = getattr(b, "width", None) if not isinstance(b, dict) else b.get("width")
                    h = getattr(b, "height", None) if not isinstance(b, dict) else b.get("height")
                    summary.append(f"sig={sig} x={x} y={y} w={w} h={h}")

                print(f"blocks: {len(blocks)} -> " + ", ".join(summary[:5]))

    except KeyboardInterrupt:
        return 0
    finally:
        # Some wrappers provide close/stop
        for method_name in ("close", "stop"):
            try:
                getattr(cam, method_name)()
            except Exception:
                pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())