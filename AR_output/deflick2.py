import cv2,numpy as np,subprocess,json,sys
v=sys.argv[1]; W,H=1920,1080
TL=sys.argv[2]; SRC=sys.argv[3]; OUTF=sys.argv[4]
m=json.load(open(TL))['marks']
blinks=[(0,1.85),(m['ending_blinks_black'][0],999)]+[(a-0.05,b+0.05) for k,(a,b) in m.items() if k.startswith('blink')]
SW=['-sws_flags','lanczos+accurate_rnd+full_chroma_int+full_chroma_inp']
raw=subprocess.run(['ffmpeg','-v','error','-i',SRC]+SW+['-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout
fr=list(np.frombuffer(raw,np.uint8).reshape(-1,H,W,3))
mean=np.array([cv2.resize(f,(160,90)).mean() for f in fr]); n=len(mean)
x=np.arange(-18,19); k=np.exp(-(x/6.0)**2); k/=k.sum()
inb=np.array([any(a-0.3<=i/24<=b+0.3 for a,b in blinks) for i in range(n)])
mm=mean.copy(); idx=np.arange(n); mm[inb]=np.interp(idx[inb],idx[~inb],mean[~inb])
pad=np.pad(mm,18,mode='edge'); sm=np.convolve(pad,k,'same')[18:-18]
corr=np.clip(sm-mm,-20,20)
for i in range(n):
    t=i/24
    if inb[i]: corr[i]=0
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r','24','-i','-','-an','-sws_flags','lanczos+accurate_rnd+full_chroma_int+full_chroma_inp','-c:v','libx264','-crf','15','-pix_fmt','yuv420p',OUTF],stdin=subprocess.PIPE)
for i,f in enumerate(fr):
    c=corr[i]
    if abs(c)>0.3:
        tgt=mean[i]+c; s=(255-tgt)/max(255-mean[i],1)
        f=np.clip(255-(255-f.astype(np.float32))*s,0,255).astype(np.uint8)
    enc.stdin.write(f.tobytes())
enc.stdin.close(); enc.wait()
G=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',OUTF,'-vf','scale=160:90','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout,np.uint8).reshape(-1,90,160).astype(np.float32)
db=np.abs(np.diff(G.mean((1,2))))
print(v,'max frame-to-frame brightness change outside blinks:',round(float(max(db[i] for i in range(len(db)) if not any(a<=i/24<=b for a,b in blinks))),1))
