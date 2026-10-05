"""Show the wardrobe stuffed with clothes: paint a crammed stack of folded clothes into the open door gap of the
Flow clip. The stack is anchored to the wardrobe (tracked homography), hand and the orange shirt stay in front."""
import cv2, numpy as np, subprocess
F = np.load('w_new.npy'); N = len(F); H_, W_ = 720, 1280
CAN = 72                                                   # canonical frame (3.0 s, camera settled close)
rng = np.random.default_rng(4)

def gapmask(f):
    g = cv2.cvtColor(f, 6); s = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)[..., 1]
    m = ((g > 60) & (g < 150) & (s < 32)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 41)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    keep = [k for k in range(1, n) if st[k, 3] > 60 and st[k, 2] < 220 and st[k, 4] > 900]
    if not keep: return np.zeros((H_, W_), np.float32), None
    big = max(keep, key=lambda k: st[k, 4]); bx = st[big, 0] + st[big, 2] / 2
    keep = [k for k in keep if abs(st[k, 0] + st[k, 2] / 2 - bx) < 60]     # all pieces of the same gap (split by the hand)
    k = big; m = np.isin(lab, keep).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    return m.astype(np.float32), st[k]

# ---- track the wardrobe: homography canonical -> frame i (chained, saturated shirt + moving hand are outliers)
sift = cv2.SIFT_create(3000)
def feats(f):
    s = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)[..., 1]; msk = (s < 40).astype(np.uint8) * 255
    return sift.detectAndCompute(cv2.cvtColor(f, 6), msk)
KD = [feats(f) for f in F]
def pairH(a, b):
    (ka, da), (kb, db) = KD[a], KD[b]
    if da is None or db is None: return np.eye(3)
    m = cv2.BFMatcher().knnMatch(da, db, k=2); g = [x for x, y in m if x.distance < 0.72 * y.distance]
    if len(g) < 12: return np.eye(3)
    P = np.float32([ka[x.queryIdx].pt for x in g]); Q = np.float32([kb[x.trainIdx].pt for x in g])
    Hm, _ = cv2.findHomography(P, Q, cv2.RANSAC, 3); return Hm if Hm is not None else np.eye(3)
Hs = [None] * N; Hs[CAN] = np.eye(3)
for i in range(CAN + 1, N): Hs[i] = pairH(i - 1, i) @ Hs[i - 1]
for i in range(CAN - 1, -1, -1): Hs[i] = pairH(i + 1, i) @ Hs[i + 1]
# smooth via corner tracks
C = np.float32([[300, 100], [980, 100], [980, 620], [300, 620]])
P = np.array([cv2.perspectiveTransform(C[None], h)[0] for h in Hs])
r = 3; k = np.exp(-0.5 * (np.arange(-r * 2, r * 2 + 1) / r) ** 2); k /= k.sum()
Pp = np.concatenate([np.repeat(P[:1], 2 * r, 0), P, np.repeat(P[-1:], 2 * r, 0)])
Ps = np.stack([np.tensordot(k, Pp[i:i + 4 * r + 1], axes=(0, 0)) for i in range(N)])
Hs = [cv2.getPerspectiveTransform(C, Ps[i].astype(np.float32)) for i in range(N)]

# ---- the crammed clothes, drawn once in canonical coordinates (pencil line-art, muted colours)
mC, stC = gapmask(F[CAN]); x0 = stC[0] - 220; x1 = stC[0] + stC[2] + 220
SS = 2; TW, TH = (x1 - x0) * SS, H_ * SS
tex = np.zeros((TH, TW, 3), np.float32)
cols = [(112, 72, 52), (62, 148, 196), (78, 122, 112), (150, 140, 205), (172, 198, 222), (212, 186, 150),
        (156, 156, 160), (66, 66, 128), (120, 170, 140), (200, 200, 205), (90, 110, 175)]
