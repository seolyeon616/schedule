"""MANYEON FILM01 9:16 숏폼(약 15초) 조립.

16:9 컷에서 세로로 잘라(피사체 위치에 맞춰 가로 위치 지정) 1080x1920으로 키우고,
숏폼 전용 자막·대형 워드마크·엔드 로고와 BGM 절정 구간을 얹는다.

usage: python3 assemble_film01_short.py <cuts_dir> <overlay_dir> <bgm.wav> <out.mp4> [--frame]
  기본(crop): 세로로 잘라 꽉 채움 (1.78배 확대 → 샤프닝으로 보정)
  --frame   : 16:9 화면을 확대 없이 가운데에 두고 위아래 검은 여백 (가장 선명, 시네마 느낌)
"""
import os
import re
import subprocess
import sys
import tempfile

F = os.environ.get("FFMPEG", "ffmpeg")
cuts, ovdir, bgm, out = sys.argv[1:5]
FRAME = "--frame" in sys.argv
BGM_FROM = 19.0  # 본편 BGM의 절정 시작 지점부터 사용

# (컷 파일, 시작, 끝, 세로 크롭 중심 x(1920 기준))
SEGS = [
    ("02_into-droplet", 0.0, 2.0, 960),
    ("03_glacier-drop", 1.8, 3.3, 850),
    ("07_woman-window", 0.2, 3.2, 1130),
    ("08_serum-drop", 0.5, 4.0, 930),
    ("09x_hero-bottle-long", 0.3, 2.8, 960),
    ("10_ripple-end", 2.4, 5.4, 960),
]
# (오버레이, 시작, 끝, 페이드)
OVERLAYS = [
    ("s-c1", 0.3, 1.9, 0.3),
    ("s-c2", 2.1, 3.4, 0.3),
    ("s-c3", 3.8, 6.4, 0.4),
    ("s-c4", 6.9, 9.8, 0.4),
    ("s-giant", 10.2, 11.9, 0.4),
    ("s-end", 12.6, None, 0.5),
]


def dur(path):
    r = subprocess.run([F, "-i", path], capture_output=True, text=True)
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def run(args):
    subprocess.run([F, "-loglevel", "error", "-y", *args], check=True)


tmp = tempfile.mkdtemp()
lst = os.path.join(tmp, "list.txt")
with open(lst, "w") as fl:
    for i, (name, a, b, cx) in enumerate(SEGS):
        src = os.path.join(cuts, name + "_CUT.mp4")
        x = max(0, min(1920 - 608, cx - 304))
        if FRAME:
            vf = "scale=1080:608:flags=lanczos,pad=1080:1920:0:656:black,setsar=1,fps=24,format=yuv420p"
        else:
            vf = (f"crop=608:1080:{x}:0,scale=1080:1920:flags=lanczos,"
                  "unsharp=5:5:0.7:5:5:0.0,setsar=1,fps=24,format=yuv420p")
        if i == 0:
            vf += ",fade=t=in:st=0:d=0.25"
        dst = os.path.join(tmp, f"{i}.mov")
        run(["-ss", str(a), "-t", f"{b - a:.3f}", "-i", src, "-vf", vf,
             "-af", "aresample=48000,aformat=channel_layouts=stereo",
             "-c:v", "libx264", "-crf", "10", "-preset", "medium", "-c:a", "pcm_s16le", dst])
        fl.write(f"file '{dst}'\n")
body = os.path.join(tmp, "body.mov")
run(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", body])
total = dur(body)

inputs = ["-i", body, "-ss", str(BGM_FROM), "-i", bgm]
# 숏폼은 확대·재압축에 그레인이 뭉개지므로 노이즈를 넣지 않음
fc = ["[0:v]eq=saturation=0.9:contrast=0.97,curves=all='0/0.025 1/1'[v0]"]
last = "v0"
for i, (png, st, en, fd) in enumerate(OVERLAYS):
    en = total if en is None else en
    inputs += ["-loop", "1", "-t", f"{total:.3f}", "-i", os.path.join(ovdir, png + ".png")]
    k = i + 2
    fc.append(f"[{k}:v]format=rgba,fade=t=in:st={st}:d={fd}:alpha=1,fade=t=out:st={en - fd:.3f}:d={fd}:alpha=1[o{i}]")
    fc.append(f"[{last}][o{i}]overlay=enable='between(t,{st},{en:.3f})'[v{i + 1}]")
    last = f"v{i + 1}"
fc.append(f"[{last}]fade=t=out:st={total - 0.4:.3f}:d=0.4,format=yuv420p[vout]")
fc.append("[0:a]volume=0.8[sfx]")
fc.append(f"[1:a]atrim=0:{total:.3f},afade=t=in:st=0:d=0.3,volume=0.7,afade=t=out:st={total - 1.2:.3f}:d=1.2[bg]")
fc.append("[sfx][bg]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[aout]")
run([*inputs, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-t", f"{total:.3f}",
     "-c:v", "libx264", "-crf", "15", "-preset", "slow", "-tune", "film", "-maxrate", "20M", "-bufsize", "30M",
     "-profile:v", "high", "-level", "4.2",
     "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", out])
print("done", out, round(dur(out), 2), "s")
