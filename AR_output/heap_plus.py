import cv2, numpy as np
rng = np.random.default_rng(11)
im = cv2.imread('pano/heap.png').astype(np.float32); Hh, Ww = im.shape[:2]
FL, CX, CY = 1240.0, 960.0, 546.0
def proj(X, Z): return np.stack([CX + FL * X / Z, CY + FL * 1.0 / Z], -1)   # floor point (eye height 1) -> image
SS = 3
def draw_sheet(img, X, Z, w, h, ang, tint=(246,246,248), curl=0.0, lines=True):
    c, s = np.cos(ang), np.sin(ang)
    pts = np.array([[-w/2, -h/2], [w/2, -h/2], [w/2, h/2], [-w/2, h/2]])
    P = np.array([[X + x * c - y * s, Z + x * s + y * c] for x, y in pts])
    uv = proj(P[:, 0], P[:, 1]).astype(np.float32)
    # soft contact shadow
    sh = np.zeros((Hh, Ww), np.float32); cv2.fillConvexPoly(sh, (uv + [3, 4]).astype(np.int32), 1.0, lineType=cv2.LINE_AA)
    sh = cv2.GaussianBlur(sh, (0, 0), 5) * 0.10
    img *= (1 - sh[..., None])
    big = np.zeros((Hh * SS, Ww * SS), np.uint8); cv2.fillConvexPoly(big, (uv * SS).astype(np.int32), 255, lineType=cv2.LINE_AA)
    a = cv2.resize(big, (Ww, Hh), interpolation=cv2.INTER_AREA).astype(np.float32)[..., None] / 255
    shade = np.array(tint, np.float32) * 0.6 + np.array([242, 242, 244], np.float32) * 0.4 - 6 * curl
    img[:] = img * (1 - a) + shade * a
    ol = np.zeros((Hh * SS, Ww * SS), np.uint8); cv2.polylines(ol, [(uv * SS).astype(np.int32)], True, 255, int(1.6 * SS), cv2.LINE_AA)
    if lines:   # a few printed text lines
        for k in range(4):
            t0 = 0.22 + 0.13 * k
            a0 = np.array([X + (-w/2 + 0.07) * c - (-h/2 + t0 * h) * s, Z + (-w/2 + 0.07) * s + (-h/2 + t0 * h) * c])
            a1 = np.array([X + (w/2 - 0.07 - 0.05 * (k % 2)) * c - (-h/2 + t0 * h) * s, Z + (w/2 - 0.07 - 0.05 * (k % 2)) * s + (-h/2 + t0 * h) * c])
            p0, p1 = proj(*a0), proj(*a1)
            cv2.line(ol, tuple((p0 * SS).astype(int)), tuple((p1 * SS).astype(int)), 110, int(0.9 * SS), cv2.LINE_AA)
    o = cv2.resize(ol, (Ww, Hh), interpolation=cv2.INTER_AREA).astype(np.float32)[..., None] / 255
    img[:] = img * (1 - o * 0.75) + np.array([70, 70, 74], np.float32) * o * 0.75
def draw_ball(img, X, Z, r):   # crumpled paper ball
    u, v = proj(X, Z); R = FL * r / Z
    sh = np.zeros((Hh, Ww), np.float32); cv2.ellipse(sh, (int(u + 4), int(v + 2)), (int(R * 1.1), int(R * 0.35)), 0, 0, 360, 1, -1, cv2.LINE_AA)
    img *= (1 - cv2.GaussianBlur(sh, (0, 0), 4)[..., None] * 0.12)
    cv2.circle(img, (int(u), int(v - R * 0.8)), int(R), (242, 242, 244), -1, cv2.LINE_AA)
    for k in range(7):
        a0 = rng.uniform(0, 2 * np.pi); a1 = a0 + rng.uniform(0.6, 1.4); rr = R * rng.uniform(0.3, 0.95)
        cv2.ellipse(img, (int(u), int(v - R * 0.8)), (int(rr), int(rr * 0.7)), np.degrees(a0), 0, np.degrees(a1 - a0), (95, 95, 100), 1, cv2.LINE_AA)
    cv2.circle(img, (int(u), int(v - R * 0.8)), int(R), (70, 70, 74), 2, cv2.LINE_AA)
# scattered sheets around the heap (left, right, front), irregular angles
Y_, B_, P_, G_ = (150, 222, 246), (238, 205, 160), (196, 180, 240), (170, 222, 190)   # BGR pastel paper colours
for X, Z, ang, tint in [(-1.55, 3.05, 0.5, Y_), (-1.05, 2.55, -0.35, B_), (-1.9, 2.75, 1.1, P_), (1.25, 2.85, -0.7, Y_),
                        (1.75, 3.25, 0.25, G_), (0.75, 2.3, 0.95, B_), (-0.35, 2.22, -0.15, P_)]:
    draw_sheet(im, X, Z, 0.30, 0.40, ang, tint)
cv2.imwrite('pano/heap_plus.png', np.clip(im, 0, 255).astype(np.uint8))
cv2.imwrite('heap_plus_prev.jpg', cv2.resize(np.clip(im, 0, 255).astype(np.uint8), (1440, 810)))
