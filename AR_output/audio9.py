import numpy as np, json, subprocess
SR = 48000
tl = json.load(open('timeline9x.json'))['marks']
TOTAL = max(v[1] for v in tl.values())
N = int(TOTAL * SR) + SR
rng = np.random.default_rng(7)
life = np.zeros(N); act = np.zeros(N); end = np.zeros(N)
cue = []

def t2i(t): return int(t * SR)
def place(buf, t, x, g=1.0, label=None):
    i = t2i(t); j = min(i + len(x), N); buf[i:j] += x[:j - i] * g
    if label: cue.append((round(t, 2), label))
def env(n, a, d, shape=4.0):
    t = np.arange(n) / SR; e = np.minimum(t / max(a, 1e-4), 1) * np.exp(-np.maximum(t - a, 0) * shape / max(d, 1e-4)); return e
def noise(n): return rng.standard_normal(n)
def bp(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def pink(n):
    X = np.fft.rfft(noise(n)); f = np.fft.rfftfreq(n, 1 / SR); X[1:] /= np.sqrt(f[1:]); X[0] = 0; y = np.fft.irfft(X, n); return y / np.abs(y).max()

# ---- sound atoms (procedural foley) ----
def tick():
    n = int(0.03 * SR); return bp(noise(n), 2500, 7000) * env(n, 0.0005, 0.01, 5)
def tak(f0=700):          # wooden "탁"
    n = int(0.18 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f0 * t) * 0.7 + bp(noise(n), 300, 4000) * 0.5) * env(n, 0.001, 0.06, 6)
def ttak():               # pen "딱"
    n = int(0.08 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2400 * t) * 0.5 + bp(noise(n), 1500, 9000) * 0.6) * env(n, 0.0005, 0.02, 6)
def rustle(d=0.5):        # cloth "부스럭"
    n = int(d * SR); g = np.abs(bp(noise(n), 3, 25)); g /= g.max() + 1e-9
    return bp(noise(n), 400, 6000) * g ** 1.5 * env(n, 0.05, d, 2.5)
def paper(d=0.25):        # "사락 / 사각"
    n = int(d * SR); g = np.abs(bp(noise(n), 20, 60)); g /= g.max() + 1e-9
    return bp(noise(n), 2500, 11000) * g * env(n, 0.01, d, 3)
def whoosh(d=0.35):       # "휙"
    n = int(d * SR); t = np.arange(n) / SR; x = noise(n); y = np.zeros(n); seg = 2048
    for k in range(0, n, seg):
        c = 500 + 3500 * np.sin(np.pi * min(k / n, 1)); y[k:k + seg] = bp(x[k:k + seg], c * 0.6, c * 1.6)
    return y * np.sin(np.pi * t / (d)) ** 2
def thud(f0=75, d=0.35):  # "툭 / 쿵"
    n = int(d * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f0 * t * (1 - 0.3 * t / d)) + bp(noise(n), 80, 900) * 0.4) * env(n, 0.002, d * 0.5, 5)
def drag(d=1.0):          # "드르륵"
    n = int(d * SR); t = np.arange(n) / SR; am = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 28 * t))
    return bp(noise(n), 150, 2500) * am * env(n, 0.05, d, 1.5)
def swish(d=0.9):         # bedding "촤락"
    n = int(d * SR); return bp(noise(n), 600, 9000) * env(n, 0.06, d, 3.5)
def ding():               # phone notification
    n = int(0.7 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 1976 * t)) * env(n, 0.005, 0.5, 4)
def clink():              # "달그락"
    n = int(0.25 * SR); t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * t) * a for f, a in [(2100, .5), (3300, .3), (4700, .2)]) * env(n, 0.001, 0.12, 6)

S = lambda k: tl[k][0]
REVEAL = S('HEAP_hold_sigh') + 0.6           # heap fully visible (camera stopped)
SIGH_T = REVEAL + 0.5                         # 0.5 s of total silence first

# ---- 1. room tone + life noises (busy from the start, more & more layered) ----
room = pink(N) * 0.004
life += room
t = 0.15
while t < REVEAL:
    place(life, t, tick(), 0.05 + 0.04 * min(t / 20, 1)); t += 1.0
