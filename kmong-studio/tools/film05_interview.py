"""FILM05 GRWM × MULGYUL — 매거진 뷰티 인터뷰 스타일 9:16 조립.

하드컷 + 인터뷰식 점프컷(같은 컷 안에서 살짝 확대), 에디토리얼 그레이드·필름 그레인,
Q(질문) → A(대답) 자막, 맑고 발랄한 어쿠스틱 팝 BGM(직접 합성)과 셔터 소리.

usage: python3 film05_interview.py <uploads_dir> <overlay_dir> <out.mp4>
       CUT=short 이면 15초 미만 숏컷 버전 (제품 크레딧 컷 생략, 컷 길이 압축)
"""
import glob
import os
import re
import subprocess
import sys
import tempfile
import wave

import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve, lfilter

F = os.environ.get("FFMPEG", "ffmpeg")
up, ovdir, out = [os.path.abspath(p) for p in sys.argv[1:4]]
SR, FPS = 48000, 24
rng = np.random.default_rng(5)

MODE = os.environ.get("CUT", "full")
# (이름, 파일 id, 시작, 끝, 줌 시작, 줌 끝)
if MODE == "short":
    SEGS = [
        ("g1", "81cc241a", 0.3, 2.3, 1.00, 1.03),
        ("g2a", "8102e669", 0.2, 1.2, 1.00, 1.02),
        ("g2b", "8102e669", 5.8, 7.2, 1.10, 1.12),
        ("g3", "c105f591", 0.0, 1.8, 1.00, 1.04),
        ("g4a", "0e83542a", 0.3, 1.5, 1.00, 1.02),
        ("g4b", "0e83542a", 5.4, 6.8, 1.10, 1.12),
        ("g6a", "814daa9c", 0.0, 2.6, 1.00, 1.03),
        ("g6b", "814daa9c", 9.0, 10.0, 1.00, 1.02),
    ]
    END_ID, END_SS, END = "451fc5a4", 1.6, 2.2
else:
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
    END_ID, END_SS, END = "451fc5a4", 1.0, 3.2   # 엔딩 패키샷 (크림 스튜디오 앰플 푸시인)
# 장면이 바뀌는 컷 (셔터 소리): 이름 앞 두 글자(g1, g2…)가 달라지는 곳 + 엔딩
SCENE_CUTS = {i for i in range(1, len(SEGS)) if SEGS[i][0][:2] != SEGS[i - 1][0][:2]} | {len(SEGS)}


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
# 엔딩: 크림 스튜디오 앰플 패키샷 + 로고
n = round(END * FPS)
endp = os.path.join(tmp, "end.mov")
run(["-ss", f"{END_SS}", "-t", f"{END}", "-i", src(END_ID), "-f", "lavfi", "-t", f"{END}", "-i",
     "anullsrc=r=48000:cl=stereo", "-vf", f"fps={FPS},{GRADE},setsar=1", "-map", "0:v", "-map", "1:a", "-frames:v", str(n),
     "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ac", "2", endp])
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

# ---------- 2) 맑고 발랄한 어쿠스틱 팝 BGM (116bpm, D-A-Bm-G) ----------
N = int((TOTAL + .5) * SR)
mix = np.zeros((N, 2))
beat = 60 / 116


def put(sig, t0, g, pan=0.0):
    i = int(t0 * SR)
    if i >= N or i < 0:
        return
    sig = sig[:N - i]
    mix[i:i + len(sig), 0] += sig * g * (1 - pan)
    mix[i:i + len(sig), 1] += sig * g * (1 + pan)


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def pluck(m, d=1.2, damp=.996):
    """카플러스-스트롱 기타/우쿨렐레 줄."""
    L = int(SR / hz(m))
    x = np.zeros(int(d * SR))
    x[:L] = rng.uniform(-1, 1, L)
    x[:L] = sosfilt(butter(1, 5000, "low", fs=SR, output="sos"), x[:L])
    a = np.zeros(L + 2)
    a[0], a[L], a[L + 1] = 1, -.5 * damp, -.5 * damp
    y = lfilter([1], a, x)
    return y * np.minimum(1, np.arange(len(y)) / (.002 * SR))


