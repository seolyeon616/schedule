"""Final: speed ramps (slow on camera turns, faster on hand work), blink cuts instead of whip turns."""
import subprocess, json, os, numpy as np, cv2
D = 'seg9'; os.makedirs(D, exist_ok=True)
FPS, W, H = 24, 1920, 1080
SW = ['-sws_flags', 'lanczos+accurate_rnd+full_chroma_int+full_chroma_inp']
E = ['-an'] + SW + ['-c:v', 'libx264', '-crf', '15', '-pix_fmt', 'yuv420p', '-r', '24']
CROP = 'crop=iw*0.988:ih*0.988,scale=1920:1080:flags=lanczos'
def dur(p): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)

def piece(name, src, t0, t1, sp, crop=True):
    out = f'{D}/{name}.mp4'
    tm = min(int(round(sp)), 3) if sp >= 1.6 else 1
    vf = f'setpts=PTS/{sp}' + (f',tmix=frames={tm}' if tm > 1 else '') + ',fps=24,' + (CROP if crop else 'scale=1920:1080:flags=lanczos')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t0:.3f}', '-t', f'{t1 - t0:.3f}', '-i', src] + SW + ['-vf', vf] + E + [out], check=True)
    return out

def chain(name, src, parts, crop=True):
    """parts: list of (t0, t1, speed) on one source -> one continuous clip"""
    files = [piece(f'{name}_{i}', src, a, b, s, crop) for i, (a, b, s) in enumerate(parts)]
    lst = f'{D}/{name}.txt'; open(lst, 'w').write(''.join(f"file '{os.path.basename(f)}'\n" for f in files))
    out = f'{D}/{name}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst] + E + [out], check=True)
    return out

def xjoin(name, files, xf):
    cur = files[0]
    for k, nx in enumerate(files[1:]):
        off = dur(cur) - xf; out = f'{D}/{name}_x{k}.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', cur, '-i', nx, '-filter_complex', f'[0:v][1:v]xfade=transition=fade:duration={xf}:offset={off:.4f},format=yuv420p'] + E + [out], check=True)
        cur = out
    return cur

def grab(src, t, crop=True):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', src] + SW + ['-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], capture_output=True).stdout
    h, w = (1080, 1920) if len(raw) == 1080 * 1920 * 3 else (720, 1280)
    f = np.frombuffer(raw, np.uint8).reshape(h, w, 3)
    if crop:
        cy, cx = int(h * 0.006) + 1, int(w * 0.006) + 1; f = f[cy:h - cy, cx:w - cx]
    return cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)

YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
def eyelid(f, op, blur=0.0):
    if blur > 0: f = cv2.GaussianBlur(f, (0, 0), blur)
    if op >= 0.999: return f
    if op <= 0.001: return np.zeros_like(f)
    ry = op * H * 0.72 + 1; rx = W * 0.78
    d = ((XX - W / 2) / rx) ** 2 + ((YY - H / 2) / ry) ** 2
    m = np.clip((1 - d) / (0.08 + 0.25 * (1 - op)), 0, 1)
    return f * m[..., None] * (0.75 + 0.25 * op)
def bc(t, t0, c, h, o):
    if t < t0: return 1.0
    t -= t0
    if t < c: x = t / c; return 1 - x * x * (3 - 2 * x)
    t -= c
    if t < h: return 0.0
    t -= h
    if t < o: x = t / o; return x * x * (3 - 2 * x)
    return 1.0
def write(name, frames):
    out = f'{D}/{name}.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '24', '-i', '-'] + E + [out], stdin=subprocess.PIPE)
    for f in frames: p.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait(); return out
def blink(name, A, B, hold_a=0.10, hold_b=0.06):
    """A holds briefly, eyelids close (0.14s), stay shut (0.06s), open on B (0.24s)"""
    fr = []; T = hold_a + 0.14 + 0.06 + 0.24 + hold_b
    for i in range(int(round(T * FPS))):
        t = i / FPS; op = bc(t, hold_a, 0.14, 0.06, 0.24)
        fr.append(eyelid(A if t < hold_a + 0.17 else B, op, blur=(1 - op) * 3))
    return write(name, fr)

segs = []
def add(p, l): segs.append((p, dur(p), l)); print(f'{l:26s} {segs[-1][1]:5.2f}', flush=True)

