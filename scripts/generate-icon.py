# -*- coding: utf-8 -*-
"""Export the selected logo candidate as the extension icon.

Change SELECTED and re-run:  py -3 scripts/generate-icon.py
The drawing code lives in generate-icon-candidates.py so both stay in sync.
"""

import importlib.util
import io
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
SELECTED = "02"          # candidate number -> assets/icon.png
SIZES = (256, 512)

spec = importlib.util.spec_from_file_location(
    "cands", os.path.join(HERE, "generate-icon-candidates.py"))
cands = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cands)


def save_png(img, path):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(buf.getvalue())


def main():
    match = [c for c in cands.CANDIDATES if c[0] == SELECTED]
    if not match:
        raise SystemExit("no candidate numbered %s" % SELECTED)
    num, name, draw = match[0]
    icon = draw()
    print("selected %s-%s" % (num, name))

    for size in SIZES:
        out = os.path.join(BASE, "assets", "icon.png" if size == SIZES[0] else "icon-%d.png" % size)
        save_png(icon.resize((size, size), Image.LANCZOS), out)
        print("wrote", os.path.relpath(out, BASE), size)


if __name__ == "__main__":
    main()
