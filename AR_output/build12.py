"""v12 (client revision): slower breathing between actions, tidy = slow & meticulous / procrastinate = fast & careless,
shirt already in the wardrobe gap, laptop re-adjusted, book flung away, stare at the clean room -> rustle -> pause ->
slow head turn rendered from ONE fixed room model (nothing in the room moves) -> heap reveal -> stare -> ending on the heap."""
import json, numpy as np, cv2
src = open('build11.py').read()
exec(src[:src.index("segs = []; COMP = {}")].replace("D = 'seg11'", "D = 'seg12'"))
import turn3d
from turn3d import render, XH

segs = []; COMP = {}; EXTRA = {}
def add(p, l, chains=(), xj=0.0):
    segs.append((p, dur(p), l)); COMP[l] = {'chains': list(chains), 'xj': xj}
    print(f'{l:26s} {segs[-1][1]:5.2f}', flush=True)

# ---- 0. opening (QC'd in v11)
add('seg11/opening.mp4', 'opening')
# ---- 1. floor clothes: slow walk-in, careless pushes, look right, second push
P1 = [(0.0, 1.2, 1.6), (1.2, 2.6, 1.2), (2.6, 5.8, 3.0), (5.8, 7.4, 1.0), (7.4, 9.6, 2.7)]
def zoom(f, k, st):
    o = k / FPS
    o0 = np.searchsorted(st, 3.2) / FPS; o1 = np.searchsorted(st, 5.8) / FPS
    z = ss((o - (o0 - 0.5)) / 0.5) * ss(((o1 + 0.6) - o) / 0.6); s = 1 + 0.06 * z
    if s <= 1.0001: return f
    M = np.array([[s, 0, (1 - s) * W / 2], [0, s, (1 - s) * H * 0.35]], np.float32)
    return cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
add(retime('SEG1', 'g1c_cl.mp4', P1, ramp=0.45, lid_in=0.30, post=zoom), 'SEG1', ['SEG1'])
# ---- 2. wardrobe: the shirt is already sticking out of the gap; look up, notice it, cram it in carelessly
add(retime('SEG2A', 'g2a2_cl.mp4', [(1.45, 2.4, 1.6), (2.4, 3.9, 1.2), (3.9, 4.7, 1.0), (4.7, 7.95, 2.5)], ramp=0.4,
           lid_out=0.18, black=0.06), 'SEG2A', ['SEG2A'])
# ---- 3. desk, perfectionist: laptop aligned slowly, nudged back and re-aligned twice
LAP = [(0.0, 6.62), (1.25, 7.05), (1.8, 7.20), (2.25, 7.09), (2.75, 7.22), (3.1, 7.15), (3.55, 7.24), (3.62, 7.24)]
add(retime('DESK_LAP', 'g2b.mp4', path=LAP, lid_in=0.28), 'DESK_LAP', ['DESK_LAP'])
# ---- 4. desk, procrastinator: the book is flung off-screen without hesitation
add(retime('DESK_TOSS', 'g3a.mp4', [(2.6, 3.1, 1.3), (3.1, 5.5, 1.25)], ramp=0.3), 'DESK_TOSS', ['DESK_TOSS'])
# ---- 5. bed: sweater thrown fast, duvet smoothed slowly
a3 = retime('SEG3Ba', 'g3b.mp4', [(0.5, 1.05, 1.3)])
b3 = retime('SEG3Bb', 'g3b.mp4', [(1.85, 2.7, 1.0), (2.7, 4.3, 2.8), (4.3, 5.3, 1.3), (5.3, 9.95, 1.9)], ramp=0.35, lid_out=0.18, black=0.06)
add(xjoin('SEG3B', [a3, b3], 0.45), 'SEG3B', ['SEG3Ba', 'SEG3Bb'], 0.45)
# ---- 6. box shoved away
a4 = retime('SEG4Aa', 'g4a_fix.mp4', [(3.05, 4.4, 3.0), (4.4, 5.2, 3.0)], lid_in=0.28)
b4 = retime('SEG4Ab', 'g4a_fix.mp4', [(5.1, 6.0, 2.4), (6.0, 7.4, 1.3), (7.4, 9.9, 3.0)])
add(xjoin('SEG4A', [a4, b4], 0.15), 'SEG4A', ['SEG4Aa', 'SEG4Ab'], 0.15)
# ---- 7. stand up
a5 = retime('SEG4Ba', 'g4b.mp4', [(0.0, 1.7, 2.0)])
b5 = retime('SEG4Bb', 'g4b.mp4', [(8.6, 10.0, 1.0)])
add(xjoin('SEG4B', [a5, b5], 0.6), 'SEG4B', ['SEG4Ba', 'SEG4Bb'], 0.6)

# ---- 8. stare at the perfect room -> rustle off-screen -> gaze stops -> slow turn -> heap
A = cv2.imread('pano/g4b_end.png').astype(np.float32); Hg = np.load('H_g4b_to_F.npy')
def lerpH(s):   # identity -> Hg
    C = np.float32([[0, 0], [W, 0], [W, H], [0, H]]); D_ = cv2.perspectiveTransform(C[None], Hg)[0]
    return cv2.getPerspectiveTransform(C, (C * (1 - s) + D_ * s).astype(np.float32))
