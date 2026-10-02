"""FILM03 STRAWBERRY MOON × 달토끼 제과점 — 몽환 동화풍 9:16 조립.

1) 컷들을 이어 붙이고  2) 몽글몽글한 빛망울·반짝이 입자(numpy)를 생성해 스크린 합성
3) 블룸·파스텔 색보정  4) Do Hyeon 자막 / Fraunces 아치 타이틀 / 엔딩 로고
5) 오르골 BGM(직접 합성)과 효과음 믹스

usage: python3 film03_dream.py <cuts_dir> <overlay_dir> <out.mp4>
cuts_dir 안의 파일(순서대로): 01 02 03a 03b 04 05 06(엔딩 배경) .mov
"""
import os
import re
import subprocess
import sys
import tempfile
import wave

import numpy as np

F = os.environ.get("FFMPEG", "ffmpeg")
cuts, ovdir, out = [os.path.abspath(p) for p in sys.argv[1:4]]
SEGS = ["01", "02", "03a", "03b", "04", "05", "06"]
LAND_IN_04 = 2.29        # #4 컷 안에서 딸기가 착지하는 시점(초)
FLASH_IN_03A = 1.7       # #3 컷 안에서 창이 번쩍이는 시점(초)
SR = 48000
rng = np.random.default_rng(3)


def dur(p):
    r = subprocess.run([F, "-i", p], capture_output=True, text=True)
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def run(args, **kw):
    subprocess.run([F, "-loglevel", "error", "-y", *args], check=True, **kw)


tmp = tempfile.mkdtemp()
d = {s: dur(os.path.join(cuts, s + ".mov")) for s in SEGS}
start, t = {}, 0.0
for s in SEGS:
    start[s] = t
    t += d[s]
TOTAL = t
T_LAND = start["04"] + LAND_IN_04
T_FLASH = start["03a"] + FLASH_IN_03A
T_STREAK = start["02"]
print("total", round(TOTAL, 2), "land", round(T_LAND, 2), "flash", round(T_FLASH, 2))

# ---------- 1) 본편 이어 붙이기 ----------
lst = os.path.join(tmp, "list.txt")
with open(lst, "w") as fl:
    for s in SEGS:
        fl.write(f"file '{os.path.join(cuts, s + '.mov')}'\n")
