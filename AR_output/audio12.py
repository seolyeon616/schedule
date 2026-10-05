import numpy as np, json, subprocess
SR = 48000
TLJ = json.load(open('timeline12x.json')); tl = TLJ['marks']; MAPS = TLJ['maps']; COMP = TLJ['comp']
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
def at(seg, src):
    off = S(seg)
    for ch in COMP[seg]['chains']:
        mp = np.array(MAPS[ch])
        if mp[0] - 1e-3 <= src <= mp[-1] + 0.05: return off + np.interp(src, mp, np.arange(len(mp))) / 24
        off += len(mp) / 24 - COMP[seg]['xj']
    raise ValueError((seg, src))
REVEAL = S('HEAP_hold_sigh') - 0.15        # turn has settled on the heap
RUSTLE = S('STARE_clean_room') + TLJ['extra']['rustle']
SIGH_T = REVEAL + 0.7                         # a moment of total silence first

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
for j, tt in enumerate(np.arange(p0, S('STARE_clean_room'), 0.55)):
    place(life, tt, [tak(), paper(0.2), whoosh(0.3), thud(80, 0.3)][j % 4], 0.05)
# staring at the clean room: the room goes quieter so the off-screen rustle is heard; noise creeps back during the turn,
# then EVERYTHING is cut the moment the heap is seen
a0, a1, a2 = t2i(S('STARE_clean_room')), t2i(S('STARE_clean_room') + 0.8), t2i(S('TURN_to_heap'))
ramp = np.ones(N); ramp[a0:a1] = np.linspace(1, 0.4, a1 - a0); ramp[a1:a2] = 0.4
i1 = t2i(REVEAL); ramp[a2:i1] = np.linspace(0.4, 0.75, i1 - a2); ramp[i1:] = 0
life *= ramp

# ---- 2. action sounds: piecewise source->output mapping of build9 ----
L0 = S('DESK_LAP')
A = [(at('SEG1', 4.4), rustle(0.35), 0.5, '왼쪽 옷 부스럭'), (at('SEG1', 5.3), tak(650), 0.55, '스윽-탁!'),
     (at('SEG1', 6.0), whoosh(0.35), 0.15, '고개 돌림'),
     (at('SEG1', 7.7), rustle(0.4), 0.5, '오른쪽 옷 부스럭'), (at('SEG1', 8.6), tak(600), 0.55, '스윽-탁!'),
     (at('SEG2A', 2.2), whoosh(0.3), 0.15, '고개 들기'),
     (at('SEG2A', 4.9), rustle(0.6), 0.65, '셔츠 대충 쑤셔넣기 부스럭'), (at('SEG2A', 7.2), tak(380), 0.7, '옷장 문 탁'),
     (L0 - 0.12, whoosh(0.3), 0.1, '깜빡 → 책상'),
     (L0 + 0.70, paper(0.35), 0.30, '노트북 스르륵 (천천히)'), (L0 + 1.55, tak(1100), 0.18, '각 맞춤 톡'),
     (L0 + 2.05, paper(0.22), 0.22, '다시 살짝 당김'), (L0 + 2.55, paper(0.22), 0.22, '다시 맞춤'),
     (L0 + 2.95, paper(0.18), 0.18, '한 번 더'), (L0 + 3.45, tak(1200), 0.16, '딱 맞춤 톡'),
     (at('DESK_TOSS', 3.15), paper(0.2), 0.5, '책 집어듦'), (at('DESK_TOSS', 4.3), whoosh(0.35), 0.65, '휙—'),
     (at('DESK_TOSS', 5.25), thud(110, 0.25), 0.55, '화면 밖 툭!'),
     (at('SEG3B', 0.8), whoosh(0.5), 0.15, '침대로 돌기'),
     (at('SEG3B', 4.3), rustle(0.3), 0.5, '스웨터 부스럭'), (at('SEG3B', 4.6), whoosh(0.35), 0.6, '휙—'),
     (at('SEG3B', 5.1), thud(100, 0.25), 0.5, '툭!'), (at('SEG3B', 5.6), swish(1.2), 0.35, '이불 천천히 스르륵—'),
     (at('SEG3B', 7.0), swish(1.0), 0.25, '이불 결 정리'), (at('SEG3B', 8.4), swish(0.9), 0.2, '한 번 더 쓸어내림'),
     (S('SEG4A') - 0.12, whoosh(0.3), 0.1, '깜빡 → 상자'), (at('SEG4A', 4.7), clink(), 0.5, '머그 달그락'),
     (at('SEG4A', 6.2), drag(1.0), 0.55, '상자 드르륵—'), (at('SEG4A', 7.4), thud(62, 0.5), 0.9, '쿵!'),
     (at('SEG4B', 0.6), whoosh(0.5), 0.15, '일어서기')]
for tt, x, g, lab in A: place(act, tt, x, g, lab)
act[t2i(REVEAL):] = 0  # nothing from actions after the cut
behind = np.zeros(N)
rb = rustle(0.75); rb = bp(rb, 300, 3500)           # muffled: it comes from behind, out of view
place(behind, RUSTLE, rb, 0.75, '화면 밖 뒤쪽 바스락…')
place(act, S('TURN_to_heap') + 0.6, whoosh(2.2), 0.12, '천천히 뒤돌아봄')

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
d = int(0.012 * SR)                                   # rustle: louder in the right ear, slightly late in the left
Lc = mix + np.concatenate([np.zeros(d), behind[:-d]]) * 0.55; Rc = mix + behind
Lc = Lc[:int(TOTAL * SR)]; Rc = Rc[:int(TOTAL * SR)]
peak = max(np.abs(Lc).max(), np.abs(Rc).max()); Lc = Lc / peak * 0.89; Rc = Rc / peak * 0.89
st2 = np.stack([Lc, Rc], 1).astype(np.float32)
open('mix.f32', 'wb').write(st2.tobytes())
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', 'mix.f32', '-c:a', 'pcm_s16le', 'soundtrack12.wav'], check=True)
json.dump({'reveal': REVEAL, 'sigh': SIGH_T, 'black': BLACK, 'cue': sorted(cue)}, open('cue12.json', 'w'), ensure_ascii=False, indent=1)
print('reveal', round(REVEAL, 2), 'sigh', round(SIGH_T, 2), 'black', round(BLACK, 2), 'total', round(TOTAL, 2))
