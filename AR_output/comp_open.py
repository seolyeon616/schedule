import cv2, numpy as np, subprocess
F = np.load('g1c_head.npy'); N = len(F)
Hs = np.load('Hs_open.npy')
K = cv2.resize(cv2.imread('../images/23.jpg'),(1920,1080),interpolation=cv2.INTER_LANCZOS4)
hsv = cv2.cvtColor(K, cv2.COLOR_BGR2HSV); gK = cv2.cvtColor(K, 6)
def hull_mask(box, img_hsv, gray):
    x0,y0,x1,y1 = box; m = np.zeros(gray.shape, np.uint8)
    sub = ((img_hsv[y0:y1,x0:x1,1] > 40) | (gray[y0:y1,x0:x1] < 185)).astype(np.uint8)
    sub = cv2.morphologyEx(sub, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(sub)
    pts = []
    for k in range(1, n):
        if st[k, 4] > 300:
            ys, xs = np.nonzero(lab == k); pts.append(np.stack([xs + x0, ys + y0], 1))
    pts = np.concatenate(pts); h = cv2.convexHull(pts.astype(np.int32))
    cv2.fillConvexPoly(m, h, 1); return m, pts
mL, pL = hull_mask((150, 905, 600, 1078), hsv, gK)
mR, pR = hull_mask((1400, 872, 1840, 1062), hsv, gK)
mS, pS = hull_mask((1560, 400, 1640, 580), hsv, gK)
print('L', pL.min(0), pL.max(0), 'R', pR.min(0), pR.max(0), 'S', pS.min(0), pS.max(0))
# --- smooth the homography track: track 4 corner points, smooth, extrapolate after reliable range
C = np.float32([[300,300],[1620,300],[1620,900],[300,900]])
good = 47
P = np.array([cv2.perspectiveTransform(C[None], Hs[i])[0] for i in range(N)])
# frame-to-frame flow for later frames (room features unreliable once the floor dominates)
o = cv2.SIFT_create(4000)
for i in range(good, N):
    a, b = F[i-1], F[i]
    ka, da = o.detectAndCompute(cv2.cvtColor(a,6), None); kb, db = o.detectAndCompute(cv2.cvtColor(b,6), None)
    m = cv2.BFMatcher().knnMatch(da, db, k=2); g = [x for x, y in m if x.distance < 0.75 * y.distance]
    A = np.float32([ka[x.queryIdx].pt for x in g]); B = np.float32([kb[x.trainIdx].pt for x in g])
    Hf, _ = cv2.findHomography(A, B, cv2.RANSAC, 3)
    P[i] = cv2.perspectiveTransform(P[i-1][None], Hf)[0]
def gaussian_filter1d(x, sig, axis=0, mode='nearest'):
    r = int(3*sig)+1; k = np.exp(-0.5*(np.arange(-r,r+1)/sig)**2); k/=k.sum()
    xp = np.concatenate([np.repeat(x[:1], r, 0), x, np.repeat(x[-1:], r, 0)], 0)
    return np.stack([np.tensordot(k, xp[i:i+2*r+1], axes=(0,0)) for i in range(len(x))])
Ps = gaussian_filter1d(P, 1.5, axis=0, mode='nearest')
Hsm = [cv2.getPerspectiveTransform(C, Ps[i].astype(np.float32)) for i in range(N)]
# --- target: the clip's own left pile at the handoff frame
TH = 50   # 2.083 s
def red_bbox(img, box):
    x0,y0,x1,y1 = box; h = cv2.cvtColor(img[y0:y1,x0:x1], cv2.COLOR_BGR2HSV)
    r = (h[...,1] > 80) & ((h[...,0] < 12) | (h[...,0] > 168)) & (h[...,2] > 60)
    ys, xs = np.nonzero(r); return np.array([xs.min()+x0, ys.min()+y0, xs.max()+x0, ys.max()+y0], float)
rk = red_bbox(K, (300, 900, 600, 1078)); rr = red_bbox(F[TH], (0, 500, 1300, 1080))
print('red K', rk, 'red clip', rr)
# K-sweater predicted into frame TH via room homography
pk = cv2.perspectiveTransform(rk.reshape(2,1,2).astype(np.float32), Hsm[TH]).reshape(2,2)
s = (rr[2]-rr[0]) / (pk[1,0]-pk[0,0]); cK = pk.mean(0); cR = np.array([(rr[0]+rr[2])/2, (rr[1]+rr[3])/2])
print('scale', s, 'pred', cK, 'real', cR)
def S_at(w):   # similarity in frame space: scale about predicted centre then move to real centre
    sc = 1 + (s - 1) * w; tr = (cR - cK) * w
    return np.array([[sc, 0, cK[0]*(1-sc) + tr[0]], [0, sc, cK[1]*(1-sc) + tr[1]], [0, 0, 1]])
def ss(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)
# expansion about the focus of expansion (bed centre) for the right pile, same strength as the left
FOE = cv2.perspectiveTransform(np.float32([[[960, 640]]]), Hsm[TH])[0, 0]
def E_at(w, Hc):
    f = cv2.perspectiveTransform(np.float32([[[960, 640]]]), Hc)[0, 0]; sc = 1 + (s - 1) * w * 1.15
    return np.array([[sc, 0, f[0]*(1-sc)], [0, sc, f[1]*(1-sc)], [0, 0, 1]])
fe = lambda m, r: cv2.GaussianBlur(m.astype(np.float32), (0, 0), r)
aL, aR, aS = fe(mL, 3), fe(mR, 3), fe(mS, 2)
Kf = K.astype(np.float32)
# grade K's clothes to the clip's tone (clip is slightly lighter / cooler)
mean_k = Kf[gK > 200].mean(0); mean_c = F[0].astype(np.float32)[cv2.cvtColor(F[0],6) > 200].mean(0)
gain = mean_c / mean_k; print('gain', gain)
BL = np.float32([[150,905],[560,905],[560,1062],[150,1062]])
endL = cv2.perspectiveTransform(cv2.perspectiveTransform(BL[None], Hsm[TH]), S_at(1.0))[0]
def HL(i, w):
    a = cv2.perspectiveTransform(BL[None], Hsm[i])[0]
    return cv2.getPerspectiveTransform(BL, ((1-w)*a + w*endL).astype(np.float32))
out = []
for i in range(N):
    t = i / 24; f = F[i].astype(np.float32); Hc = Hsm[i]
    w = ss((t - 0.15) / (TH/24 - 0.15))       # glide from the trigger position to the real pile
    # hide the clip's own pile before the handoff (it only peeks in from the bottom edge)
    if 34 <= i < TH + 9:
        reg = ((cv2.cvtColor(F[i], cv2.COLOR_BGR2HSV)[...,1] > 40) | (cv2.cvtColor(F[i],6) < 185)).astype(np.uint8)
        reg[:int(1080*0.72)] = 0; reg[:, 1300:] = 0
        reg = cv2.dilate(reg, np.ones((25,25),np.uint8))
        if reg.any():
            clean = cv2.inpaint(F[i], reg, 9, cv2.INPAINT_TELEA).astype(np.float32)
            hide = 1 - ss((i - TH + 3) / 11)
            mk = fe(reg, 6)[..., None] * hide; f = f * (1 - mk) + clean * mk
    layers = [(aL, HL(i, w), 1 - ss((i - TH + 3) / 11)),
              (aR, E_at(w, Hc) @ Hc, 1.0),
              (aS, Hc, 1.0)]
    for a, Hm, op in layers:
        if op <= 0: continue
        Kw = cv2.warpPerspective(Kf * gain, Hm, (1920, 1080), flags=cv2.INTER_LANCZOS4)
        aw = cv2.warpPerspective(a, Hm, (1920, 1080), flags=cv2.INTER_LINEAR)[..., None] * op
        f = f * (1 - aw) + Kw * aw
    out.append(np.clip(f, 0, 255).astype(np.uint8))
np.save('g1c_head_comp.npy', np.array(out))
sheet = [cv2.resize(out[i], (384, 216)) for i in range(0, N, 4)]
while len(sheet) % 4: sheet.append(np.zeros_like(sheet[0]))
cv2.imwrite('comp_sheet.jpg', np.vstack([np.hstack(sheet[r:r+4]) for r in range(0, len(sheet), 4)]))

dec = subprocess.Popen(['ffmpeg','-v','error','-i','g1c_fix.mp4','-sws_flags','lanczos+accurate_rnd+full_chroma_int+full_chroma_inp','-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1920x1080','-r','24','-i','-','-sws_flags','lanczos+accurate_rnd+full_chroma_int+full_chroma_inp','-c:v','libx264','-crf','12','-pix_fmt','yuv420p','g1c_cl.mp4'],stdin=subprocess.PIPE)
i=0
while True:
    b=dec.stdout.read(1920*1080*3)
    if len(b)<1920*1080*3: break
    enc.stdin.write(out[i].tobytes() if i<len(out) else b); i+=1
enc.stdin.close(); enc.wait(); print('wrote g1c_cl.mp4', i)
