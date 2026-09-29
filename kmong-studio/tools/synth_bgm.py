"""MANYEON FILM01 BGM 합성기 (A: Glacial Hymn / C: Crystal Pulse).

외부 음원·샘플 없이 numpy로 직접 합성하므로 라이선스 걱정이 없는 오리지널 음원.
영상 타임라인(초)에 맞춰 절정·정적·마무리를 배치한다.

usage: python3 synth_bgm.py A out.wav [total_seconds]
"""
import sys
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt

SR = 48000
KIND = sys.argv[1]
OUT = sys.argv[2]
TOTAL = float(sys.argv[3]) if len(sys.argv) > 3 else 43.8

# 영상 타임라인 (FILM01 v2)
T_BREAK = 15.1      # 폭포 → 숲: 0.3초 완전 무음
T_CLIMAX = 19.0     # 여인 등장
T_SERUM = 23.4      # 세럼 (내레이션 자리)
T_HERO = 29.4       # 제품 + 대형 로고
T_RIPPLE = 35.6     # 파문
T_IMPACT = 37.8     # 물방울이 수면에 닿는 순간
rng = np.random.default_rng(7)
N = int(TOTAL * SR)
t_all = np.arange(N) / SR


def hz(note):
    names = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4, "F#": -3, "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}
    n, o = note[:-1], int(note[-1])
    return 440.0 * 2 ** ((names[n] + (o - 4) * 12) / 12)


def buf():
    return np.zeros((N, 2))


def place(dst, sig, start, gain=1.0, pan=0.0):
    i = int(start * SR)
    if i >= N:
        return
    sig = sig[: N - i]
    l, r = np.sqrt(0.5 * (1 - pan)), np.sqrt(0.5 * (1 + pan))
    if sig.ndim == 2:
        dst[i:i + len(sig)] += sig * gain
        return
    dst[i:i + len(sig), 0] += sig * gain * l
    dst[i:i + len(sig), 1] += sig * gain * r


def env_adsr(n, a, d, s, r, sustain_len):
    total = int((a + d + sustain_len + r) * SR)
    e = np.zeros(total)
    ia, idd, isl = int(a * SR), int(d * SR), int(sustain_len * SR)
    e[:ia] = np.linspace(0, 1, ia, endpoint=False) if ia else []
    e[ia:ia + idd] = np.linspace(1, s, idd, endpoint=False)
    e[ia + idd:ia + idd + isl] = s
    e[ia + idd + isl:] = np.linspace(s, 0, total - (ia + idd + isl))
    return e


def lowpass(x, fc, order=2):
    sos = butter(order, fc, btype="low", fs=SR, output="sos")
    return sosfilt(sos, x, axis=0)


def highpass(x, fc, order=2):
    sos = butter(order, fc, btype="high", fs=SR, output="sos")
    return sosfilt(sos, x, axis=0)


def piano(f, dur=4.0, vel=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for k, a in enumerate([1, 0.55, 0.3, 0.16, 0.09, 0.05], start=1):
        fk = f * k * (1 + 0.0004 * k * k)
        s += a * np.sin(2 * np.pi * fk * t) * np.exp(-t * (1.1 + 0.9 * k))
    att = np.minimum(1, t / 0.012)
    s = s * att * vel
    return lowpass(s, 2600)


def glass(f, dur=6.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t * 0.7)
         + 0.35 * np.sin(2 * np.pi * f * 2.756 * t) * np.exp(-t * 1.6)
         + 0.15 * np.sin(2 * np.pi * f * 5.404 * t) * np.exp(-t * 3.0))
    return s * np.minimum(1, t / 0.004)


def pluck(f, dur=1.6, bright=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * t) + 0.3 * bright * np.sin(2 * np.pi * 2 * f * t) + 0.12 * bright * np.sin(2 * np.pi * 3.01 * f * t))
    return s * np.exp(-t * 3.2) * np.minimum(1, t / 0.003)


def saw_pad(freqs, dur, attack, release, fc):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.zeros((n, 2))
    for f in freqs:
        for ch, det in ((0, -0.0035), (1, 0.0035)):
            for d2 in (-0.002, 0.0, 0.002):
                ph = 2 * np.pi * f * (1 + det + d2) * t + rng.uniform(0, 6.28)
                s[:, ch] += 2 * ((ph / (2 * np.pi)) % 1) - 1
    s /= max(1, len(freqs) * 3)
    e = np.minimum(1, t / attack) * np.minimum(1, np.maximum(0, (dur - t) / release))
    s *= e[:, None]
    return lowpass(s, fc)