# opening (unchanged, QC'd): trigger -> blink -> same room -> short blink -> one-take starts
add('seg5/opening5.mp4', 'opening')
# 1. floor clothes x2: slow walk-in, quicker pushes, SLOW right turn
p = chain('SEG1', 'g1c_fix.mp4', [(0.5, 2.6, 1.8), (2.6, 5.8, 2.4), (5.8, 7.4, 1.0), (7.4, 9.6, 2.6)])
# push-in 6% while the grey corner slabs are visible (src 3.6-5.4)
segmap = [(0.5, 2.6, 1.8), (2.6, 5.8, 2.4), (5.8, 7.4, 1.0), (7.4, 9.6, 2.6)]
def src_t(o):
    for a, b, s in segmap:
        d = (b - a) / s
        if o < d: return a + o * s
        o -= d
    return segmap[-1][1]
cap = cv2.VideoCapture(p); fr = []
i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    o = i / FPS
    def out_t(src):
        acc = 0
        for a, b, sp in segmap:
            if src <= b: return acc + (src - a) / sp
            acc += (b - a) / sp
        return acc
    o0, o1 = out_t(3.2), out_t(5.8)
    k = np.clip((o - (o0 - 0.5)) / 0.5, 0, 1) * np.clip(((o1 + 0.6) - o) / 0.6, 0, 1); s = 1 + 0.06 * k
    M = np.array([[s, 0, (1 - s) * W / 2], [0, s, (1 - s) * H * 0.35]], np.float32)
    fr.append(cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT).astype(np.float32)); i += 1
add(write('SEG1z', fr), 'SEG1')
# 2. look up to wardrobe slowly, cram the shirt
add(chain('SEG2A', 'g2a2.mp4', [(1.0, 1.8, 2.0), (1.8, 4.2, 1.35), (4.2, 7.95, 2.6)]), 'SEG2A')
# 3. blink -> desk (avoids the wrong-room whip and the vanishing pens)
add(blink('blink_wardrobe_desk', grab('g2a2.mp4', 7.95), grab('g2b.mp4', 4.55)), 'blink_desk')
add(chain('SEG2B', 'g2b.mp4', [(4.55, 9.9, 3.0)]), 'SEG2B')
# 4. notebook toss (natural speed for the throw)
add(chain('SEG3A', 'g3a.mp4', [(2.6, 4.0, 2.5), (4.0, 5.7, 1.0)]), 'SEG3A')
# 5. bed: slow turn, sweater + duvet
a3 = chain('SEG3Ba', 'g3b.mp4', [(0.5, 1.05, 1.3)])
b3 = chain('SEG3Bb', 'g3b.mp4', [(1.85, 2.7, 1.0), (2.7, 4.3, 3.0), (4.3, 6.6, 2.0), (6.6, 9.95, 3.0)])
add(xjoin('SEG3B', [a3, b3], 0.45), 'SEG3B')
# 6. blink -> crouched by the nightstand, box shove
add(blink('blink_bed_box', grab('g3b.mp4', 9.95), grab('g4a_fix.mp4', 3.05)), 'blink_box')
a4 = chain('SEG4Aa', 'g4a_fix.mp4', [(3.05, 4.4, 2.5), (4.4, 5.2, 2.8)])
b4 = chain('SEG4Ab', 'g4a_fix.mp4', [(5.1, 6.0, 2.8), (6.0, 7.4, 1.5), (7.4, 9.9, 3.0)])
add(xjoin('SEG4A', [a4, b4], 0.15), 'SEG4A')
# 7. stand up and look at the perfect room (computed stand-up at natural speed)
a5 = chain('SEG4Ba', 'g4b.mp4', [(0.0, 1.7, 1.6)])
b5 = chain('SEG4Bb', 'g4b.mp4', [(8.6, 10.0, 1.0)])
add(xjoin('SEG4B', [a5, b5], 0.6), 'SEG4B')
# 8. 360: walk in, slow turn to wardrobe, keep turning, slow down at the door
add(chain('R1', 'ru.mp4', [(1.5, 3.6, 3.0), (3.6, 6.3, 1.6)]), 'R1_walk_turn')
add(chain('R2', 'r2.mp4', [(0.33, 2.5, 1.15), (2.5, 4.4, 1.15)]), 'R2_turn')
add(chain('HEAP', 'r2.mp4', [(4.4, 7.4, 1.0)]), 'HEAP_hold_sigh')
add(chain('R3', 'rv.mp4', [(0.7, 1.0, 1.0), (1.0, 7.5, 3.0)]), 'R3_turn_to_desk')
a6 = chain('R4a', 'ry.mp4', [(0.0, 1.4, 1.4)])
b6 = chain('R4c', 'ry.mp4', [(2.75, 5.5, 1.6), (5.5, 6.4, 1.0)])
add(xjoin('R4', [a6, b6], 0.6), 'R4_turn_window_step_back')
add('seg2/s26_ending.mp4', 'ending_blinks_black')
json.dump({'segs': segs}, open('timeline9.json', 'w'), ensure_ascii=False, indent=1)
print('sum', round(sum(s[1] for s in segs), 2))