xx = np.arange(TW, dtype=np.float32)
y = -40.0 * SS; prev = np.full(TW, y, np.float32); li = 0
layers = []
while y < TH + 60:
    h = rng.uniform(26, 62) * SS
    ph1, ph2, a1 = rng.uniform(0, 6.3), rng.uniform(0, 6.3), rng.uniform(3, 9) * SS
    nxt = y + h + a1 * np.sin(xx / (rng.uniform(35, 70) * SS) + ph1) + 0.4 * a1 * np.sin(xx / (rng.uniform(9, 18) * SS) + ph2)
    layers.append((prev.copy(), nxt.copy(), cols[li % len(cols)] if rng.random() > 0.12 else cols[rng.integers(len(cols))]))
    prev = np.maximum(nxt, prev + 6 * SS); y += h; li += 1
YY = np.arange(TH, dtype=np.float32)[:, None]
for top, bot, c in layers:
    inside = (YY >= top[None]) & (YY < bot[None])
    u = np.clip((YY - top[None]) / np.maximum(bot - top, 1)[None], 0, 1)
    shade = 0.80 + 0.28 * np.sin(np.pi * np.clip(u * 1.1, 0, 1)) - 0.22 * np.clip((u - 0.75) / 0.25, 0, 1)   # rounded folded edge
    tex[inside] = (np.array(c, np.float32)[None, None] * shade[..., None])[inside]
line = np.zeros((TH, TW), np.uint8)
for top, bot, c in layers:
    pts = np.stack([xx, bot], 1).astype(np.int32); cv2.polylines(line, [pts], False, 255, int(2.2 * SS), cv2.LINE_AA)
    for _ in range(rng.integers(1, 4)):                     # fold creases
        cx = rng.uniform(0, TW); L = rng.uniform(25, 70) * SS; cy = (top[int(min(cx, TW - 1))] + bot[int(min(cx, TW - 1))]) / 2
        cv2.line(line, (int(cx), int(cy)), (int(cx + L), int(cy + rng.uniform(-4, 4) * SS)), 150, int(1.3 * SS), cv2.LINE_AA)
lf = cv2.GaussianBlur(line, (0, 0), 0.6).astype(np.float32)[..., None] / 255
tex = tex * (1 - lf) + np.array([58, 58, 64], np.float32) * lf
gry = tex.mean(2, keepdims=True); tex = tex * 0.72 + gry * 0.28          # softer, closer to the drawing's palette
tex = cv2.resize(tex, (x1 - x0, H_), interpolation=cv2.INTER_AREA)
TEX = np.zeros((H_, W_, 3), np.float32); TEX[:, max(x0, 0):min(x1, W_)] = tex[:, max(0, -x0):(x1 - x0) - max(0, x1 - W_)]
VAL = np.zeros((H_, W_), np.float32); VAL[:, max(x0, 0):min(x1, W_)] = 1

out = []
for i in range(N):
    f = F[i].astype(np.float32); m, st = gapmask(F[i])
    if st is not None:
        T = cv2.warpPerspective(TEX, Hs[i], (W_, H_), flags=cv2.INTER_LINEAR)
        V = cv2.warpPerspective(VAL, Hs[i], (W_, H_), flags=cv2.INTER_NEAREST)
        a = cv2.GaussianBlur(m * V, (0, 0), 1.0)[..., None]
        # inside the wardrobe is in shadow: darker towards the door edges (ambient occlusion)
        d = cv2.distanceTransform((m * 255).astype(np.uint8), cv2.DIST_L2, 5)
        ao = (0.62 + 0.30 * np.clip(d / 18.0, 0, 1))[..., None]
        f = f * (1 - a) + T * ao * a
    out.append(np.clip(f, 0, 255).astype(np.uint8))
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W_}x{H_}', '-r', '24', '-i', '-',
                        '-sws_flags', 'lanczos+accurate_rnd+full_chroma_int+full_chroma_inp', '-c:v', 'libx264', '-crf', '12', '-pix_fmt', 'yuv420p', 'w_new_full.mp4'], stdin=subprocess.PIPE)
for f in out: enc.stdin.write(f.tobytes())
enc.stdin.close(); enc.wait()
cv2.imwrite('w_fill_prev.jpg', np.hstack([out[i][60:700, 380:860] for i in (0, 30, 48, 96, 144, 160, 176)]))
print('done')