def sine_pad(freqs, dur, attack, release):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for f in freqs:
        s += np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28)) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    s /= len(freqs)
    return s * np.minimum(1, t / attack) * np.minimum(1, np.maximum(0, (dur - t) / release))


def thump(f0=55, dur=0.6):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f0 * (1 + 1.5 * np.exp(-t * 30))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7)


def reverb(x, seconds=3.5, wet=0.35, predelay=0.02):
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = np.zeros((n + int(predelay * SR), 2))
    for ch in range(2):
        noise = rng.standard_normal(n) * np.exp(-t * (6.9 / seconds))
        ir[int(predelay * SR):, ch] = lowpass(noise, 6000)
    ir /= np.sqrt((ir ** 2).sum(axis=0))
    out = np.stack([fftconvolve(x[:, ch], ir[:, ch])[: len(x)] for ch in range(2)], axis=1)
    return x * (1 - wet) + out * wet * 1.6


def delay(x, time, fb=0.35, mix=0.3):
    d = int(time * SR)
    y = x.copy()
    for k in range(1, 6):
        g = mix * fb ** (k - 1)
        sh = d * k
        if sh >= len(x):
            break
        if k % 2:
            y[sh:, 0] += x[:-sh, 1] * g
            y[sh:, 1] += x[:-sh, 0] * g
        else:
            y[sh:] += x[:-sh] * g
    return y


def gate_break(x):
    a, b = int(T_BREAK * SR), int((T_BREAK + 0.3) * SR)
    fade = int(0.08 * SR)
    x[a - fade:a] *= np.linspace(1, 0, fade)[:, None]
    x[a:b] = 0
    return x


def master(x, fade_out=2.5):
    x = highpass(x, 28)
    fo = int(fade_out * SR)
    x[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    x[: int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))[:, None]
    x = np.tanh(x * 1.1) / np.tanh(1.1)
    peak = np.max(np.abs(x))
    return x / peak * 0.89


def glacial_hymn():
    mix = buf()
    # 0–7: 거의 무음, 저음 스웰 + 유리 한 음
    sub = sine_pad([hz("D2"), hz("A2")], T_BREAK - 0.2, 5.0, 3.0)
    place(mix, sub, 0.0, 0.06)
    place(mix, glass(hz("D6"), 7), 0.35, 0.10, -0.2)
    place(mix, glass(hz("A5"), 7), 3.05, 0.08, 0.25)
    # 7–15: 드문 피아노 (고대의 시간)
    for tt, nn, v in [(7.3, "F#4", .8), (8.7, "A4", .7), (10.2, "D5", .75), (11.6, "E5", .65), (13.1, "C#5", .6), (14.2, "A4", .5)]:
        place(mix, piano(hz(nn), 4.0, v), tt, 0.22, rng.uniform(-.3, .3))
    place(mix, saw_pad([hz("D3"), hz("A3"), hz("E4"), hz("F#4")], T_BREAK - 9.0, 3.0, 1.5, 900), 9.0, 0.05)
    # 15.4–19: 피아노가 조용히 돌아옴
    for tt, nn, v in [(15.5, "B3", .6), (16.4, "D4", .55), (17.3, "F#4", .6), (18.3, "A4", .55)]:
        place(mix, piano(hz(nn), 4.0, v), tt, 0.20, rng.uniform(-.3, .3))
    # 19–29.4: 현악이 차오르는 절정 (Bm → G → D/F# → Asus)
    chords = [(T_CLIMAX, 3.2, ["B2", "F#3", "B3", "D4", "F#4"]),
              (22.0, 3.2, ["G2", "D3", "B3", "D4", "G4"]),
              (25.0, 2.8, ["F#2", "D3", "A3", "D4", "F#4"]),
              (27.6, 2.4, ["A2", "E3", "A3", "D4", "E4"])]
    for i, (st, du, notes) in enumerate(chords):
        g = [0.30, 0.38, 0.36, 0.32][i]
        place(mix, saw_pad([hz(n) for n in notes], du + 1.4, 1.2, 1.4, 1100 + 400 * i), st, g)
    for tt, nn in [(19.3, "D5"), (20.6, "C#5"), (21.4, "B4"), (22.4, "D5"), (23.2, "E5"), (26.2, "F#5"), (27.9, "E5")]:
        place(mix, piano(hz(nn), 3.5, .7), tt, 0.22, rng.uniform(-.2, .2))
    # 29.4–35.6: Dmaj9로 해소, 로고에 유리 한 음
    place(mix, saw_pad([hz(n) for n in ["D2", "A2", "F#3", "C#4", "E4"]], 6.6, 1.0, 3.0, 1300), T_HERO, 0.22)
    place(mix, glass(hz("F#6"), 6), T_HERO + 0.6, 0.09, 0.2)
    place(mix, sine_pad([hz("D2")], 6.4, 0.5, 3.0), T_HERO, 0.18)
    # 파문: 피아노 한 음으로 끝 (긴 잔향)
    for nn, v in [("D3", .8), ("D4", .6), ("A4", .45)]:
        place(mix, piano(hz(nn), 6.0, v), T_IMPACT, 0.30)
    place(mix, glass(hz("D6"), 6), T_IMPACT + 0.02, 0.07)
    mix = reverb(mix, 4.5, 0.45)
    return master(gate_break(mix))


