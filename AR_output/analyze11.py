import subprocess, numpy as np, json, sys
f = sys.argv[1]; T = json.load(open(sys.argv[2])); tl = T['marks']
lids = [tuple(x) for x in T.get('lids', [])]
w, h = 320, 180
G = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-vf', f'scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout, np.uint8).reshape(-1, h, w).astype(np.float32)
n = len(G)
def shift(a, b):
    A = np.fft.fft2(a - a.mean()); B = np.fft.fft2(b - b.mean()); R = A * np.conj(B); R /= np.abs(R) + 1e-6; r = np.abs(np.fft.ifft2(R))
    y, x = np.unravel_index(r.argmax(), r.shape); return (x if x < w // 2 else x - w), (y if y < h // 2 else y - h)
pan = np.zeros(n); diff = np.zeros(n); bri = G.mean((1, 2))
for i in range(1, n):
    dx, dy = shift(G[i - 1], G[i]); pan[i] = np.hypot(dx, dy) * 1920 / w; diff[i] = np.abs(G[i] - G[i - 1]).mean()
# robust speed: median of 3 to ignore single-frame correlation glitches; jerk = change of speed per frame
ps = np.array([np.median(pan[max(i - 1, 0):i + 2]) for i in range(n)]); jerk = np.abs(np.diff(ps, prepend=ps[0]))
def seg(t): return [k for k, (a, b) in tl.items() if a <= t < b + 1e-6][-1]
def excluded(t): return t < tl['opening'][1] + 0.05 or t > tl['ending_blinks_black'][0] + 0.15 or any(a <= t <= b for a, b in lids)
rows = []
for b in range(int(n / 2.4)):
    i0, i1 = int(b * 2.4), int((b + 1) * 2.4) + 1; t = b / 10
    p = pan[i0:i1].max(); d = diff[i0:i1].max(); db = np.abs(np.diff(bri[i0:i1])).max(); j = jerk[i0:i1].max()
    fl = []
    if not excluded(t):
        if p > 45: fl.append(f'FAST-PAN {p:.0f}')
        if d > 14: fl.append(f'JUMP {d:.1f}')
        if db > 6: fl.append(f'FLASH {db:.1f}')
        if j > 22: fl.append(f'JERK {j:.0f}')
    rows.append((t, seg(t), p, d, db, j, fl))
bad = [r for r in rows if r[6]]
ok = [r for r in rows if not excluded(r[0])]
print(f'{f}: windows {len(rows)} flagged {len(bad)} | mean jerk {np.mean([r[5] for r in ok]):.1f} p95 jerk {np.percentile([r[5] for r in ok], 95):.1f} max pan {max(r[2] for r in ok):.0f}')
if '-v' in sys.argv:
    for r in bad: print(f'{r[0]:5.1f}s {r[1]:24s} pan {r[2]:4.0f} diff {r[3]:5.1f} dbri {r[4]:4.1f} jerk {r[5]:4.0f}  {", ".join(r[6])}')