body = os.path.join(tmp, "body.mov")
run(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", body])

# ---------- 2) 몽글몽글 입자 레이어 (540x960, 검정 배경 → screen 합성) ----------
W, H, FPS = 540, 960, 24
NF = int(TOTAL * FPS) + 1


def sprite(r):
    y, x = np.mgrid[-r * 2:r * 2 + 1, -r * 2:r * 2 + 1]
    g = np.exp(-(x * x + y * y) / (2 * (r * 0.7) ** 2))
    return g


def star(r):
    y, x = np.mgrid[-r:r + 1, -r:r + 1].astype(float)
    a = np.exp(-np.abs(x) / (r * 0.08)) * np.exp(-np.abs(y) / (r * 0.45))
    b = np.exp(-np.abs(y) / (r * 0.08)) * np.exp(-np.abs(x) / (r * 0.45))
    c = np.exp(-(x * x + y * y) / (2 * (r * 0.18) ** 2))
    return np.clip(a + b + c, 0, 1)


PALETTE = np.array([[255, 190, 215], [255, 225, 170], [255, 245, 235], [230, 200, 255]], float) / 255
bokeh = [dict(x=rng.uniform(0, W), y=rng.uniform(0, H), r=rng.uniform(5, 18), vy=rng.uniform(6, 22),
              ph=rng.uniform(0, 6.28), sp=rng.uniform(.3, .9), c=PALETTE[rng.integers(0, 4)],
              a=rng.uniform(.10, .30)) for _ in range(46)]
sparks = [dict(x=rng.uniform(20, W - 20), y=rng.uniform(20, H - 20), r=int(rng.uniform(7, 14)),
               ph=rng.uniform(0, 6.28), sp=rng.uniform(1.2, 2.6), c=PALETTE[rng.integers(0, 4)]) for _ in range(18)]


def burst(cx, cy, n, t0, life, spread):
    return [dict(cx=cx, cy=cy, ang=rng.uniform(0, 6.28), v=rng.uniform(.4, 1.0) * spread, t0=t0 + rng.uniform(0, .25),
                 life=life * rng.uniform(.7, 1.1), r=int(rng.uniform(6, 13)), c=PALETTE[rng.integers(0, 4)]) for _ in range(n)]


bursts = burst(270, 470, 34, T_LAND, 1.4, 260) + burst(270, 330, 22, T_FLASH, 1.1, 180)
spr_cache, star_cache = {}, {}


def add(img, s, x, y, col, a):
    h, w = s.shape
    x0, y0 = int(x) - w // 2, int(y) - h // 2
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xa >= xb or ya >= yb:
        return
    img[ya:yb, xa:xb] += s[ya - y0:yb - y0, xa - x0:xb - x0, None] * col[None, None, :] * a


ppath = os.path.join(tmp, "particles.mp4")
enc = subprocess.Popen([F, "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                        "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", ppath], stdin=subprocess.PIPE)
for i in range(NF):
    tt = i / FPS
    img = np.zeros((H, W, 3))
    for b in bokeh:
        y = (b["y"] - b["vy"] * tt) % (H + 60) - 30
        x = b["x"] + 14 * np.sin(tt * b["sp"] + b["ph"])
        r = int(b["r"])
        s = spr_cache.setdefault(r, sprite(r))
        add(img, s, x, y, b["c"], b["a"] * (0.65 + 0.35 * np.sin(tt * b["sp"] * 2 + b["ph"])))
    for s_ in sparks:
        tw = max(0.0, np.sin(tt * s_["sp"] + s_["ph"])) ** 6
        if tw > .02:
            st = star_cache.setdefault(s_["r"], star(s_["r"]))
            add(img, st, s_["x"], s_["y"], s_["c"], .9 * tw)
    for b in bursts:
        k = (tt - b["t0"]) / b["life"]
        if 0 <= k <= 1:
            dist = b["v"] * (1 - (1 - k) ** 2)
            x, y = b["cx"] + np.cos(b["ang"]) * dist, b["cy"] + np.sin(b["ang"]) * dist - 40 * k
            st = star_cache.setdefault(b["r"], star(b["r"]))
            add(img, st, x, y, b["c"], 1.1 * (1 - k) * (0.6 + 0.4 * np.sin(k * 30)))
    enc.stdin.write((np.clip(img, 0, 1) * 255).astype(np.uint8).tobytes())
enc.stdin.close()
enc.wait()

# ---------- 3) 오르골 BGM (3/4 왈츠, 84bpm) ----------
N = int((TOTAL + 0.5) * SR)
mix = np.zeros((N, 2))


def hz(n):
    names = {"C": -9, "D": -7, "E": -5, "F": -4, "G": -2, "A": 0, "B": 2}
    return 440 * 2 ** ((names[n[0]] + (int(n[-1]) - 4) * 12) / 12)


def tine(f, dur=1.8, vel=1.0):
    tt = np.arange(int(dur * SR)) / SR
    s = (np.sin(2 * np.pi * f * tt) + .25 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt * 6)
         + .12 * np.sin(2 * np.pi * 4.2 * f * tt) * np.exp(-tt * 12))
    return s * np.exp(-tt * 2.2) * np.minimum(1, tt / .002) * vel


def pad(fs, dur, att=1.2, rel=1.5):
    tt = np.arange(int(dur * SR)) / SR
    s = sum(np.sin(2 * np.pi * f * tt + rng.uniform(0, 6)) + .3 * np.sin(2 * np.pi * f * 2.003 * tt) for f in fs) / len(fs)
    return s * np.minimum(1, tt / att) * np.minimum(1, np.maximum(0, (dur - tt) / rel))


def put(sig, t0, g, pan=0.0):
    i = int(t0 * SR)
    if i >= N:
        return
    sig = sig[:N - i]
    mix[i:i + len(sig), 0] += sig * g * (1 - pan) * .7
    mix[i:i + len(sig), 1] += sig * g * (1 + pan) * .7


beat = 60 / 84
melody = [("E5", 1), ("G5", 1), ("C6", 1), ("B5", 2), ("G5", 1), ("A5", 1), ("G5", 1), ("E5", 1), ("D5", 3),
          ("E5", 1), ("G5", 1), ("C6", 1), ("D6", 2), ("C6", 1), ("B5", 1), ("A5", 1), ("B5", 1), ("C6", 3)]
tt = 0.25
while tt < TOTAL - 1.5:
    for n, L in melody:
        if tt >= TOTAL - 1.5:
            break
        put(tine(hz(n), 1.8, .9), tt, .22, rng.uniform(-.3, .3))
        tt += L * beat * (1.0 if tt > T_LAND else 1.15)
# 착지 전: 몽환 패드 / 착지 후: 왈츠 반주(베이스 + 화음)가 들어옴 = 비트 드롭
put(pad([hz("C4"), hz("E4"), hz("G4"), hz("B4")], T_LAND, 2.0, 1.0), 0, .10)
chords = [["C3", "E4", "G4"], ["A2", "E4", "A4"], ["F2", "C4", "A4"], ["G2", "D4", "B4"]]
k, tb = 0, T_LAND
while tb < TOTAL - 1.2:
    ch = chords[(k // 3) % 4]
    if k % 3 == 0:
        put(tine(hz(ch[0]), 1.6, 1.0), tb, .30)
    else:
        put(tine(hz(ch[1]), .9, .6) + tine(hz(ch[2]), .9, .6), tb, .12, .2)
    k += 1
    tb += beat
put(pad([hz("C4"), hz("G4"), hz("E5")], TOTAL - T_LAND, 1.0, 2.0), T_LAND, .12)
# 효과: 별똥별 글리산도, 창 번쩍 차임, 착지 반짝
for j, n in enumerate(["C6", "D6", "E6", "G6", "A6", "C7"]):
    put(tine(hz(n), 1.0, .6), T_STREAK + .05 + j * .07, .10, -.4 + j * .15)
for j, n in enumerate(["G6", "E6", "C7"]):
    put(tine(hz(n), 1.6, .8), T_FLASH + j * .09, .14)
for j, n in enumerate(["C7", "G6", "E7", "C7"]):
    put(tine(hz(n), 1.4, .7), T_LAND + j * .06, .13, (-1) ** j * .3)
put(tine(hz("C6"), 3.0, 1.0) + tine(hz("E6"), 3.0, .7) + tine(hz("G6"), 3.0, .6), TOTAL - 2.6, .18)
# 잔향
ir = rng.standard_normal(int(1.8 * SR)) * np.exp(-np.arange(int(1.8 * SR)) / SR * 3.5)
ir /= np.sqrt((ir ** 2).sum())
from scipy.signal import fftconvolve
wet = np.stack([fftconvolve(mix[:, c], ir)[:N] for c in range(2)], 1)
mix = mix * .75 + wet * .55
fo = int(1.4 * SR)
mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
mix /= np.max(np.abs(mix)) / .85
bgm = os.path.join(tmp, "bgm.wav")
with wave.open(bgm, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())

# ---------- 4) 합성 ----------
OV = [("cap1", 0.3, start["02"] - 0.15), ("cap2", start["02"] + 0.2, start["03a"] - 0.1),
      ("cap3", start["03a"] + 0.3, start["04"] - 0.1), ("title", T_LAND - 0.15, start["05"] - 0.1),
      ("cap5", start["05"] + 0.2, start["06"] - 0.1), ("endlogo", start["06"] + 0.5, TOTAL)]
inputs = ["-i", body, "-i", ppath, "-i", bgm]
fc = ["[0:v]scale=1080:1920,format=gbrp,split[base][forbl]",
      "[forbl]gblur=sigma=28,eq=brightness=0.03:saturation=1.15[bl]",
      "[base][bl]blend=all_mode=screen:all_opacity=0.32,format=yuv420p,"
      "eq=saturation=1.06:gamma=1.04,colorbalance=rh=.04:bh=.02:rm=.02:bs=.03,curves=all='0/0.035 1/0.99',"
      "vignette=angle=PI/5[graded]",
      "[1:v]scale=1080:1920:flags=bicubic,gblur=sigma=1.2,format=gbrp[pt]",
      "[graded]format=gbrp[g2]",
      "[g2][pt]blend=all_mode=screen:all_opacity=0.85,format=yuv420p[v0]"]
last = "v0"
for i, (png, st, en) in enumerate(OV):
    inputs += ["-loop", "1", "-t", f"{TOTAL:.3f}", "-i", os.path.join(ovdir, png + ".png")]
    k = i + 3
    fc.append(f"[{k}:v]format=rgba,fade=t=in:st={st:.3f}:d=0.35:alpha=1,fade=t=out:st={en - 0.3:.3f}:d=0.3:alpha=1[o{i}]")
    fc.append(f"[{last}][o{i}]overlay=enable='between(t,{st:.3f},{en:.3f})'[v{i + 1}]")
    last = f"v{i + 1}"
fc.append(f"[{last}]fade=t=in:st=0:d=0.3,fade=t=out:st={TOTAL - 0.5:.3f}:d=0.5,format=yuv420p[vout]")
fc.append("[0:a]volume=0.55[sfx]")
fc.append(f"[2:a]atrim=0:{TOTAL:.3f},volume=0.9[bg]")
fc.append("[sfx][bg]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[aout]")
run([*inputs, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-t", f"{TOTAL:.3f}",
     "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-maxrate", "16M", "-bufsize", "24M",
     "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", out])
print("done", out, round(dur(out), 2))
