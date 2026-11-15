"""Read CH1 (G5) and CH2 (sensor) levels from the three GDS-1072A-U phone photos of 15.11.2026.

Both channels 1 V/div DC, 1 s/div ROLL, 0 V of both channels on the centre axis ("1>" marker).
Pixel constants were measured from each photo: AXIS = row of the centre axis (0 V),
PX = pixels per division (top grid border to centre axis / 4; same as horizontal 10 div).
Each trace is split into ten time segments and the median trace row of each segment is used.
Photo reading accuracy is about +-0.05 V. Run: python scope_photo_fit.py
"""
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
# file: (plot columns x0..x1, trace rows lo..hi, AXIS row, PX per div)
PHOTOS = {
    "photo1_media.jpg": (190, 835, 740, 1235, 1009.5, 63.9),
    "photo2_media_1.jpg": (170, 795, 765, 1260, 1026.0, 64.0),
    "photo3_media_2.jpg": (150, 795, 655, 1140, 919.0, 63.7),
}


def segments(path, x0, x1, lo, hi, axis, px):
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    masks = {"ch1": (r > 170) & (g > 170) & (b < 140), "ch2": (r < 120) & (g > 150) & (b > 170)}
    out = {}
    for name, m in masks.items():
        rows = [np.median(np.where(m[lo:hi, x])[0] + lo) if m[lo:hi, x].any() else np.nan for x in range(x0, x1)]
        rows = np.array(rows)
        seg = []
        for part in np.array_split(rows, 10):
            part = part[~np.isnan(part)]
            # ignore stray pixels far from the segment's trace
            part = part[np.abs(part - np.median(part)) < 30] if len(part) else part
            v = (axis - np.median(part)) / px if len(part) else np.nan
            # menu text and labels can be picked up as trace; the board cannot give < -0.2 V or > 3.5 V
            seg.append(v if -0.2 <= v <= 3.5 else np.nan)
        out[name] = np.array(seg)
    return out


def main():
    xs, ys = [], []
    for name, c in PHOTOS.items():
        s = segments(HERE / name, *c)
        print(name)
        print("  CH1 G5     V:", " ".join(f"{v:.2f}" for v in s["ch1"]))
        print("  CH2 sensor V:", " ".join(f"{v:.2f}" for v in s["ch2"]))
        ok = ~np.isnan(s["ch1"]) & ~np.isnan(s["ch2"])
        xs += list(s["ch2"][ok]); ys += list(s["ch1"][ok])
    x, y = np.array(xs), np.array(ys)
    a, b = np.polyfit(x, y, 1)
    print(f"\nFit over {len(x)} segments: G5 = {a:.2f} * sensor {b:+.2f} V, r = {np.corrcoef(x, y)[0, 1]:.3f}, "
          f"residual std {np.std(y - a * x - b):.3f} V")
    print(f"Design gain 1 + 10/53.8 = {1 + 10 / 53.8:.3f}; with 6.8 kOhm only 1 + 10/6.8 = {1 + 10 / 6.8:.3f}")
    print(f"Vref implied by the fit: {-b / (a - 1):.2f} V")


if __name__ == "__main__":
    main()