def crystal_pulse():
    mix = buf()
    beat = 60 / 70
    air = highpass(rng.standard_normal(N), 5000) * 0.006
    mix[:, 0] += air
    mix[:, 1] += np.roll(air, 900)
    place(mix, pluck(hz("E6"), 3.0, .6), 0.25, 0.16, -0.3)
    place(mix, pluck(hz("B5"), 3.0, .6), 3.05, 0.14, 0.3)
    arp = ["E4", "G4", "B4", "D5", "F#5", "D5", "B4", "G4"]

    def arps(start, end, gain, bright, fc):
        seg = buf()
        k, tt = 0, start
        while tt < end:
            place(seg, pluck(hz(arp[k % len(arp)]), 1.2, bright), tt, gain, 0.5 * np.sin(k * 0.9))
            k += 1
            tt += beat / 2
        return lowpass(seg, fc)

    def pulse(start, end, gain):
        tt = start
        while tt < end:
            place(mix, thump(52), tt, gain)
            place(mix, thump(52), tt + 0.22, gain * 0.6)
            tt += beat * 2

    # 7–15: 심장 박동 같은 펄스 + 필터된 아르페지오가 쌓임
    pulse(7.1, T_BREAK - 0.3, 0.45)
    mix += arps(7.1, T_BREAK - 0.2, 0.09, .5, 1800)
    mix += arps(11.1, T_BREAK - 0.2, 0.06, .9, 4000)
    # 15.4–19: 필터된 아르페지오만
    mix += arps(15.45, T_CLIMAX, 0.07, .4, 1200)
    # 19–29.4: 따뜻한 패드가 열리고 펄스가 커짐 (Cmaj7 → G → D → Em9)
    chords = [(T_CLIMAX, ["C3", "G3", "B3", "E4"]), (22.0, ["G2", "D3", "B3", "F#4"]),
              (25.0, ["D3", "A3", "F#4", "A4"]), (27.6, ["E2", "B2", "G3", "D4", "F#4"])]
    for i, (st, notes) in enumerate(chords):
        du = (chords[i + 1][0] if i + 1 < len(chords) else T_HERO) - st
        place(mix, saw_pad([hz(n) for n in notes], du + 1.2, 0.8, 1.2, 700 + 500 * i), st, 0.36)
    pulse(T_CLIMAX, T_HERO, 0.55)
    mix += arps(T_CLIMAX, T_HERO, 0.08, 1.0, 6000)
    # 29.4–35.6: Em9 위에서 잔잔하게
    place(mix, saw_pad([hz(n) for n in ["E2", "B2", "G3", "D4", "F#4"]], T_RIPPLE - T_HERO + 1.5, 0.6, 2.0, 1600), T_HERO, 0.24)
    pulse(T_HERO, T_RIPPLE - 1.0, 0.35)
    mix += arps(T_HERO, T_RIPPLE - 0.5, 0.05, .7, 3000)
    # 파문: 펄스 멈추고 크리스털 한 음
    place(mix, pluck(hz("E6"), 6.0, .5), T_IMPACT, 0.22)
    place(mix, glass(hz("B6"), 6.0), T_IMPACT + 0.01, 0.07)
    place(mix, sine_pad([hz("E2")], 5.5, 0.05, 4.0), T_IMPACT, 0.16)
    mix = delay(mix, beat * 0.75, 0.4, 0.22)
    mix = reverb(mix, 3.2, 0.35)
    return master(gate_break(mix))


out = glacial_hymn() if KIND.upper() == "A" else crystal_pulse()
pcm = (out * 32767).astype(np.int16)
import wave
with wave.open(OUT, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote", OUT, round(len(out) / SR, 2), "s")