dens = []
kinds = [(paper, 0.3, 'paper'), (clink, None, 'clink'), (ding, None, 'notify'), (tak, 480, 'object')]
tt = 0.6; k = 0
while tt < REVEAL - 0.4:
    fn, arg, lab = kinds[k % 4]; x = fn(arg) if arg is not None else fn()
    dens.append((tt, x, lab)); k += 1
    prog = tt / REVEAL
    tt += 1.9 - 1.3 * prog + rng.random() * 0.4      # more & more frequent toward the reveal
for tt, x, lab in dens:
    g = 0.035 + 0.06 * min(tt / REVEAL, 1)
    place(life, tt, x, g * (0.6 if lab == 'notify' else 1.0))
p0 = S('SEG4A')
for j, tt in enumerate(np.arange(p0, S('R1_walk_turn'), 0.55)):
    place(life, tt, [tak(), paper(0.2), whoosh(0.3), thud(80, 0.3)][j % 4], 0.05)
# rotation: everything fades down, then HARD CUT at reveal
fade_start = S('R1_walk_turn'); i0, i1 = t2i(fade_start), t2i(REVEAL)
ramp = np.ones(N); ramp[i0:i1] = np.linspace(1, 0.35, i1 - i0); ramp[i1:] = 0
life *= ramp

# ---- 2. action sounds: piecewise source->output mapping of build9 ----
PL = {'SEG1': [[(0.5, 2.6, 1.8), (2.6, 5.8, 2.4), (5.8, 7.4, 1.0), (7.4, 9.6, 2.6)]],
      'SEG2A': [[(1.0, 1.8, 2.0), (1.8, 4.2, 1.35), (4.2, 7.95, 2.6)]],
      'SEG2B': [[(4.55, 9.9, 3.0)]],
      'SEG3A': [[(2.6, 4.0, 2.5), (4.0, 5.7, 1.0)]],
      'SEG3B': [[(0.5, 1.05, 1.3)], [(1.85, 2.7, 1.0), (2.7, 4.3, 3.0), (4.3, 6.6, 2.0), (6.6, 9.95, 3.0)]],
      'SEG4A': [[(3.05, 4.4, 2.5), (4.4, 5.2, 2.8)], [(5.1, 6.0, 2.8), (6.0, 7.4, 1.5), (7.4, 9.9, 3.0)]],
      'SEG4B': [[(0.0, 1.7, 1.6)], [(8.6, 10.0, 1.0)]]}
XJ = {'SEG3B': 0.45, 'SEG4A': 0.15, 'SEG4B': 0.6}
def at(seg, src):
    off = S(seg)
    for ch in PL[seg]:
        acc = 0.0
        for a, b, sp in ch:
            if a <= src <= b: return off + acc + (src - a) / sp
            acc += (b - a) / sp
        off += acc - XJ.get(seg, 0)
    raise ValueError((seg, src))
A = [(at('SEG1', 4.4), rustle(0.35), 0.5, '왼쪽 옷 부스럭'), (at('SEG1', 5.3), tak(650), 0.55, '탁!'),
     (at('SEG1', 6.0), whoosh(0.35), 0.2, '고개 돌림'),
     (at('SEG1', 7.7), rustle(0.4), 0.5, '오른쪽 옷 부스럭'), (at('SEG1', 8.6), tak(600), 0.55, '탁!'),
     (at('SEG2A', 2.2), whoosh(0.3), 0.2, '고개 들기'),
     (at('SEG2A', 4.6), rustle(0.5), 0.6, '부스럭부스럭'), (at('SEG2A', 7.2), tak(380), 0.7, '옷장 문 탁'),
     (S('blink_desk') + 0.2, whoosh(0.3), 0.12, '깜빡 → 책상'),
     (at('SEG2B', 4.75), paper(0.2), 0.45, '노트 슥'), (at('SEG2B', 5.55), tak(800), 0.5, '책 탁'),
     (at('SEG2B', 5.95), ttak(), 0.45, '펜 딱'), (at('SEG2B', 6.6), paper(0.25), 0.4, '노트북 슥'),
     (at('SEG2B', 7.55), tak(850), 0.5, '노트북 탁'), (at('SEG2B', 7.85), paper(0.15), 0.4, '노트 각 맞춤'),
     (at('SEG3A', 3.0), paper(0.25), 0.5, '종이 사락'), (at('SEG3A', 4.2), whoosh(0.35), 0.6, '휙—'),
     (at('SEG3A', 5.2), thud(110, 0.25), 0.5, '화면 밖 툭!'),
     (at('SEG3B', 0.8), whoosh(0.5), 0.2, '침대로 돌기'),
     (at('SEG3B', 4.3), rustle(0.3), 0.5, '옷 부스럭'), (at('SEG3B', 4.6), whoosh(0.35), 0.6, '휙—'),
     (at('SEG3B', 5.1), thud(100, 0.25), 0.5, '툭!'), (at('SEG3B', 5.6), swish(0.8), 0.45, '침구 촤락—'),
     (at('SEG3B', 7.3), tak(500), 0.35, '쿠션 툭'),
     (S('blink_box') + 0.2, whoosh(0.3), 0.12, '깜빡 → 상자'), (at('SEG4A', 4.7), clink(), 0.5, '머그 달그락'),
     (at('SEG4A', 6.2), drag(1.0), 0.55, '상자 드르륵—'), (at('SEG4A', 7.4), thud(62, 0.5), 0.9, '쿵!'),
     (at('SEG4B', 0.6), whoosh(0.5), 0.2, '일어서기')]
