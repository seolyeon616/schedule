"""FILM04 SEASON NOTE × ONDO — 사계절 룩북 9:16 조립.

컷(s0~s6)을 '휘감기 블러(hblur)' 전환으로 잇고, 계절 자막·엔딩 로고를 얹고,
120bpm 패션 비트(직접 합성)와 전환 '휙' 소리를 믹스한다.

usage: python3 film04_lookbook.py <cuts_dir> <overlay_dir> <out.mp4>
cuts: s0(스튜디오) s1(봄) s2(여름) s3(가을) s4(겨울) s5(스튜디오 엔딩) s6(흐려지는 로고 배경) .mov
"""
import os
import re
import subprocess
import sys
import tempfile
import wave

import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

F = os.environ.get("FFMPEG", "ffmpeg")
cuts, ovdir, out = [os.path.abspath(p) for p in sys.argv[1:4]]
SEGS = ["s0", "s1", "s2", "s3", "s4", "s5", "s6"]
XF = 0.22                       # 휘감기 전환 길이
WHIP = {1, 2, 3, 4, 5}          # 이 컷으로 들어올 때 hblur 전환 (s6은 그냥 디졸브)
SR = 48000
rng = np.random.default_rng(11)


def dur(p):
    r = subprocess.run([F, "-i", p], capture_output=True, text=True)
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def run(a):
    subprocess.run([F, "-loglevel", "error", "-y", *a], check=True)


tmp = tempfile.mkdtemp()
d = [dur(os.path.join(cuts, s + ".mov")) for s in SEGS]
starts, t = [0.0], d[0]
for i in range(1, len(SEGS)):
    t -= XF
    starts.append(t)
    t += d[i]
TOTAL = t
cuts_t = starts[1:]
print("total", round(TOTAL, 2), "cuts", [round(x, 2) for x in cuts_t])

# ---------- 1) 영상 잇기 (xfade) ----------
inp, fc = [], []
for s in SEGS:
    inp += ["-i", os.path.join(cuts, s + ".mov")]
last_v, last_a, acc = "0:v", "0:a", d[0]
for i in range(1, len(SEGS)):
    tr = "hblur" if i in WHIP else "fade"
    off = acc - XF
    fc.append(f"[{last_v}][{i}:v]xfade=transition={tr}:duration={XF}:offset={off:.3f}[xv{i}]")
    fc.append(f"[{last_a}][{i}:a]acrossfade=d={XF}[xa{i}]")
    last_v, last_a = f"xv{i}", f"xa{i}"
    acc = off + d[i]
body = os.path.join(tmp, "body.mov")
run([*inp, "-filter_complex", ";".join(fc), "-map", f"[{last_v}]", "-map", f"[{last_a}]",
     "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", body])

# ---------- 2) 120bpm 패션 비트 ----------
N = int((TOTAL + .5) * SR)
mix = np.zeros((N, 2))
beat = 0.5


def put(sig, t0, g, pan=0.0):
    i = int(t0 * SR)
    if i >= N or i < 0:
        return
    sig = sig[:N - i]
    mix[i:i + len(sig), 0] += sig * g * (1 - pan)
    mix[i:i + len(sig), 1] += sig * g * (1 + pan)


def kick():
    tt = np.arange(int(.35 * SR)) / SR
    f = 50 + 90 * np.exp(-tt * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)


def hat(dur=.06):
    n = rng.standard_normal(int(dur * SR))
    sos = butter(2, 7000, "high", fs=SR, output="sos")
    return sosfilt(sos, n) * np.exp(-np.arange(len(n)) / SR * 60)


def clap():
    n = rng.standard_normal(int(.18 * SR))
    sos = butter(2, [900, 3500], "band", fs=SR, output="sos")
    return sosfilt(sos, n) * np.exp(-np.arange(len(n)) / SR * 22)


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def pluck(m, dur=.4, br=1.0):
    tt = np.arange(int(dur * SR)) / SR
    f = hz(m)
    s = sum((1 / k) * np.sin(2 * np.pi * f * k * tt) * np.exp(-tt * (6 + 5 * k / br)) for k in range(1, 6))
    return s * np.minimum(1, tt / .003)


