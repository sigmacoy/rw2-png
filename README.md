# rw2-png

Recursively scans a folder, converts every `.rw2` file it finds, and writes full-resolution 16-bit PNGs into a `RAW png pics/` subfolder next to each source file. Originals are never modified.

---

## Setup

### macOS

```bash
cd rw2-png
python3 -m venv .venv
source .venv/bin/activate
.venv/bin/python3 -m pip install rawpy numpy opencv-python-headless
```

### Windows

```powershell
cd rw2-png
python -m venv .venv
.venv\Scripts\activate
pip install rawpy numpy opencv-python-headless
```

## Usage

```bash
python3 rw2_to_png.py {path}
```

**Example output:**

```
/photos/
  trip/
    IMG_0001.RW2              ← untouched
    IMG_0002.RW2              ← untouched
    RAW png pics/
      IMG_0001.png            ← 16-bit PNG
      IMG_0002.png
```

- Re-runs are safe — existing PNGs are skipped.
- Corrupt or unsupported files are logged and skipped without stopping the batch.
- Originals are never deleted, moved, or renamed.