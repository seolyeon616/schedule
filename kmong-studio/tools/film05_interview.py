"""FILM05 GRWM × MULGYUL — 매거진 뷰티 인터뷰 스타일 9:16 조립.

하드컷 + 인터뷰식 점프컷(같은 컷 안에서 살짝 확대), 에디토리얼 그레이드·필름 그레인,
Q(질문) → A(대답) 자막, 잔잔한 재즈 피아노 BGM(직접 합성)과 셔터 소리.

usage: python3 film05_interview.py <uploads_dir> <overlay_dir> <out.mp4>
"""
import glob
import os
import re
import subprocess
import sys
import tempfile
import wave

import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

F = os.environ.get("FFMPEG", "ffmpeg")
up, ovdir, out = [os.path.abspath(p) for p in sys.argv[1:4]]
SR, FPS = 48000, 24
rng = np.random.default_rng(5)

# (이름, 파일 id, 시작, 끝, 줌 시작, 줌 끝)
SEGS = [
    ("g1", "81cc241a", 0.3, 3.0, 1.00, 1.03),   # 손 인사 + 타이틀
    ("g2a", "8102e669", 0.2, 1.7, 1.00, 1.02),  # 앰플 기울이기 (질문)
    ("g2b", "8102e669", 5.6, 7.6, 1.10, 1.12),  # 카메라 보며 미소 (대답, 점프컷)
    ("g3", "c105f591", 0.0, 2.6, 1.00, 1.04),   # 손등에 한 방울
    ("g4a", "0e83542a", 0.3, 2.1, 1.00, 1.02),  # 볼 톡톡 (질문)
    ("g4b", "0e83542a", 5.2, 7.2, 1.10, 1.12),  # 거울 보며 미소 (대답, 점프컷)
    ("g5", "fe92c77d", 3.0, 5.6, 1.00, 1.04),   # 제품 히어로
    ("g6a", "814daa9c", 0.0, 3.4, 1.00, 1.03),  # 윙크 → 미소
    ("g6b", "814daa9c", 8.4, 10.0, 1.00, 1.02), # 문 열고 나감
]
END = 2.8                                       # 흐린 엔딩 로고 카드
SCENE_CUTS = {1, 3, 4, 6, 7, 9}                 # 장면이 바뀌는 컷 (셔터 소리)


def dur(p):
    r = subprocess.run([F, "-i", p], capture_output=True, text=True)
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def run(a):
    subprocess.run([F, "-loglevel", "error", "-y", *a], check=True)


def src(fid):
    return glob.glob(os.path.join(up, fid + "*.mp4"))[0]


tmp = tempfile.mkdtemp()
GRADE = ("eq=contrast=1.04:saturation=0.94:gamma=1.02,"
         "colorbalance=rh=0.03:gh=0.01:bh=-0.03:rs=0.01:bs=0.02,"
         "curves=all='0/0.03 0.5/0.5 1/0.98',unsharp=5:5:0.5")

# ---------- 1) 컷 다듬기 (천천히 밀어 들어가는 줌) ----------
parts, starts, t = [], [], 0.0
for name, fid, a, b, z0, z1 in SEGS:
    n = round((b - a) * FPS)
    p = os.path.join(tmp, name + ".mov")
    vf = (f"fps={FPS},scale=2160:3840,zoompan=z='{z0}+({z1}-{z0})*in/{n}':d=1:"
          f"x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':s=1080x1920:fps={FPS},{GRADE},setsar=1")
    run(["-ss", f"{a}", "-t", f"{b - a}", "-i", src(fid), "-vf", vf, "-af", "aresample=48000",
         "-frames:v", str(n), "-c:v", "libx264", "-crf", "12", "-preset", "medium",
         "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ac", "2", p])
    starts.append(t)
    parts.append(p)
    t += n / FPS
# 엔딩: 마지막 프레임을 멈추고 흐리게
last = os.path.join(tmp, "last.png")
run(["-sseof", "-0.1", "-i", parts[-1], "-frames:v", "1", "-update", "1", last])
endp = os.path.join(tmp, "end.mov")
run(["-loop", "1", "-t", f"{END}", "-i", last, "-f", "lavfi", "-t", f"{END}", "-i", "anullsrc=r=48000:cl=stereo",
     "-filter_complex", f"[0:v]fps={FPS},split[a][b];[b]gblur=sigma=32:steps=2,eq=brightness=0.03,format=rgba,"
     "fade=t=in:st=0:d=0.7:alpha=1[bl];[a][bl]overlay,format=yuv420p[v]", "-map", "[v]", "-map", "1:a",
     "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-c:a", "pcm_s16le", endp])
starts.append(t)
parts.append(endp)
TOTAL = t + END
print("total", round(TOTAL, 2), "starts", [round(x, 2) for x in starts])

lst = os.path.join(tmp, "list.txt")
with open(lst, "w") as f:
    f.writelines(f"file '{p}'\n" for p in parts)
body = os.path.join(tmp, "body.mov")
run(["-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "12", "-preset", "medium",
     "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", body])

# ---------- 2) 재즈 피아노 BGM (84bpm, Gm9-C13-Fmaj9-Dm9) ----------
N = int((TOTAL + .5) * SR)
mix = np.zeros((N, 2))
beat = 60 / 84


def put(sig, t0, g, pan=0.0):
    i = int(t0 * SR)
    if i >= N or i < 0:
        return
    sig = sig[:N - i]
    mix[i:i + len(sig), 0] += sig * g * (1 - pan)
    mix[i:i + len(sig), 1] += sig * g * (1 + pan)


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def rhodes(m, d=2.4):
    tt = np.arange(int(d * SR)) / SR
    f = hz(m)
    s = (np.sin(2 * np.pi * f * tt + .6 * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 4))
         + .25 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt * 3)
         + .08 * np.sin(2 * np.pi * 7 * f * tt) * np.exp(-tt * 18))
    trem = 1 + .12 * np.sin(2 * np.pi * 4.5 * tt)
    return s * trem * np.exp(-tt * 1.1) * np.minimum(1, tt / .004)