def strum(ms, t0, g, up=False):
    for j, m in enumerate(reversed(ms) if up else ms):
        put(pluck(m, .9), t0 + j * .011, g * (.7 if up else 1), -.35 + .14 * j)


def glock(m, d=1.4):
    tt = np.arange(int(d * SR)) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * tt) + .35 * np.sin(2 * np.pi * 2.76 * f * tt) * np.exp(-tt * 6) \
        + .12 * np.sin(2 * np.pi * 5.4 * f * tt) * np.exp(-tt * 14)
    return s * np.exp(-tt * 3.2) * np.minimum(1, tt / .001)


def bass(m, d=.45):
    tt = np.arange(int(d * SR)) / SR
    s = np.sin(2 * np.pi * hz(m) * tt) + .2 * np.sin(4 * np.pi * hz(m) * tt)
    return s * np.exp(-tt * 5) * np.minimum(1, tt / .006)


def kick():
    tt = np.arange(int(.25 * SR)) / SR
    return np.sin(2 * np.pi * np.cumsum(55 + 70 * np.exp(-tt * 40)) / SR) * np.exp(-tt * 16)


def noise_hit(d, lo, hi, dec):
    n = rng.standard_normal(int(d * SR))
    return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), n) * np.exp(-np.arange(len(n)) / SR * dec)


def clap():
    c = np.zeros(int(.2 * SR))
    for k, dt in enumerate([0, .011, .022]):
        h = noise_hit(.15, 900, 4000, 28)
        c[int(dt * SR):int(dt * SR) + len(h)] += h * (.6 if k < 2 else 1)
    return c


def bird(t0, g):
    tt = np.arange(int(.12 * SR)) / SR
    f = 3800 + 1400 * np.sin(2 * np.pi * 9 * tt) - 2500 * tt
    chirp = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / tt[-1]) ** 2
    for k in range(2 + int(rng.integers(0, 2))):
        put(chirp, t0 + k * .15, g, .6 if k % 2 else -.5)


def shutter():
    c = noise_hit(.09, 1500, 7000, 80)
    c2 = np.zeros(int(.16 * SR))
    c2[:len(c)] += c
    c2[int(.055 * SR):int(.055 * SR) + len(c)] += c * .6
    return c2


# 코드 (근음, 우쿨렐레 보이싱) · 멜로디 (박, 음) 2마디 모티프 반복
prog = [(38, [62, 66, 69, 74]), (45, [61, 64, 69, 73]), (47, [62, 66, 71, 74]), (43, [62, 67, 71, 74])]
mel = [(0, 81), (1, 78), (1.5, 81), (2, 83), (3, 81),
       (4, 76), (5, 78), (5.5, 81), (6, 85), (7, 83)]
