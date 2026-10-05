import cv2, numpy as np, subprocess
SW=['-sws_flags','lanczos+accurate_rnd+full_chroma_int+full_chroma_inp']
raw=subprocess.run(['ffmpeg','-v','error','-i','g2a2.mp4']+SW+['-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout
FR=np.frombuffer(raw,np.uint8).reshape(-1,1080,1920,3); N=len(FR); print(N)
REF=int(3.95*24)
ref=FR[REF]
# region: the gap + shirt (saturated) dilated
hsv=cv2.cvtColor(ref,cv2.COLOR_BGR2HSV); m=((hsv[...,1]>60)&(hsv[...,2]>50)).astype(np.uint8)
ys,xs=np.nonzero(m); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max(); print('shirt bbox',x0,y0,x1,y1)
mask=np.zeros((1080,1920),np.float32); cv2.rectangle(mask,(x0-60,max(y0-40,0)),(x1+40,min(y1+60,1079)),1,-1)
mask=cv2.GaussianBlur(mask,(0,0),18)
o=cv2.SIFT_create(4000); dis=lambda im: o.detectAndCompute(cv2.cvtColor(cv2.resize(im,(960,540)),6),None)
# chain homographies backwards: H[i] maps ref coords -> frame i
Hs={REF:np.eye(3)}; kd={REF:dis(ref)}
for i in range(REF-1, int(1.0*24)-1, -1):
    kd[i]=dis(FR[i]); (ka,da),(kb,db)=kd[i+1],kd[i]
    mm=cv2.BFMatcher().knnMatch(da,db,k=2); g=[a for a,b in mm if a.distance<0.7*b.distance]
    P=np.float32([ka[x.queryIdx].pt for x in g])*2;Q=np.float32([kb[x.trainIdx].pt for x in g])*2
    Hm,inl=cv2.findHomography(P,Q,cv2.RANSAC,3)
    Hs[i]=Hm@Hs[i+1]; print(i, round(i/24,2), len(g), int(inl.sum()))
np.save('wardrobe_H.npy',np.array([Hs.get(i,np.eye(3)) for i in range(N)]))