def bass(m, dur=.45):
    tt = np.arange(int(dur * SR)) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * tt) + .3 * np.sin(2 * np.pi * 2 * f * tt)
    return s * np.exp(-tt * 3) * np.minimum(1, tt / .005)


def whoosh(dur=.45):
    n = rng.standard_normal(int(dur * SR))
    tt = np.arange(len(n)) / SR
    out_ = np.zeros_like(n)
    for k, fc_ in enumerate(np.linspace(800, 6000, 8)):
        sos = butter(2, [fc_ * .7, fc_ * 1.3], "band", fs=SR, output="sos")
        seg = sosfilt(sos, n)
        w = np.exp(-((tt / dur - k / 8) ** 2) / .01)
        out_ += seg * w
    return out_ * np.sin(np.pi * tt / dur) ** 2


prog = [(60, [64, 67, 72]), (55, [62, 67, 71]), (57, [64, 69, 72]), (53, [65, 69, 72])]  # C G Am F
T_END = starts[6]                       # 로고 카드부터 비트 멈춤
b = 0
while b * beat < T_END:
    tb = b * beat
    bar = (b // 4) % 4
    root, ch = prog[bar]
    if tb >= starts[1] - .5:            # 첫 회전 직전에 드럼 인
        put(kick(), tb, .9)
        if b % 2 == 1:
            put(clap(), tb, .35, .1)
        put(hat(), tb + beat / 2, .18, .3)
        put(bass(root - 24), tb, .45)
    else:
        put(hat(.04), tb + beat / 2, .08, .3)
    for j, m in enumerate(ch):
        put(pluck(m + (12 if b % 2 else 0)), tb + j * .06 * (b % 2), .16, -.3 + .3 * j)
    b += 1
for ct in cuts_t[:5]:
    put(whoosh(), ct - .25, .35)
for j, m in enumerate([72, 76, 79, 84]):
    put(pluck(m, 2.5, 2.0), T_END + j * .08, .22, -.2 + .15 * j)
ir = rng.standard_normal(int(1.2 * SR)) * np.exp(-np.arange(int(1.2 * SR)) / SR * 5)
ir /= np.sqrt((ir ** 2).sum())
mix = mix * .85 + np.stack([fftconvolve(mix[:, c], ir)[:N] for c in range(2)], 1) * .25
fo = int(1.2 * SR)
mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
mix /= np.max(np.abs(mix)) / .85
bgm = os.path.join(tmp, "bgm.wav")
with wave.open(bgm, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())

# ---------- 3) 자막·로고 합성 ----------
OV = [("intro", .2, starts[1] - .05), ("spring", starts[1] + .25, starts[2] - .05),
      ("summer", starts[2] + .25, starts[3] - .05), ("autumn", starts[3] + .25, starts[4] - .05),
      ("winter", starts[4] + .25, starts[5] - .05), ("endlogo", starts[6] + .3, TOTAL)]
inputs = ["-i", body, "-i", bgm]
fc = ["[0:v]eq=saturation=1.03:contrast=1.02,curves=all='0/0.02 1/1',format=yuv420p[v0]"]
last = "v0"
for i, (png, st, en) in enumerate(OV):
    inputs += ["-loop", "1", "-t", f"{TOTAL:.3f}", "-i", os.path.join(ovdir, png + ".png")]
    k = i + 2
    fc.append(f"[{k}:v]format=rgba,fade=t=in:st={st:.3f}:d=0.25:alpha=1,fade=t=out:st={en - .2:.3f}:d=0.2:alpha=1[o{i}]")
    fc.append(f"[{last}][o{i}]overlay=enable='between(t,{st:.3f},{en:.3f})'[v{i + 1}]")
    last = f"v{i + 1}"
fc.append(f"[{last}]fade=t=in:st=0:d=0.25,fade=t=out:st={TOTAL - .4:.3f}:d=0.4,format=yuv420p[vout]")
fc.append("[0:a]volume=0.35[sfx]")
fc.append(f"[1:a]atrim=0:{TOTAL:.3f},volume=0.9[bg]")
fc.append("[sfx][bg]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[aout]")
run([*inputs, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-t", f"{TOTAL:.3f}",
     "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-maxrate", "16M", "-bufsize", "24M",
     "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", out])
print("done", out, round(dur(out), 2))
