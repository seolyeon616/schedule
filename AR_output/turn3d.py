"""Head-turn from the clean front view (K07) to the heap (door wall), rendered from ONE fixed room model,
so the wardrobe / walls can never move or morph. Units: eye height = 1.
x right (towards wardrobe), y down, z forward (towards the window)."""
import cv2, numpy as np
W, H = 1920, 1080
FL = 1240.0
R, LW, ZF, ZB = 1.596, 3.22, 5.77, 4.26          # wardrobe face, left wall, front wall, back wall
FLOOR, CEIL = 1.0, -1.637
XH = -0.624                                       # heap-view camera is a little further from the wardrobe
F = cv2.imread('pano/F.png').astype(np.float32)
HP = cv2.imread('pano/heap_plus.png' if __import__('os').path.exists('pano/heap_plus.png') else 'pano/heap.png').astype(np.float32)
S = cv2.imread('pano/S.png').astype(np.float32)
# wardrobe tile: one double-door unit without sun streaks (S x 1453..1784), full wall height 127..853
UNIT = S[127:854, 1453:1785].copy(); UW = 1.2                     # two doors = 1.2 eye heights
FLOOR_C = np.median(F[950:1080, 1000:1300].reshape(-1, 3), 0)
CEIL_C = np.median(S[0:90, 600:1300].reshape(-1, 3), 0)
LINE_C = np.array([150, 150, 155], np.float32)
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)

def feather(u, v, w=W, h=H, m=70.0):
    return np.clip(np.minimum(np.minimum(u, w - 1 - u), np.minimum(v, h - 1 - v)) / m, 0, 1)

def render(yaw_deg, pos, cx, cy, pitch=0.0):
    th = np.radians(yaw_deg); fw = np.array([np.sin(th), 0, np.cos(th)]); rt = np.array([np.cos(th), 0, -np.sin(th)]); dn = np.array([0, 1.0, 0])
    if pitch:
        p = np.radians(pitch); fw, dn = fw * np.cos(p) - dn * np.sin(p), dn * np.cos(p) + fw * np.sin(p)
    a = (XX - cx) / FL; b = (YY - cy) / FL
    dx = rt[0] * a + dn[0] * b + fw[0]; dy = rt[1] * a + dn[1] * b + fw[1]; dz = rt[2] * a + dn[2] * b + fw[2]
    px, py, pz = pos
    big = np.float32(1e9); t = np.full((H, W), big, np.float32); kind = np.zeros((H, W), np.uint8)
    for k, (d, p0, plane) in enumerate([(dx, px, R), (dx, px, -LW), (dy, py, FLOOR), (dy, py, CEIL), (dz, pz, ZF), (dz, pz, -ZB)]):
        with np.errstate(divide='ignore', invalid='ignore'):
            tt = (plane - p0) / d
        ok = (tt > 1e-4) & (tt < t)
        t = np.where(ok, tt, t); kind = np.where(ok, k, kind)
    X = px + dx * t; Y = py + dy * t; Z = pz + dz * t
    # ---- base layer: wardrobe tiles on the right wall, procedural floor / ceiling / plain walls
    base = np.empty((H, W, 3), np.float32); base[:] = (FLOOR_C + CEIL_C) / 2
    m = kind == 0
    u = ((3.90 - Z) / UW % 1.0) * (UNIT.shape[1] - 1); v = (Y - CEIL) / (FLOOR - CEIL) * (UNIT.shape[0] - 1)
    tile = cv2.remap(UNIT, u.astype(np.float32), v.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    base[m] = tile[m]
    m = kind == 2
    # floor: soft tiles (0.9 units), anti-aliased seams scaled by pixel footprint
    fx, fz = X / 0.9, Z / 0.9
    fp = np.maximum(t / FL / 0.9 * 1.5, 1e-3)
    seam = np.maximum(np.clip(1 - np.abs(fx - np.round(fx)) / fp, 0, 1), np.clip(1 - np.abs(fz - np.round(fz)) / fp, 0, 1)) * 0.35
    fl = FLOOR_C[None, None, :] * (1 - seam[..., None]) + LINE_C * seam[..., None]
    base[m] = fl[m]
    m = kind == 3
    lights = np.zeros((H, W), np.float32)
    for lx, lz in [(-0.8, 3.0), (-0.8, 0.0), (-0.8, -3.0)]:
        r = np.hypot(X - lx, Z - lz); fpx = np.maximum(t / FL * 1.5, 1e-3)
        lights = np.maximum(lights, np.clip(1 - np.abs(r - 0.13) / fpx, 0, 1))
    ce = CEIL_C[None, None, :] * (1 - 0.5 * lights[..., None]) + LINE_C * 0.5 * lights[..., None]
    base[m] = ce[m]
    for kk in (1, 4, 5):
        m = kind == kk; base[m] = CEIL_C * 0.98
    # ---- projective layers: the real images where their camera saw the surface
    out = base
    # heap view (camera at (XH,0,0) facing -z)
    Zl = -(Z - 0.0); Xl = -(X - XH)
    with np.errstate(divide='ignore', invalid='ignore'):
        uh = 960 + FL * Xl / Zl; vh = 546 + FL * Y / Zl
    wh = np.where(Zl > 0.05, feather(uh, vh), 0).astype(np.float32)
    if wh.max() > 0:
        smp = cv2.remap(HP, np.nan_to_num(uh).astype(np.float32), np.nan_to_num(vh).astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        out = out * (1 - wh[..., None]) + smp * wh[..., None]
    # front view (camera at origin facing +z)
    with np.errstate(divide='ignore', invalid='ignore'):
        uf = 1013 + FL * X / Z; vf = 485 + FL * Y / Z
    wf = np.where(Z > 0.05, feather(uf, vf), 0).astype(np.float32)
    if wf.max() > 0:
        smp = cv2.remap(F, np.nan_to_num(uf).astype(np.float32), np.nan_to_num(vf).astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        out = out * (1 - wf[..., None]) + smp * wf[..., None]
    return out

if __name__ == '__main__':
    tiles = []
    for k, yaw in enumerate([0, 25, 50, 75, 100, 125, 150, 180]):
        s = yaw / 180; s = s * s * (3 - 2 * s)
        im = render(yaw, (XH * s, 0, 0), 1013 + (960 - 1013) * s, 485 + (546 - 485) * s)
        tiles.append(cv2.resize(np.clip(im, 0, 255).astype(np.uint8), (480, 270)))
    cv2.imwrite('turn_test.jpg', np.vstack([np.hstack(tiles[:4]), np.hstack(tiles[4:])]))