T_IN, T_STARE, T_RUSTLE, T_TURN = 0.5, 1.7, 0.9, 6.4
RUSTLE_AT = T_IN + T_STARE          # output time of the off-screen "바스락" within STARE
wr = Writer('STARE'); n = int(round((T_IN + T_STARE + T_RUSTLE) * FPS)); yaw_end = 0.0
for k in range(n):
    t = k / FPS
    amp = ss(t / 1.0) * (1 - ss((t - RUSTLE_AT) / 0.25))           # breathing; freezes when the sound comes
    yb = 0.30 * np.sin(2 * np.pi * min(t, RUSTLE_AT + 0.2) / 3.4) * amp
    pb = 0.20 * np.sin(2 * np.pi * min(t, RUSTLE_AT + 0.2) / 2.7 + 0.8) * amp
    look = 2.5 * ss((t - RUSTLE_AT - 0.35) / 0.5)                   # eyes drift a little towards the sound, then hold
    yaw = yb + look; yaw_end = yaw
    f = render(yaw, (0, 0, 0), 1013, 485, pitch=pb)
    if t < T_IN:            # the stand-up shot ends on (almost) this exact view: tiny homography cross-blend
        s = ss(t / T_IN); Aw = cv2.warpPerspective(A, lerpH(1.0), (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
        Aw = cv2.warpPerspective(A, lerpH(s), (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
        f = Aw * (1 - s) + f * s
    wr.w(f)
add(wr.close(), 'STARE_clean_room')
EXTRA['rustle'] = RUSTLE_AT
# slow head turn: yaw_end -> 180, camera drifts to the heap-view position, motion blur by sub-frames
import os
TURN_CACHED = os.path.exists(f'{D}/TURN.mp4') and os.environ.get('REDO_TURN') != '1'
wr = Writer('TURN_tmp') if TURN_CACHED else Writer('TURN'); n = 0 if TURN_CACHED else int(round(T_TURN * FPS))
# speed profile: gentle 1.5 s start, steady slow middle, long 1.9 s settle (no fast peak)
_tt = np.linspace(0, T_TURN, 4001); TA, TD = 1.5, 1.9
_v = np.where(_tt < TA, 0.5 - 0.5 * np.cos(np.pi * _tt / TA), np.where(_tt > T_TURN - TD, 0.5 - 0.5 * np.cos(np.pi * (T_TURN - _tt) / TD), 1.0))
_e = np.concatenate([[0], np.cumsum((_v[1:] + _v[:-1]) / 2 * np.diff(_tt))]); _e /= _e[-1]
def yaw_at(t):
    e = float(np.interp(t, _tt, _e))
    return yaw_end + (180 - yaw_end) * e, e
for k in range(n):
    t = k / FPS; y0, _ = yaw_at(t); y1, _ = yaw_at(t + 1 / FPS)
    sub = int(min(max(np.ceil(abs(y1 - y0) / 0.7), 1), 5)); acc = 0
    for q in range(sub):
        tt = t + (q + 0.5) / sub / FPS * 0.8 - 0.4 / FPS
        y, e = yaw_at(tt); pitch = 1.2 * np.sin(np.pi * e)            # head dips a little mid-turn
        acc = acc + render(y, (XH * e, 0, 0), 1013 + (960 - 1013) * e, 485 + (546 - 485) * e, pitch=pitch)
    wr.w(acc / sub)
wr.close(); add(f'{D}/TURN.mp4', 'TURN_to_heap')
# ---- 9. heap: stand still and stare (breathing only), then the ending on the heap
HP = cv2.imread('pano/heap_plus.png').astype(np.float32)
def breathe(img, t, amp, zoom=1.0, blur=0.0):
    dx = 3.0 * np.sin(2 * np.pi * t / 3.6) * amp; dy = 2.0 * np.sin(2 * np.pi * t / 2.8 + 0.6) * amp
    M = np.array([[zoom, 0, (1 - zoom) * W / 2 + dx], [0, zoom, (1 - zoom) * H * 0.55 + dy]], np.float32)
    f = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return cv2.GaussianBlur(f, (0, 0), blur) if blur > 0.05 else f
T_HOLD = 2.4
wr = Writer('HEAP_hold'); n = int(round(T_HOLD * FPS))
for k in range(n):
    t = k / FPS; wr.w(breathe(HP, t, ss(t / 1.2), zoom=1 + 0.008 * t / T_HOLD))
add(wr.close(), 'HEAP_hold_sigh')
# ending (same timing as before so the sound design matches): blink, blink, blur + slow push-in + weak noise, eyes close
def bcurve(t, t0, c, h, o):
    if t < t0: return 1.0
    t -= t0
    if t < c: return 1 - ss(t / c)
    t -= c
    if t < h: return 0.0
    t -= h
    if t < o: return ss(t / o)
    return 1.0
rng = np.random.default_rng(5)
wr = Writer('ENDING'); n = int(round(3.2 * FPS))
for k in range(n):
    t = k / FPS; T0 = T_HOLD + t
    op = min(bcurve(t, 0.25, 0.12, 0.10, 0.22), bcurve(t, 1.05, 0.18, 0.16, 0.38), bcurve(t, 2.05, 0.70, 9, 1))
    g = ss((t - 1.2) / 1.0)
    f = breathe(HP, T0, 1.0, zoom=1.008 + 0.05 * ss((t - 0.9) / 2.0), blur=2.5 * g)
    if g > 0:
        nz = rng.standard_normal((H // 2, W // 2)).astype(np.float32); nz = cv2.resize(nz, (W, H), interpolation=cv2.INTER_NEAREST)
        f = f + nz[..., None] * 9 * g
    wr.w(eyelid(f, op, blur=(1 - op) * 3))
add(wr.close(), 'ending_blinks_black')
json.dump({'segs': segs, 'comp': COMP, 'maps': MAPS, 'extra': EXTRA}, open('timeline12.json', 'w'), ensure_ascii=False)
print('sum', round(sum(s[1] for s in segs), 2))
