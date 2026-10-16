#!/usr/bin/env bash
# MANYEON FILM01 조립: 컷 10개 + 자막/로고 오버레이 + 색 보정 → 본편 / 포트폴리오 버전
# usage: assemble_film01.sh <cuts_dir> <overlay_dir> <slate_png> <out_dir>
set -eu
F=${FFMPEG:-ffmpeg}
C=$1; O=$2; SLATE=$3; OUT=$4; mkdir -p "$OUT"
clips=(01_drop-hook 02_into-droplet 03_glacier-drop 04_waterfall-dive 05_fern-dew 06_city-window 07_woman-window 08_serum-drop 09_hero-bottle 10_ripple-end)
TMP=$(mktemp -d)
# 1) 컷마다 규격 통일 + 컷별 페이드 (영상/오디오)
for c in "${clips[@]}"; do
  in="$C/${c}_CUT.mp4"
  d=$($F -i "$in" 2>&1 | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p' | awk -F: '{print $1*3600+$2*60+$3}')
  vf="scale=1920:1080,fps=24,format=yuv420p"; af="aresample=48000,aformat=channel_layouts=stereo"
  case $c in
    01_drop-hook) vf="$vf,fade=t=in:st=0:d=0.4";;
    04_waterfall-dive) af="$af,afade=t=out:st=$(echo "$d-0.12"|bc):d=0.12";;
    05_fern-dew) af="$af,volume=0:enable='lt(t,0.3)',afade=t=in:st=0.3:d=0.4";;
    09_hero-bottle) vf="$vf,fade=t=out:st=$(echo "$d-0.35"|bc):d=0.35"; af="$af,afade=t=out:st=$(echo "$d-0.35"|bc):d=0.35";;
    10_ripple-end) vf="$vf,fade=t=in:st=0:d=0.35,fade=t=out:st=$(echo "$d-0.6"|bc):d=0.6"; af="$af,afade=t=out:st=$(echo "$d-0.8"|bc):d=0.8";;
  esac
  if $F -i "$in" 2>&1 | grep -q "Audio:"; then
    $F -loglevel error -y -i "$in" -vf "$vf" -af "$af" -c:v libx264 -crf 14 -preset medium -c:a pcm_s16le "$TMP/$c.mov"
  else
    $F -loglevel error -y -i "$in" -f lavfi -i anullsrc=r=48000:cl=stereo -vf "$vf" -shortest -c:v libx264 -crf 14 -preset medium -c:a pcm_s16le "$TMP/$c.mov"
  fi
  echo "file '$TMP/$c.mov'" >> "$TMP/list.txt"
done
$F -loglevel error -y -f concat -safe 0 -i "$TMP/list.txt" -c copy "$TMP/body.mov"
TOTAL=$($F -i "$TMP/body.mov" 2>&1 | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p' | awk -F: '{print $1*3600+$2*60+$3}')
# 2) 자막 타이밍 (#3 시작 7.08s, #10 시작 37.41s 기준)
T1S=8.0;  T1E=10.3
T2S=40.0; T2E=42.0
T3S=42.3; T3E=$TOTAL
ov() { # name start end
  echo "[$1:v]format=rgba,fade=t=in:st=$2:d=0.5:alpha=1,fade=t=out:st=$(echo "$3-0.5"|bc):d=0.5:alpha=1[o$1]"
}
$F -loglevel error -y -i "$TMP/body.mov" \
  -loop 1 -t "$TOTAL" -i "$O/ov-t1.png" -loop 1 -t "$TOTAL" -i "$O/ov-t2.png" -loop 1 -t "$TOTAL" -i "$O/ov-t3.png" \
  -filter_complex "[0:v]eq=saturation=0.9:contrast=0.97,curves=all='0/0.025 1/1',noise=alls=3:allf=t[g];\
$(ov 1 $T1S $T1E);$(ov 2 $T2S $T2E);$(ov 3 $T3S $T3E);\
[g][o1]overlay=enable='between(t,$T1S,$T1E)'[a];[a][o2]overlay=enable='between(t,$T2S,$T2E)'[b];[b][o3]overlay=enable='between(t,$T3S,$T3E)',format=yuv420p[v];\
[0:a]loudnorm=I=-16:TP=-1.5:LRA=11[au]" \
  -map "[v]" -map "[au]" -c:v libx264 -crf 17 -preset slow -b:v 0 -c:a aac -b:a 256k -movflags +faststart "$OUT/MANYEON_FirstDrop_16x9.mp4"
# 3) 포트폴리오 버전: 끝에 뚝딱컷 슬레이트 1.2초
$F -loglevel error -y -loop 1 -t 1.2 -i "$SLATE" -f lavfi -t 1.2 -i anullsrc=r=48000:cl=stereo \
  -vf "scale=1920:1080,fps=24,format=yuv420p,fade=t=in:st=0:d=0.3,fade=t=out:st=0.9:d=0.3" \
  -c:v libx264 -crf 17 -c:a aac -b:a 256k "$TMP/slate.mp4"
$F -loglevel error -y -i "$OUT/MANYEON_FirstDrop_16x9.mp4" -i "$TMP/slate.mp4" \
  -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" \
  -c:v libx264 -crf 17 -preset slow -c:a aac -b:a 256k -movflags +faststart "$OUT/MANYEON_FirstDrop_portfolio_16x9.mp4"
rm -rf "$TMP"
echo "done: $OUT"
