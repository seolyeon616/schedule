import subprocess,numpy as np,json,sys
f=sys.argv[1]; tlf=sys.argv[2]
tl=json.load(open(tlf))['marks']
w,h=320,180
G=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-vf',f'scale={w}:{h}','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout,np.uint8).reshape(-1,h,w).astype(np.float32)
n=len(G)
def shift(a,b):
    A=np.fft.fft2(a-a.mean());B=np.fft.fft2(b-b.mean());R=A*np.conj(B);R/=np.abs(R)+1e-6;r=np.abs(np.fft.ifft2(R))
    y,x=np.unravel_index(r.argmax(),r.shape);return (x if x<w//2 else x-w),(y if y<h//2 else y-h),r.max()
pan=np.zeros(n);diff=np.zeros(n);bri=G.mean((1,2))
for i in range(1,n):
    dx,dy,c=shift(G[i-1],G[i]); pan[i]=np.hypot(dx,dy)*1920/w; diff[i]=np.abs(G[i]-G[i-1]).mean()
seg=lambda t:[k for k,(a,b) in tl.items() if a<=t<b][-1]
blink=lambda t: any(k.startswith('blink') or k in('opening','ending_blinks_black') for k in [seg(t)]) and (seg(t)!='ending_blinks_black' or t>tl['ending_blinks_black'][0]+0.15)
rows=[]
for b in range(int(n/2.4)):
    i0,i1=int(b*2.4),int((b+1)*2.4)+1
    t=b/10; s=seg(t)
    p=pan[i0:i1].max(); d=diff[i0:i1].max(); db=np.abs(np.diff(bri[i0:i1])).max() if i1-i0>1 else 0
    flags=[]
    if not blink(t):
        if p>45: flags.append(f'FAST-PAN {p:.0f}px/f')
        if d>14: flags.append(f'JUMP {d:.1f}')
        if db>6: flags.append(f'FLASH {db:.1f}')
    rows.append((t,s,round(p),round(d,1),round(db,1),flags))
bad=[r for r in rows if r[5]]
print('windows',len(rows),'flagged',len(bad))
for r in bad: print(f'{r[0]:5.1f}s {r[1]:24s} pan {r[2]:4d} diff {r[3]:5.1f} dbri {r[4]:4.1f}  {", ".join(r[5])}')

