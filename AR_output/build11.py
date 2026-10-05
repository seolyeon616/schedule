"""v11 (33 s): smooth speed curves (no speed steps), speed-matched motion blur, blinks over moving
footage (no frozen frames), clothes restored in the first walk-in (g1c_cl.mp4)."""
import subprocess, json, os, math, numpy as np, cv2
D = 'seg11'; os.makedirs(D, exist_ok=True)
FPS, W, H = 24, 1920, 1080
SW = ['-sws_flags', 'lanczos+accurate_rnd+full_chroma_int+full_chroma_inp']
E = ['-an'] + SW + ['-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', '-r', '24']
def dur(p): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
MAPS = {}

YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
def eyelid(f, op, blur=0.0):
    if blur > 0: f = cv2.GaussianBlur(f, (0, 0), blur)
    if op >= 0.999: return f
    if op <= 0.001: return np.zeros_like(f)
    ry = op * H * 0.72 + 1; rx = W * 0.78
    d = ((XX - W / 2) / rx) ** 2 + ((YY - H / 2) / ry) ** 2
    m = np.clip((1 - d) / (0.08 + 0.25 * (1 - op)), 0, 1)
    return f * m[..., None] * (0.75 + 0.25 * op)
def ss(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)

class Writer:
    def __init__(s, name):
        s.out = f'{D}/{name}.mp4'
        s.p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '24', '-i', '-'] + E + [s.out], stdin=subprocess.PIPE)
    def w(s, f): s.p.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
    def close(s): s.p.stdin.close(); s.p.wait(); return s.out

def load(src, a, b, crop):
    j0 = max(int(math.floor(a * FPS)) - 4, 0); n = int(math.ceil((b - j0 / FPS) * FPS)) + 6
    w, h = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.strip().split(','))
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src] + SW + ['-vf', f'select=gte(n\\,{j0})', '-vsync', '0', '-frames:v', str(n), '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
    out = []
    for f in fr:
        if crop:
            cy, cx = int(h * 0.006) + 1, int(w * 0.006) + 1; f = f[cy:h - cy, cx:w - cx]
        out.append(cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4) if f.shape[:2] != (H, W) else np.ascontiguousarray(f))
    return j0, out

def curve(parts, ramp):
    """smoothed speed curve -> source time at each output frame (and speed)"""
    do = 1 / 480; v = []
    for a, b, sp in parts: v += [sp] * max(int(round((b - a) / sp / do)), 1)
    v = np.array(v, float)
    if ramp > 0 and len(parts) > 1:
        r = int(3 * ramp / do); k = np.exp(-0.5 * (np.arange(-r, r + 1) * do / ramp) ** 2); k /= k.sum()
        v = np.convolve(np.pad(v, r, mode='edge'), k, mode='valid')
    a0, b1 = parts[0][0], parts[-1][1]
    v *= (b1 - a0) / (v.sum() * do)
    s = a0 + np.concatenate([[0], np.cumsum(v)]) * do
    T = len(v) * do; n = int(round(T * FPS))
    idx = np.minimum((np.arange(n) / FPS / do).astype(int), len(v) - 1)
    return s[idx], v[idx]

def path_curve(keys):
    """keys: [(out_t, src_t)] -> smooth (C1, monotone between keys) source time per output frame"""
    ko = np.array([k[0] for k in keys], float); ks = np.array([k[1] for k in keys], float)
    n = int(round(ko[-1] * FPS)); o = np.arange(n) / FPS
    i = np.clip(np.searchsorted(ko, o, side='right') - 1, 0, len(ko) - 2)
    u = (o - ko[i]) / (ko[i + 1] - ko[i]); u = u * u * (3 - 2 * u)      # ease in/out at every key (direction changes stop softly)
    st = ks[i] + (ks[i + 1] - ks[i]) * u
    vt = np.abs(np.gradient(st)) * FPS
    return st, vt