T_END = starts[-1]
DRUMS = starts[1] - beat / 2
b = 0
while b * beat < T_END - .05:
    tb = b * beat
    bar = (b // 4) % 4
    root, ch = prog[bar]
    # 스트럼: 박마다 다운 · 8분 뒤 업
    strum(ch, tb, .16, False)
    strum(ch, tb + beat / 2, .10, True)
    if tb >= DRUMS:
        put(kick(), tb, .55 if b % 2 == 0 else .35)
        if b % 2 == 1:
            put(clap(), tb, .32, .05)
        put(noise_hit(.05, 6000, 12000, 70), tb + beat / 2, .10, .4)   # 셰이커
        put(noise_hit(.04, 6000, 12000, 90), tb + beat * .75, .06, .4)
        put(bass(root if b % 2 == 0 else root + 7), tb, .38)
    b += 1
nbar = 0
while nbar * 8 * beat < T_END:
    for pos, m in mel:
        tm = (nbar * 8 + pos) * beat
        if tm < T_END - .1:
            put(glock(m), tm, .13, .15)
    nbar += 1
for k, t_ in enumerate([.3, 1.9, 6.4, 11.0, 15.6]):                 # 멀리서 새소리
    bird(t_, .05)
# 엔딩: D 코드 아르페지오 + 글로켄 반짝
for j, m in enumerate([62, 66, 69, 74, 78, 81]):
    put(pluck(m, 2.5, .998), T_END + j * .07, .2, -.3 + .12 * j)
for j, m in enumerate([86, 90, 93, 98]):
    put(glock(m, 2.0), T_END + .35 + j * .09, .10, .2)
put(bass(38, 2.0), T_END, .4)
put(kick(), T_END, .5)
for i in SCENE_CUTS:
    put(shutter(), starts[i] - .02, .35, .1)
ir = rng.standard_normal(int(1.0 * SR)) * np.exp(-np.arange(int(1.0 * SR)) / SR * 6)
ir /= np.sqrt((ir ** 2).sum())
mix = mix * .88 + np.stack([fftconvolve(mix[:, c], ir)[:N] for c in range(2)], 1) * .18
mix = sosfilt(butter(2, 35, "high", fs=SR, output="sos"), mix, axis=0)
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
st = {name: starts[i] for i, (name, *_) in enumerate(SEGS)}
st["end"] = starts[-1]
en = {name: (starts[i + 1]) for i, (name, *_) in enumerate(SEGS)}
OV = [("title", st["g1"] + .25, en["g1"], True),
      ("q1", st["g2a"] + .1, en["g2a"], True), ("qa1", st["g2b"], en["g2b"], False),
      ("step", st["g3"] + .2, en["g3"], True),
      ("q2", st["g4a"] + .1, en["g4a"], True), ("qa2", st["g4b"], en["g4b"], False)]
if "g5" in st:
    OV.append(("credit", st["g5"] + .3, en["g5"], True))
qa3_at = st["g6a"] + (1.8 if MODE != "short" else 1.3)
OV += [("q3", st["g6a"] + .2, qa3_at, True), ("qa3", qa3_at, min(en["g6a"] + 1.0, st["end"] - .3), False),
       ("endlogo", st["end"] + .3, TOTAL, True)]
inputs = ["-i", body, "-i", bgm]
fc = ["[0:v]noise=alls=5:allf=t,format=yuv420p[v0]"]
lastv = "v0"
for i, (png, t0, t1, fade_in) in enumerate(OV):
    inputs += ["-loop", "1", "-t", f"{TOTAL:.3f}", "-i", os.path.join(ovdir, png + ".png")]
    k = i + 2
    fi = f"fade=t=in:st={t0:.3f}:d=0.2:alpha=1," if fade_in else ""
    fo_ = f"fade=t=out:st={t1 - .15:.3f}:d=0.15:alpha=1" if png.startswith(("qa", "title", "step", "credit", "endlogo")) else "null"
    fc.append(f"[{k}:v]format=rgba,{fi}{fo_}[o{i}]")
    fc.append(f"[{lastv}][o{i}]overlay=enable='between(t,{t0:.3f},{t1:.3f})'[v{i + 1}]")
    lastv = f"v{i + 1}"
inputs += ["-f", "lavfi", "-t", f"{TOTAL:.3f}", "-i", "color=c=white:s=1080x1920:r=24"]
w = len(OV) + 2
t_w = st["end"]
fc.append(f"[{w}:v]format=rgba,fade=t=in:st={t_w - .25:.3f}:d=0.25:alpha=1,fade=t=out:st={t_w:.3f}:d=0.45:alpha=1[wf]")
fc.append(f"[{lastv}][wf]overlay=enable='between(t,{t_w - .25:.3f},{t_w + .45:.3f})'[vw]")
lastv = "vw"
fc.append(f"[{lastv}]fade=t=in:st=0:d=0.2,fade=t=out:st={TOTAL - .4:.3f}:d=0.4,format=yuv420p[vout]")
fc.append("[0:a]volume=0.30[sfx]")
fc.append(f"[1:a]atrim=0:{TOTAL:.3f},volume=0.9[bg]")
fc.append("[sfx][bg]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[aout]")
run([*inputs, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-t", f"{TOTAL:.3f}",
     "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-maxrate", "16M", "-bufsize", "24M",
     "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", out])
print("done", out, round(dur(out), 2))