for tt, x, g, lab in A: place(act, tt, x, g, lab)
act[t2i(REVEAL):] = 0  # nothing from actions after the cut

# ---- 3. sigh ----
sig = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'sigh_clean.wav', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
sigh = np.frombuffer(sig, np.float32).astype(np.float64)
place(end, SIGH_T, sigh, 1.0, '한숨 "하…" (고객 녹음 5번)')
cue.append((round(REVEAL, 2), '더미 완전 공개 = 모든 소음 CUT'))

# ---- 4. tinnitus "삐—" after the sigh, wavering at blinks, weak static, BLACK = cut ----
E0 = S('ending_blinks_black')
BLACK = E0 + 2.05 + 0.70
t_on = SIGH_T + len(sigh) / SR + 0.15
i0, i1 = t2i(t_on), t2i(BLACK)
tt = np.arange(i1 - i0) / SR
beep = np.sin(2 * np.pi * 6200 * tt) * (0.004 + 0.016 * (tt / tt[-1]) ** 1.5) * (1 + 0.15 * np.sin(2 * np.pi * 5 * tt))
beep[:int(0.8 * SR)] *= np.linspace(0, 1, int(0.8 * SR))
end[i0:i1] += beep
cue.append((round(t_on, 2), '얇은 이명음 삐— 시작'))
# blinks in the ending: momentary sound drop-out (same timing as the picture)
def blink_gate(t0, c, h, o):
    a = t2i(E0 + t0 + c * 0.6); b = t2i(E0 + t0 + c + h + o * 0.4)
    end[a:b] *= 0.15
blink_gate(0.25, 0.12, 0.10, 0.22); blink_gate(1.05, 0.18, 0.16, 0.38)
cue += [(round(E0 + 0.25, 2), '엔딩 깜빡 1 (소리 순간 끊김)'), (round(E0 + 1.05, 2), '엔딩 깜빡 2 (소리 흔들림)')]
# weak static noise growing until black
s0 = t2i(E0 + 1.2)
st = bp(noise(i1 - s0), 1500, 12000) * np.linspace(0, 0.02, i1 - s0) * (0.7 + 0.3 * (rng.random(i1 - s0) > 0.97))
end[s0:i1] += st
cue.append((round(E0 + 1.2, 2), '약한 지직 노이즈 시작'))
end[i1:] = 0
cue.append((round(BLACK, 2), '완전 BLACK = 삐—·모든 소리 뚝'))

mix = life + act + end
mix[t2i(BLACK):] = 0
mix = mix[:int(TOTAL * SR)]
peak = np.abs(mix).max(); mix = mix / peak * 0.89
st2 = np.stack([mix, mix], 1).astype(np.float32)
open('mix.f32', 'wb').write(st2.tobytes())
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', 'mix.f32', '-c:a', 'pcm_s16le', 'soundtrack9.wav'], check=True)
json.dump({'reveal': REVEAL, 'sigh': SIGH_T, 'black': BLACK, 'cue': sorted(cue)}, open('cue9.json', 'w'), ensure_ascii=False, indent=1)
print('reveal', round(REVEAL, 2), 'sigh', round(SIGH_T, 2), 'black', round(BLACK, 2), 'total', round(TOTAL, 2))
