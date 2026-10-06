"""FILM06 LIFT × 온결 피부과(가상) — HIFU 리프팅 9:16 조립.

모든 컷을 '위로' 향하는 움직임으로 잇는다: 위로 밀리는 전환(smoothup)과 하얀 빛 전환(fadewhite),
창빛 속에 위로 떠오르는 빛 입자, 맑은 피아노 + 패드 BGM(직접 합성), 엔딩 로고와 부작용 고지.

usage: python3 film06_lift.py <uploads_dir> <overlay_dir> <out.mp4>
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
SR, FPS, W, H = 48000, 24, 1080, 1920
rng = np.random.default_rng(6)

# (이름, 파일 id, 시작, 끝)
SEGS = [
    ("l1", "52d44ede", 1.0, 3.4),    # 창유리 물방울이 위로
    ("l2", "a9fde502", 1.6, 4.0),    # 처진 커튼이 위로
    ("l3", "5cb2783d", 1.2, 3.8),    # 옆모습, 턱을 들고 머리카락이 위로
    ("l4a", "eed813f8", 3.4, 5.4),   # 장비 히어로
    ("l4b", "e329b486", 2.8, 5.6),   # 시술: 턱선 빛점 → 위로
    ("l5", "61b2f8de", 3.2, 8.0),    # 눈 뜨고 미소 → 흐려지며 로고
]
# 들어오는 컷마다 전환 (종류, 길이)
TRANS = [None, ("smoothup", .35), ("fadewhite", .45), ("smoothup", .35), ("fade", .30), ("fadewhite", .45)]
END_AT = 2.5                     # l5 안에서 엔딩 카드가 시작되는 시점


def dur(p):
    r = subprocess.run([F, "-i", p], capture_output=True, text=True)
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def run(a, **kw):
    subprocess.run([F, "-loglevel", "error", "-y", *a], check=True, **kw)


def src(fid):
    return glob.glob(os.path.join(up, fid + "*.mp4"))[0]


tmp = tempfile.mkdtemp()
GRADE = (f"scale={W}:{H}:flags=lanczos,eq=contrast=1.02:saturation=0.92:gamma=1.02,"
         "colorbalance=rs=-0.02:bs=0.03:rh=0.01:bh=-0.01,curves=all='0/0.04 0.5/0.52 1/0.98'")

# ---------- 1) 컷 다듬기 ----------
parts, lens = [], []
for name, fid, a, b in SEGS:
    n = round((b - a) * FPS)
    p = os.path.join(tmp, name + ".mov")
    if name == "l5":   # 엔딩: 같은 장면 위에 흐림을 천천히 덮는다
        fc = (f"[0:v]fps={FPS},{GRADE},split[s][bl];[bl]gblur=sigma=34:steps=2,eq=brightness=0.05,format=rgba,"
              f"fade=t=in:st={END_AT}:d=0.7:alpha=1[blur];[s][blur]overlay,format=yuv420p,setsar=1[v]")
    else:
        fc = f"[0:v]fps={FPS},{GRADE},format=yuv420p,setsar=1[v]"
    run(["-ss", f"{a}", "-t", f"{b - a}", "-i", src(fid), "-filter_complex", fc, "-map", "[v]", "-map", "0:a",
         "-af", "aresample=48000", "-frames:v", str(n), "-c:v", "libx264", "-crf", "12", "-preset", "medium",
         "-c:a", "pcm_s16le", "-ac", "2", p])
    parts.append(p)
    lens.append(n / FPS)

# ---------- 2) 전환으로 잇기 ----------
starts, acc = [0.0], lens[0]
inp, fc = [], []
for p in parts:
    inp += ["-i", p]
lv, la = "0:v", "0:a"
for i in range(1, len(parts)):
    kind, xd = TRANS[i]
    off = acc - xd
    starts.append(off)
    fc.append(f"[{lv}][{i}:v]xfade=transition={kind}:duration={xd}:offset={off:.3f}[xv{i}]")
    fc.append(f"[{la}][{i}:a]acrossfade=d={xd}[xa{i}]")
    lv, la = f"xv{i}", f"xa{i}"
    acc = off + lens[i]
TOTAL = acc
print("total", round(TOTAL, 2), "starts", [round(x, 2) for x in starts])
body = os.path.join(tmp, "body.mov")
run([*inp, "-filter_complex", ";".join(fc), "-map", f"[{lv}]", "-map", f"[{la}]",
     "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", body])
st = {s[0]: starts[i] for i, s in enumerate(SEGS)}
en = {s[0]: (starts[i + 1] + TRANS[i + 1][1] / 2 if i + 1 < len(SEGS) else TOTAL) for i, s in enumerate(SEGS)}

# ---------- 3) 위로 떠오르는 빛 입자 (L3, L5 구간) ----------
pw, ph = W // 2, H // 2
NP = 46
px = rng.uniform(0, pw, NP)
py = rng.uniform(0, ph, NP)
depth = rng.uniform(0, 1, NP)                  # 0=멀리(작고 또렷) 1=가까이(크고 흐림)
spd = 8 + 30 * depth
size = 1.0 + 5.5 * depth ** 2
amp = .16 + .30 * (1 - depth) * rng.uniform(.6, 1, NP)
ph0 = rng.uniform(0, 2 * np.pi, NP)
yy, xx = np.mgrid[0:ph, 0:pw]
windows = [(st["l3"] + .2, en["l3"]), (st["l5"], st["l5"] + END_AT + .4)]


def env(t):
    v = 0.0
    for a, b in windows:
        if a <= t <= b:
            v = max(v, min(1, (t - a) / .5, (b - t) / .5))
    return v


part = os.path.join(tmp, "motes.mov")
nf = int(TOTAL * FPS) + 1
proc = subprocess.Popen([F, "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{pw}x{ph}",
                         "-r", str(FPS), "-i", "-", "-vf", f"scale={W}:{H}", "-c:v", "qtrle", part],
                        stdin=subprocess.PIPE)
for k in range(nf):
    t = k / FPS
    e = env(t)
    a = np.zeros((ph, pw), np.float32)
    if e > 0:
        y = (py - spd * t) % (ph + 40) - 20
        x = px + 6 * np.sin(t * .7 + ph0)
        for j in range(NP):
            r = int(size[j] * 3) + 2
            x0, x1 = int(max(0, x[j] - r)), int(min(pw, x[j] + r + 1))
            y0, y1 = int(max(0, y[j] - r)), int(min(ph, y[j] + r + 1))
            if x0 >= x1 or y0 >= y1:
                continue
            d2 = (xx[y0:y1, x0:x1] - x[j]) ** 2 + (yy[y0:y1, x0:x1] - y[j]) ** 2
            tw = .75 + .25 * np.sin(t * 2.3 + ph0[j])
            a[y0:y1, x0:x1] += amp[j] * tw * np.exp(-d2 / (2 * size[j] ** 2))
    a = np.clip(a * e, 0, 1)
    rgba = np.empty((ph, pw, 4), np.uint8)
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = 255, 252, 240
    rgba[..., 3] = (a * 255).astype(np.uint8)
    proc.stdin.write(rgba.tobytes())
proc.stdin.close()
proc.wait()

# ---------- 4) 맑은 피아노 + 패드 BGM (72bpm) ----------
N = int((TOTAL + .5) * SR)
mix = np.zeros((N, 2))
beat = 60 / 72


def put(sig, t0, g, pan=0.0):
    i = int(t0 * SR)
    if i >= N or i < 0:
        return
    sig = sig[:N - i]
    mix[i:i + len(sig), 0] += sig * g * (1 - pan)
    mix[i:i + len(sig), 1] += sig * g * (1 + pan)


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def piano(m, d=2.6):
    tt = np.arange(int(d * SR)) / SR
    f = hz(m)
    s = sum((.6 ** (k - 1)) * np.sin(2 * np.pi * f * k * tt * (1 + .0004 * k * k)) * np.exp(-tt * (1.3 + .9 * k))
            for k in range(1, 7))
    ham = rng.standard_normal(int(.01 * SR)) * np.linspace(1, 0, int(.01 * SR)) * .15
    s[:len(ham)] += ham
    return s * np.minimum(1, tt / .003)


def pad(ms, d):
    tt = np.arange(int(d * SR)) / SR
    s = np.zeros_like(tt)
    for m in ms:
        for det in (-.12, .12):
            ph_ = 2 * np.pi * hz(m + det) * tt
            s += np.sin(ph_) + .3 * np.sin(2 * ph_) + .12 * np.sin(3 * ph_)
    s = sosfilt(butter(2, 1800, "low", fs=SR, output="sos"), s)
    envl = np.minimum(1, tt / .8) * np.minimum(1, (d - tt) / .8)
    return s * envl / (len(ms) * 2)


def riser(d=.9):
    n = rng.standard_normal(int(d * SR))
    tt = np.arange(len(n)) / SR
    o = np.zeros_like(n)
    for k, fc_ in enumerate(np.geomspace(600, 7000, 10)):
        seg = sosfilt(butter(2, [fc_ * .75, fc_ * 1.3], "band", fs=SR, output="sos"), n)
        o += seg * np.exp(-((tt / d - k / 10) ** 2) / .012)
    return o * np.sin(np.pi * tt / d) ** 2


prog = [([48, 55, 59, 62, 64], [60, 64, 67, 71, 74]),     # Cmaj9
        ([45, 52, 55, 60, 64], [57, 60, 64, 67, 71]),     # Am9
        ([41, 48, 52, 57, 60], [53, 57, 60, 64, 67]),     # Fmaj9
        ([43, 50, 55, 57, 62], [55, 59, 62, 64, 69])]     # G6/9
T_END = st["l5"] + END_AT
bar_len = 4 * beat
nb = int(np.ceil(T_END / bar_len))
for bi in range(nb):
    t0 = bi * bar_len
    low, arp = prog[bi % 4]
    put(pad(low[1:4], bar_len + .9), t0, .22)
    put(piano(low[0] - 12, 3.5), t0, .30)
    for j in range(8):                                   # 위로 오르는 8분 아르페지오
        tj = t0 + j * beat / 2
        if tj < T_END - .1:
            m = arp[j % 5] + (12 if j >= 5 else 0)
            put(piano(m, 1.8), tj, .15 if j else .2, -.3 + .08 * j)
for j, m in enumerate([60, 64, 67, 71, 74, 79, 84]):      # 엔딩 Cmaj9 펼침
    put(piano(m, 4.0), T_END + j * .09, .2, -.3 + .1 * j)
put(pad([48, 55, 64, 71], TOTAL - T_END + 1), T_END - .2, .25)
for name in ("l2", "l4a"):
    put(riser(), st[name] - .55, .30)
for name in ("l3", "l5"):
    put(riser(.7), st[name] - .45, .22)
ir = rng.standard_normal(int(2.2 * SR)) * np.exp(-np.arange(int(2.2 * SR)) / SR * 2.6)
ir /= np.sqrt((ir ** 2).sum())
mix = mix * .78 + np.stack([fftconvolve(mix[:, c], ir)[:N] for c in range(2)], 1) * .34
mix = sosfilt(butter(2, 40, "high", fs=SR, output="sos"), mix, axis=0)
fo = int(1.4 * SR)
mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
mix /= np.max(np.abs(mix)) / .85
bgm = os.path.join(tmp, "bgm.wav")
with wave.open(bgm, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())

# ---------- 5) 합성: 블룸 · 입자 · 자막 · 로고 ----------
OV = [("c1", st["l1"] + .25, en["l1"]), ("c2", st["l2"] + .3, en["l2"]), ("c3", st["l3"] + .45, en["l3"]),
      ("c4", st["l4a"] + .25, en["l4a"]), ("c5", st["l4b"] + .35, en["l4b"]),
      ("c6", st["l5"] + .5, st["l5"] + END_AT - .05), ("endlogo", st["l5"] + END_AT + .25, TOTAL)]
inputs = ["-i", body, "-i", bgm, "-i", part]
fc = ["[0:v]split[b0][b1];[b1]gblur=sigma=22,format=gbrp[bb];[b0]format=gbrp[bs];"
      "[bs][bb]blend=all_mode=screen:all_opacity=0.12,format=yuv420p[g]",
      "[2:v]format=rgba[pt]", "[g][pt]overlay=format=auto[v0]"]
last = "v0"
for i, (png, a, b) in enumerate(OV):
    inputs += ["-loop", "1", "-t", f"{TOTAL:.3f}", "-i", os.path.join(ovdir, png + ".png")]
    k = i + 3
    fc.append(f"[{k}:v]format=rgba,fade=t=in:st={a:.3f}:d=0.35:alpha=1,fade=t=out:st={b - .25:.3f}:d=0.25:alpha=1[o{i}]")
    fc.append(f"[{last}][o{i}]overlay=enable='between(t,{a:.3f},{b:.3f})'[v{i + 1}]")
    last = f"v{i + 1}"
fc.append(f"[{last}]noise=alls=3:allf=t,fade=t=in:st=0:d=0.25,fade=t=out:st={TOTAL - .45:.3f}:d=0.45,format=yuv420p[vout]")
fc.append("[0:a]volume=0.35[sfx]")
fc.append(f"[1:a]atrim=0:{TOTAL:.3f},volume=0.9[bg]")
fc.append("[sfx][bg]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[aout]")
run([*inputs, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-t", f"{TOTAL:.3f}",
     "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-maxrate", "16M", "-bufsize", "24M",
     "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", out])
print("done", out, round(dur(out), 2))