def bass(m, d=.7):
    tt = np.arange(int(d * SR)) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * tt) + .25 * np.sin(2 * np.pi * 2 * f * tt)
    return s * np.exp(-tt * 3.5) * np.minimum(1, tt / .01)


def brush(d=.12, g=1.0):
    n = rng.standard_normal(int(d * SR))
    sos = butter(2, [3000, 9000], "band", fs=SR, output="sos")
    return sosfilt(sos, n) * np.exp(-np.arange(len(n)) / SR * 30) * g


def kick():
    tt = np.arange(int(.3 * SR)) / SR
    return np.sin(2 * np.pi * np.cumsum(45 + 60 * np.exp(-tt * 35)) / SR) * np.exp(-tt * 12)


def shutter():
    n = rng.standard_normal(int(.09 * SR))
    sos = butter(2, [1500, 7000], "band", fs=SR, output="sos")
    c = sosfilt(sos, n) * np.exp(-np.arange(len(n)) / SR * 80)
    c2 = np.zeros(int(.16 * SR))
    c2[:len(c)] += c
    c2[int(.055 * SR):int(.055 * SR) + len(c)] += c * .6
    return c2


prog = [(43, [58, 62, 65, 69]), (36, [58, 62, 64, 69]), (41, [57, 60, 64, 67]), (38, [57, 60, 64, 65])]
T_END = starts[-1]
b = 0
while b * beat < T_END:
    tb = b * beat
    bar = (b // 4) % 4
    root, ch = prog[bar]
    if b % 4 == 0:
        for j, m in enumerate(ch):
            put(rhodes(m), tb + j * .018, .11, -.25 + .17 * j)
    if b % 4 == 2:
        for j, m in enumerate(ch[1:]):
            put(rhodes(m + 12, 1.2), tb + beat * .66, .05, .2)
    put(bass(root if b % 2 == 0 else root + 7), tb, .30)
    if tb >= starts[1] - .1:
        if b % 2 == 0:
            put(kick(), tb, .35)
        put(brush(), tb, .10, .3)
        put(brush(.08), tb + beat * .66, .07, .35)        # 스윙
    b += 1
for j, m in enumerate([53, 57, 60, 64, 67, 72]):        # 엔딩 Fmaj9
    put(rhodes(m, 3.5), T_END + j * .05, .12, -.25 + .1 * j)
put(bass(29, 2.5), T_END, .3)
for i in SCENE_CUTS:
    put(shutter(), starts[i] - .02, .55, .1)
crackle = (rng.random(N) < 6 / SR) * rng.standard_normal(N) * .25
mix += np.stack([crackle, crackle], 1) * .2
ir = rng.standard_normal(int(1.4 * SR)) * np.exp(-np.arange(int(1.4 * SR)) / SR * 4)
ir /= np.sqrt((ir ** 2).sum())
mix = mix * .82 + np.stack([fftconvolve(mix[:, c], ir)[:N] for c in range(2)], 1) * .28
lp = butter(2, 9000, "low", fs=SR, output="sos")
mix = sosfilt(lp, mix, axis=0)
fo = int(1.3 * SR)
mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
mix /= np.max(np.abs(mix)) / .85
bgm = os.path.join(tmp, "bgm.wav")
with wave.open(bgm, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())

# ---------- 3) 자막 합성 (Q 먼저, 점프컷에 A) ----------
s = starts
OV = [("title", s[0] + .25, s[1], True),
      ("q1", s[1] + .1, s[2], True), ("qa1", s[2], s[3], False),
      ("step", s[3] + .2, s[4], True),
      ("q2", s[4] + .1, s[5], True), ("qa2", s[5], s[6], False),
      ("credit", s[6] + .3, s[7], True),
      ("q3", s[7] + .2, s[7] + 1.8, True), ("qa3", s[7] + 1.8, s[8] + 1.0, False),
      ("endlogo", s[9] + .35, TOTAL, True)]
inputs = ["-i", body, "-i", bgm]
fc = ["[0:v]noise=alls=5:allf=t,format=yuv420p[v0]"]
lastv = "v0"
for i, (png, st, en, fade_in) in enumerate(OV):
    inputs += ["-loop", "1", "-t", f"{TOTAL:.3f}", "-i", os.path.join(ovdir, png + ".png")]
    k = i + 2
    fi = f"fade=t=in:st={st:.3f}:d=0.2:alpha=1," if fade_in else ""
    fo_ = f"fade=t=out:st={en - .15:.3f}:d=0.15:alpha=1" if png.startswith(("qa", "title", "step", "credit", "endlogo")) else "null"
    fc.append(f"[{k}:v]format=rgba,{fi}{fo_}[o{i}]")
    fc.append(f"[{lastv}][o{i}]overlay=enable='between(t,{st:.3f},{en:.3f})'[v{i + 1}]")
    lastv = f"v{i + 1}"
fc.append(f"[{lastv}]fade=t=in:st=0:d=0.2,fade=t=out:st={TOTAL - .4:.3f}:d=0.4,format=yuv420p[vout]")
fc.append("[0:a]volume=0.30[sfx]")
fc.append(f"[1:a]atrim=0:{TOTAL:.3f},volume=0.9[bg]")
fc.append("[sfx][bg]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[aout]")
run([*inputs, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-t", f"{TOTAL:.3f}",
     "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-maxrate", "16M", "-bufsize", "24M",
     "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", out])
print("done", out, round(dur(out), 2))
