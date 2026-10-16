"""MANYEON FILM01 v2 조립: 컷 9개 + 장면 자막 + 대형 워드마크 + 엔드 로고 + BGM.

usage: python3 assemble_film01_v2.py <cuts_dir> <overlay_dir> <bgm.wav> <out.mp4> [--slate]
FFMPEG 환경변수로 ffmpeg 경로 지정 가능.
"""
import os
import re
import subprocess
import sys
import tempfile

F = os.environ.get("FFMPEG", "ffmpeg")
cuts, ovdir, bgm, out = sys.argv[1:5]
with_slate = "--slate" in sys.argv

# (파일, 영상 필터 추가분, 오디오 필터 추가분) — #6 도시 유리창은 v2에서 제외
CLIPS = [
    ("01_drop-hook", "fade=t=in:st=0:d=0.5", ""),
    ("02_into-droplet", "", ""),
    ("03_glacier-drop", "", ""),
    ("04_waterfall-dive", "", "afade=t=out:st={end_012}:d=0.12"),
    ("05_fern-dew", "", "volume=0:enable='lt(t,0.3)',afade=t=in:st=0.3:d=0.4"),
    ("07_woman-window", "", ""),
    ("08_serum-drop", "", ""),
    ("09x_hero-bottle-long", "fade=t=out:st={end_035}:d=0.35", "afade=t=out:st={end_035}:d=0.35"),
    ("10_ripple-end", "fade=t=in:st=0:d=0.35", ""),
]

# (오버레이 PNG, 시작, 끝, 페이드) — 타임라인 초
OVERLAYS = [
    ("c1", 3.5, 6.7, 0.5),
    ("c2", 7.5, 10.8, 0.5),
    ("c3", 11.5, 14.8, 0.5),
    ("c4", 15.6, 18.8, 0.5),
    ("c5", 19.6, 23.1, 0.5),
    ("c6", 24.4, 28.9, 0.5),
    ("giant", 30.0, 35.3, 0.7),
    ("c7", 38.2, 40.5, 0.5),
    ("endlogo", 40.8, None, 0.6),  # None = 영상 끝까지
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
    for name, vx, ax in CLIPS:
        src = os.path.join(cuts, name + "_CUT.mp4")
        d = dur(src)
        fmt = {"end_012": f"{d - 0.12:.3f}", "end_035": f"{d - 0.35:.3f}"}
        vf = ",".join(x for x in ["scale=1920:1080,fps=24,format=yuv420p", vx.format(**fmt)] if x)
        af = ",".join(x for x in ["aresample=48000,aformat=channel_layouts=stereo", ax.format(**fmt)] if x)
        dst = os.path.join(tmp, name + ".mov")
        has_audio = "Audio:" in subprocess.run([F, "-i", src], capture_output=True, text=True).stderr
        if has_audio:
            run(["-i", src, "-vf", vf, "-af", af, "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-c:a", "pcm_s16le", dst])
        else:
            run(["-i", src, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-vf", vf, "-shortest",
                 "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-c:a", "pcm_s16le", dst])
        fl.write(f"file '{dst}'\n")
body = os.path.join(tmp, "body.mov")
run(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", body])
total = dur(body)

inputs = ["-i", body, "-i", bgm]
fc = ["[0:v]eq=saturation=0.9:contrast=0.97,curves=all='0/0.025 1/1',noise=alls=3:allf=t[v0]"]
last = "v0"
for i, (png, st, en, fd) in enumerate(OVERLAYS):
    en = total if en is None else en
    inputs += ["-loop", "1", "-t", f"{total:.3f}", "-i", os.path.join(ovdir, png + ".png")]
    k = i + 2
    fc.append(f"[{k}:v]format=rgba,fade=t=in:st={st}:d={fd}:alpha=1,fade=t=out:st={en - fd:.3f}:d={fd}:alpha=1[o{i}]")
    fc.append(f"[{last}][o{i}]overlay=enable='between(t,{st},{en:.3f})'[v{i + 1}]")
    last = f"v{i + 1}"
fc.append(f"[{last}]fade=t=out:st={total - 0.5:.3f}:d=0.5,format=yuv420p[vout]")
# 효과음(영상 소리) + BGM. 효과음이 주인공, BGM은 아래에.
fc.append("[0:a]volume=1.0[sfx]")
fc.append(f"[1:a]atrim=0:{total:.3f},volume=0.62,afade=t=out:st={total - 1.5:.3f}:d=1.5[bg]")
fc.append("[sfx][bg]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[aout]")
main = out if not with_slate else os.path.join(tmp, "main.mp4")
run([*inputs, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-t", f"{total:.3f}",
     "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
     "-movflags", "+faststart", main])

if with_slate:
    slate = os.path.join(tmp, "slate.mp4")
    run(["-loop", "1", "-t", "1.2", "-i", os.path.join(ovdir, "slate.png"), "-f", "lavfi", "-t", "1.2", "-i",
         "anullsrc=r=48000:cl=stereo", "-vf", "scale=1920:1080,fps=24,format=yuv420p,fade=t=in:st=0:d=0.3,fade=t=out:st=0.9:d=0.3",
         "-c:v", "libx264", "-crf", "17", "-c:a", "aac", "-b:a", "256k", slate])
    run(["-i", main, "-i", slate, "-filter_complex", "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out])
print("done", out, round(dur(out), 2), "s")
