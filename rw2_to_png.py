#!/usr/bin/env python3
"""
Batch-convert Panasonic RAW (.rw2) files to 16-bit PNG.

pip install rawpy numpy opencv-python-headless
"""

import os
import sys
import rawpy
import numpy as np
import cv2

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

OUTPUT_DIR_NAME = "RAW png pics"


def find_rw2_files(root: str) -> list[str]:
    """Recursively find all .rw2 files under *root* (case-insensitive)."""
    found = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fname in filenames:
            if fname.lower().endswith(".rw2"):
                found.append(os.path.join(dirpath, fname))
    return sorted(found)


def save_png_16bit(rgb16: np.ndarray, dest: str) -> None:
    """Save a uint16 RGB array as a 16-bit PNG using OpenCV."""
    # OpenCV expects BGR channel order
    bgr = cv2.cvtColor(rgb16, cv2.COLOR_RGB2BGR)
    cv2.imwrite(dest, bgr)


def convert_one(src: str, dest: str) -> None:
    """Decode a single .rw2 and write a 16-bit PNG to *dest*."""
    with rawpy.imread(src) as raw:
        rgb = raw.postprocess(
            use_camera_wb=True,
            no_auto_bright=False,
            output_bps=16,
            output_color=rawpy.ColorSpace.sRGB,
        )
    save_png_16bit(rgb, dest)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} /path/to/photos")
        sys.exit(1)

    root = os.path.abspath(sys.argv[1])
    if not os.path.isdir(root):
        print(f"Error: '{root}' is not a directory.")
        sys.exit(1)

    # Discover files
    rw2_files = find_rw2_files(root)
    total = len(rw2_files)
    if total == 0:
        print("No .rw2 files found.")
        return

    print(f"Found {total} .rw2 file(s) under {root}\n")

    converted = 0
    skipped = 0
    failed: list[tuple[str, str]] = []  # (path, error)

    for idx, src in enumerate(rw2_files, start=1):
        base = os.path.splitext(os.path.basename(src))[0]
        parent = os.path.dirname(src)
        out_dir = os.path.join(parent, OUTPUT_DIR_NAME)
        dest = os.path.join(out_dir, base + ".png")

        # Skip if already converted
        if os.path.exists(dest):
            print(f"[{idx}/{total}] skipped (exists) {src}")
            skipped += 1
            continue

        print(f"[{idx}/{total}] converting {src}")

        try:
            os.makedirs(out_dir, exist_ok=True)
            convert_one(src, dest)
            converted += 1
        except Exception as exc:
            failed.append((src, str(exc)))
            print(f"         ⚠ FAILED: {exc}")

    # Summary
    print("\n--- Summary ---")
    print(f"  Total found : {total}")
    print(f"  Converted   : {converted}")
    print(f"  Skipped     : {skipped}")
    print(f"  Failed      : {len(failed)}")
    if failed:
        print("\nFailed files:")
        for path, err in failed:
            print(f"  {path}  —  {err}")


if __name__ == "__main__":
    main()
