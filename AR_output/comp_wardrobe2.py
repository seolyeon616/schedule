import cv2, numpy as np, subprocess
SW=['-sws_flags','lanczos+accurate_rnd+full_chroma_int+full_chroma_inp']
raw=subprocess.run(['ffmpeg','-v','error','-i','g2a2.mp4']+SW+['-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout
FR=np.frombuffer(raw,np.uint8).reshape(-1,1080,1920,3).copy(); N=len(FR)
REF=int(3.95*24); ref=FR[REF].astype(np.float32); Hs=np.load('wardrobe_H.npy')
hsv=cv2.cvtColor(FR[REF],cv2.COLOR_BGR2HSV)
m=((hsv[...,1]>90)&(hsv[...,2]>60)&((hsv[...,0]<20)|(hsv[...,0]>165))).astype(np.uint8)
n,lab,st,_=cv2.connectedComponentsWithStats(m); k=1+np.argmax(st[1:,4]); x,y,w,h=st[k,:4]; print('shirt',x,y,w,h)
mask=np.zeros((1080,1920),np.float32); cv2.rectangle(mask,(x-90,max(y-30,0)),(x+w+50,min(y+h+50,1079)),1,-1)
mask=cv2.GaussianBlur(mask,(0,0),20)
# smooth the homography track (corner points) to avoid jitter
C=np.float32([[x-90,y-30],[x+w+50,y-30],[x+w+50,y+h+50],[x-90,y+h+50]])
idx=list(range(24,REF+1)); P=np.array([cv2.perspectiveTransform(C[None],Hs[i])[0] for i in idx])
def gs(a,s):
    r=int(3*s)+1;kk=np.exp(-0.5*(np.arange(-r,r+1)/s)**2);kk/=kk.sum();ap=np.concatenate([np.repeat(a[:1],r,0),a,np.repeat(a[-1:],r,0)])
    return np.stack([np.tensordot(kk,ap[i:i+2*r+1],axes=(0,0)) for i in range(len(a))])
Ps=gs(P,2.0)
START=int(3.25*24)   # before this the real door is closed; composite fades OUT as we reach the real ajar door
for j,i in enumerate(idx):
    if i>=REF: break
    Hm=cv2.getPerspectiveTransform(C,Ps[j].astype(np.float32))
    pw=cv2.warpPerspective(ref,Hm,(1920,1080),flags=cv2.INTER_LANCZOS4)
    aw=cv2.warpPerspective(mask,Hm,(1920,1080))[...,None]
    fade=1.0
    FR[i]=np.clip(FR[i]*(1-aw*fade)+pw*aw*fade,0,255).astype(np.uint8)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1920x1080','-r','24','-i','-']+SW+['-c:v','libx264','-crf','12','-pix_fmt','yuv420p','g2a2_cl.mp4'],stdin=subprocess.PIPE)
for f in FR: enc.stdin.write(f.tobytes())
enc.stdin.close(); enc.wait()
