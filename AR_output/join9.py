"""Concatenate segments; at joins where two different AI renders meet while the camera is still,
use a short dissolve (XF s). Writes raw3.mp4 and timeline9x.json with corrected start times."""
import json, subprocess
XF = 0.25
DISSOLVE_BEFORE = {'SEG2A', 'SEG3A', 'SEG3B', 'R1_walk_turn', 'R2_turn', 'R3_turn_to_desk', 'R4_turn_window_step_back', 'ending_blinks_black'}
TL = json.load(open('timeline9.json')); segs = TL['segs']
def dur(p): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
# group consecutive segments; a new group starts at each dissolve label
groups = [[]]
for p, d, l in segs:
    if l in DISSOLVE_BEFORE and groups[-1]: groups.append([])
    groups[-1].append((p, d, l))
files = []
for gi, g in enumerate(groups):
    lst = f'g9grp{gi}.txt'; open(lst, 'w').write(''.join(f"file '{p}'\n" for p, d, l in g))
    out = f'g9grp{gi}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-sws_flags', 'lanczos+accurate_rnd+full_chroma_int+full_chroma_inp', '-c:v', 'libx264', '-crf', '15', '-pix_fmt', 'yuv420p', '-r', '24', out], check=True)
    files.append(out)
cur = files[0]
for k, nxt in enumerate(files[1:]):
    off = dur(cur) - XF; out = f'g9xf{k}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', cur, '-i', nxt, '-filter_complex',
                    f'[0:v][1:v]xfade=transition=fade:duration={XF}:offset={off:.4f},format=yuv420p', '-sws_flags', 'lanczos+accurate_rnd+full_chroma_int+full_chroma_inp', '-c:v', 'libx264', '-crf', '15', '-r', '24', out], check=True)
    cur = out
subprocess.run(['cp', cur, 'raw9.mp4'], check=True)
# corrected marks
marks = {}; t = 0.0
for p, d, l in segs:
    if l in DISSOLVE_BEFORE and t > 0: t -= XF
    marks[l] = [round(t, 3), round(t + d, 3)]; t += d
json.dump({'segs': segs, 'marks': marks}, open('timeline9x.json', 'w'), ensure_ascii=False, indent=1)
print('total', round(t, 3), 'raw3', round(dur('raw9.mp4'), 3))
