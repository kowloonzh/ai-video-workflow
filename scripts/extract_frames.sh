#!/usr/bin/env bash
# 从视频抽帧检查。
# 用法: extract_frames.sh 视频 输出目录 [每秒帧数，默认 4]
# 输出: 输出目录/f_0001.png ...（按 fps 抽帧）、first.png、last.png、info.txt
set -euo pipefail

if [ $# -lt 2 ]; then
  echo "用法: $0 视频 输出目录 [每秒帧数]" >&2
  exit 1
fi

in="$1"
out="$2"
fps="${3:-4}"
mkdir -p "$out"

ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,nb_frames,duration,color_space,color_primaries,color_transfer,pix_fmt \
  -of default=noprint_wrappers=1 "$in" > "$out/info.txt"
ffprobe -v error -select_streams a -show_entries stream=codec_name,channels \
  -of default=noprint_wrappers=1 "$in" >> "$out/info.txt" || true
cat "$out/info.txt"

ffmpeg -v error -y -i "$in" -vf "fps=$fps" "$out/f_%04d.png"
ffmpeg -v error -y -i "$in" -vf "select=eq(n\,0)" -frames:v 1 "$out/first.png"
ffmpeg -v error -y -sseof -0.1 -i "$in" -update 1 -q:v 1 "$out/last.png"

echo "抽帧完成: $(ls "$out"/f_*.png | wc -l) 张 -> $out"