def retime(name, src, parts=None, crop=True, ramp=0.3, lid_in=0.0, lid_out=0.0, black=0.0, post=None, path=None):
    if path is not None:
        st, vt = path_curve(path); lo, hi = float(st.min()), float(st.max())
    else:
        st, vt = curve(parts, ramp); lo, hi = parts[0][0], parts[-1][1]
    j0, fr = load(src, lo, hi, crop)
    last = len(fr) - 1
    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    gy = [None] * len(fr); fl = {}
    def gray(i):
        if gy[i] is None: gy[i] = cv2.cvtColor(cv2.resize(fr[i], (W // 2, H // 2), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
        return gy[i]
    def flow(i):                      # forward flow i -> i+1 at full res (pixels per source frame)
        if i not in fl:
            j = min(i + 1, last)
            f2 = dis.calc(gray(i), gray(j), None) if j != i else np.zeros((H // 2, W // 2, 2), np.float32)
            fl[i] = cv2.resize(f2, (W, H), interpolation=cv2.INTER_LINEAR) * 2.0
        return fl[i]
    def at(t):
        x = t * FPS - j0; i = int(math.floor(x)); u = x - i
        i = min(max(i, 0), last); i2 = min(i + 1, last)
        if u < 0.02 or i == i2: return fr[i].astype(np.float32)
        if u > 0.98: return fr[i2].astype(np.float32)
        return cv2.addWeighted(fr[i], 1 - u, fr[i2], u, 0).astype(np.float32)
    def flow_frame(t, Lf):
        """frame at source time t with motion blur spanning Lf source frames, built by warping the
        nearest real frame along its optical flow (no stacked ghost copies)"""
        x = t * FPS - j0; c = min(max(int(round(x)), 0), last - 1); d = x - c
        F = flow(c); fx, fy = F[..., 0], F[..., 1]
        m = max(int(math.ceil(Lf * 6)), 1)
        acc = np.zeros((H, W, 3), np.float32)
        for q in range(m):
            sft = np.float32(d + (Lf * ((q + 0.5) / m - 0.5) if m > 1 else 0.0))
            acc += cv2.remap(fr[c], XX - sft * fx, YY - sft * fy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        return acc / m
    wr = Writer(name); n = len(st)
    for k in range(n):
        Lf = min(vt[k], 3.0) * 0.75          # 270-degree shutter in source frames
        f = at(st[k]) if vt[k] <= 1.25 else flow_frame(st[k], Lf)
        if post: f = post(f, k, st)
        o = k / FPS; T = n / FPS
        if lid_in and o < lid_in:
            op = ss(o / lid_in); f = eyelid(f, op, blur=(1 - op) * 3)
        if lid_out and o > T - lid_out:
            op = ss((T - o) / lid_out); f = eyelid(f, op, blur=(1 - op) * 3)
        wr.w(f)
    for _ in range(int(round(black * FPS))): wr.w(np.zeros((H, W, 3), np.float32))
    MAPS[name] = [round(float(x), 4) for x in st]
    return wr.close()

def xjoin(name, files, xf):
    cur = files[0]
    for k, nx in enumerate(files[1:]):
        off = dur(cur) - xf; out = f'{D}/{name}_x{k}.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', cur, '-i', nx, '-filter_complex', f'[0:v][1:v]xfade=transition=fade:duration={xf}:offset={off:.4f},format=yuv420p'] + E + [out], check=True)
        cur = out
    return cur

segs = []; COMP = {}
def add(p, l, chains=(), xj=0.0):
    segs.append((p, dur(p), l)); COMP[l] = {'chains': list(chains), 'xj': xj}
    print(f'{l:26s} {segs[-1][1]:5.2f}', flush=True)

def bc(t, t0, c, h, o):
    if t < t0: return 1.0
    t -= t0
    if t < c: return 1 - ss(t / c)
    t -= c
    if t < h: return 0.0
    t -= h
    if t < o: return ss(t / o)
    return 1.0
# ---- opening: trigger K00 -> blink -> K00 -> eyes close ... open on the moving walk-in
K = cv2.resize(cv2.imread('../images/23.jpg'), (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
c0 = load('g1c_cl.mp4', 0.0, 0.1, True)[1][0].astype(np.float32)
gain = (c0.reshape(-1, 3).mean(0) / K.reshape(-1, 3).mean(0))   # match the clip's tone so the reopen is seamless
wr = Writer('opening')
for i in range(int(round(1.45 * FPS))):
    t = i / FPS; Kt = K * (1 + (gain - 1) * ss((t - 0.7) / 0.6))
    op = bc(t, 0.65, 0.12, 0.08, 0.20) if t < 1.30 else bc(t, 1.30, 0.13, 1.0, 1.0)
    wr.w(eyelid(Kt, op, blur=(1 - op) * 3))
wr.w(np.zeros((H, W, 3), np.float32))
add(wr.close(), 'opening')

# ---- 1. floor clothes: walk in (clothes stay), push x2, turn right
P1 = [(0.0, 1.2, 2.1), (1.2, 2.6, 1.5), (2.6, 5.8, 3.4), (5.8, 7.4, 1.1), (7.4, 9.6, 2.6)]
def zoom(f, k, st):
    o = k / FPS
    o0 = np.searchsorted(st, 3.2) / FPS; o1 = np.searchsorted(st, 5.8) / FPS
    z = ss((o - (o0 - 0.5)) / 0.5) * ss(((o1 + 0.6) - o) / 0.6); s = 1 + 0.06 * z
    if s <= 1.0001: return f
    M = np.array([[s, 0, (1 - s) * W / 2], [0, s, (1 - s) * H * 0.35]], np.float32)
    return cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
add(retime('SEG1', 'g1c_cl.mp4', P1, ramp=0.45, lid_in=0.30, post=zoom), 'SEG1', ['SEG1'])
# ---- 2. wardrobe: look up slowly, cram the shirt; eyes close while still moving
add(retime('SEG2A', 'g2a2.mp4', [(1.0, 1.8, 2.0), (1.8, 4.2, 1.5), (4.2, 7.95, 3.4)], lid_out=0.18, black=0.06), 'SEG2A', ['SEG2A'])
# ---- 3. desk (eyes open on the moving hands)
add(retime('SEG2B', 'g2b.mp4', [(4.55, 9.9, 3.6)], lid_in=0.28), 'SEG2B', ['SEG2B'])
# ---- 4. notebook toss
add(retime('SEG3A', 'g3a.mp4', [(2.6, 4.0, 2.8), (4.0, 5.7, 1.2)]), 'SEG3A', ['SEG3A'])
# ---- 5. bed (dissolve over the swirl), eyes close at the end
a3 = retime('SEG3Ba', 'g3b.mp4', [(0.5, 1.05, 1.3)])
b3 = retime('SEG3Bb', 'g3b.mp4', [(1.85, 2.7, 1.0), (2.7, 4.3, 3.4), (4.3, 6.6, 2.4), (6.6, 9.95, 3.2)], lid_out=0.18, black=0.06)
add(xjoin('SEG3B', [a3, b3], 0.45), 'SEG3B', ['SEG3Ba', 'SEG3Bb'], 0.45)
# ---- 6. box (eyes open on the moving shove; hidden cut at 5.15 under a short dissolve)
a4 = retime('SEG4Aa', 'g4a_fix.mp4', [(3.05, 4.4, 3.0), (4.4, 5.2, 3.2)], lid_in=0.28)
b4 = retime('SEG4Ab', 'g4a_fix.mp4', [(5.1, 6.0, 3.2), (6.0, 7.4, 1.9), (7.4, 9.9, 3.6)])
add(xjoin('SEG4A', [a4, b4], 0.15), 'SEG4A', ['SEG4Aa', 'SEG4Ab'], 0.15)
# ---- 7. stand up, look at the perfect room
a5 = retime('SEG4Ba', 'g4b.mp4', [(0.0, 1.7, 1.9)])
b5 = retime('SEG4Bb', 'g4b.mp4', [(8.6, 10.0, 1.0)])
add(xjoin('SEG4B', [a5, b5], 0.6), 'SEG4B', ['SEG4Ba', 'SEG4Bb'], 0.6)
# ---- 8. 360: walk, turn, the heap, back round to the window
add(retime('R1', 'ru.mp4', [(1.5, 3.6, 3.6), (3.6, 6.3, 1.8)], ramp=0.35), 'R1_walk_turn', ['R1'])
add(retime('R2', 'r2.mp4', [(0.33, 4.4, 1.45), (4.4, 7.3, 1.0)], ramp=0.45), 'R2_turn_heap', ['R2'])
add(retime('R3', 'rv.mp4', [(0.7, 1.0, 1.0), (1.0, 7.5, 3.3)], ramp=0.4), 'R3_turn_to_desk', ['R3'])
a6 = retime('R4a', 'ry.mp4', [(0.0, 1.4, 1.4)])
b6 = retime('R4c', 'ry.mp4', [(2.75, 5.5, 2.0), (5.5, 6.4, 1.0)], ramp=0.4)
add(xjoin('R4', [a6, b6], 0.6), 'R4_turn_window_step_back', ['R4a', 'R4c'], 0.6)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'seg2/s26_ending.mp4', '-t', '3.2'] + E + [f'{D}/ending.mp4'], check=True)
add(f'{D}/ending.mp4', 'ending_blinks_black')
json.dump({'segs': segs, 'comp': COMP, 'maps': MAPS}, open('timeline11.json', 'w'), ensure_ascii=False)
print('sum', round(sum(s[1] for s in segs), 2))
