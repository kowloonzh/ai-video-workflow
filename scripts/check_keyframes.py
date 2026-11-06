#!/usr/bin/env python3
"""检查一组首尾帧：尺寸是否一致、画幅是否正确，并输出叠加图和差异热图。

用法:
  python check_keyframes.py first.png last.png [--aspect 16:9] [--out DIR] [--crop]

--crop  若画幅不对，按目标画幅居中裁切，另存为 *_cropped.png（不覆盖原图）
输出:
  DIR/overlay.png   首尾帧 50% 叠加（错位处会出现重影）
  DIR/diff.png      差异热图（越亮差异越大；不该变的地方应该是黑的）
  DIR/side.png      左右并排
  DIR/gray_first.png / gray_last.png  黑白版，检查明暗对比
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image, ImageOps


def parse_aspect(s):
    w, h = s.split(":")
    return float(w) / float(h)


def center_crop(img, aspect):
    w, h = img.size
    if w / h > aspect:
        nw = round(h * aspect)
        left = (w - nw) // 2
        return img.crop((left, 0, left + nw, h))
    nh = round(w / aspect)
    top = (h - nh) // 2
    return img.crop((0, top, w, top + nh))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("first")
    ap.add_argument("last")
    ap.add_argument("--aspect", default="16:9")
    ap.add_argument("--out", default=None)
    ap.add_argument("--crop", action="store_true")
    a = ap.parse_args()

    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.first)), "check")
    os.makedirs(out, exist_ok=True)
    target = parse_aspect(a.aspect)

    imgs = []
    problems = []
    for p in (a.first, a.last):
        im = Image.open(p).convert("RGB")
        w, h = im.size
        ratio = w / h
        ok = abs(ratio - target) < 0.01
        print(f"{p}: {w}x{h}  ratio={ratio:.4f}  target={target:.4f}  {'OK' if ok else 'ASPECT MISMATCH'}")
        if not ok:
            problems.append(f"{os.path.basename(p)} 画幅不对")
            if a.crop:
                c = center_crop(im, target)
                root, _ = os.path.splitext(p)
                cp = root + "_cropped.png"
                c.save(cp)
                print(f"  -> 居中裁切另存: {cp} ({c.size[0]}x{c.size[1]})")
                im = c
        imgs.append(im)

    f, l = imgs
    if f.size != l.size:
        problems.append(f"首尾帧尺寸不一致: {f.size} vs {l.size}")
        print(f"SIZE MISMATCH: {f.size} vs {l.size}（对比图按首帧尺寸缩放尾帧，仅供参考）")
        l = l.resize(f.size, Image.LANCZOS)

    fa = np.asarray(f, dtype=np.float32)
    la = np.asarray(l, dtype=np.float32)
    diff = np.abs(fa - la).mean(axis=2)
    Image.blend(f, l, 0.5).save(os.path.join(out, "overlay.png"))
    d = diff / max(diff.max(), 1.0) * 255
    Image.fromarray(d.astype(np.uint8)).save(os.path.join(out, "diff.png"))

    side = Image.new("RGB", (f.size[0] * 2, f.size[1]))
    side.paste(f, (0, 0))
    side.paste(l, (f.size[0], 0))
    side.save(os.path.join(out, "side.png"))
    ImageOps.grayscale(f).save(os.path.join(out, "gray_first.png"))
    ImageOps.grayscale(l).save(os.path.join(out, "gray_last.png"))

    # 按 4x4 网格报告差异，帮助定位"不该变却变了"的区域
    gh, gw = 4, 4
    H, W = diff.shape
    print("\n差异网格（平均像素差 0-255，从左上到右下）：")
    for r in range(gh):
        row = []
        for c in range(gw):
            cell = diff[r * H // gh:(r + 1) * H // gh, c * W // gw:(c + 1) * W // gw]
            row.append(f"{cell.mean():6.1f}")
        print("  " + " ".join(row))
    print(f"\n整体平均差异: {diff.mean():.1f}")
    print(f"输出目录: {out}")
    if problems:
        print("\n问题:\n  - " + "\n  - ".join(problems))
        sys.exit(1)


if __name__ == "__main__":
    main()
