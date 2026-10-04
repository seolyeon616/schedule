import cv2, numpy as np, subprocess, json
raw = subprocess.run(['ffmpeg','-v','error','-t','2.6','-i','g1c_fix.mp4','-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout
F = np.frombuffer(raw,np.uint8).reshape(-1,1080,1920,3); print('frames',len(F))
np.save('g1c_head.npy',F)
K = cv2.resize(cv2.imread('../images/23.jpg'),(1920,1080),interpolation=cv2.INTER_LANCZOS4)
o = cv2.SIFT_create(6000); ka,da=o.detectAndCompute(cv2.cvtColor(K,6),None)
# room-only features: ignore the floor half where clothes differ
Hs=[]; prev=None
for i,f in enumerate(F):
    kb,db=o.detectAndCompute(cv2.cvtColor(f,6),None)
    m = cv2.BFMatcher().knnMatch(da,db,k=2); g=[a for a,b in m if a.distance<0.75*b.distance]
    P=np.float32([ka[x.queryIdx].pt for x in g]);Q=np.float32([kb[x.trainIdx].pt for x in g])
    keep = P[:,1] < 760
    Hm,inl = cv2.findHomography(P[keep],Q[keep],cv2.RANSAC,4)
    Hs.append(Hm/Hm[2,2]); print(i, round(i/24,3), int(keep.sum()), int(inl.sum()))
np.save('Hs_open.npy',np.array(Hs))
