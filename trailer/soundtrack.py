#!/usr/bin/env python3
"""Compose the trailer's soundtrack: a music bed and the sound effects, both written in code.

Nothing is sampled, so the repo owns all of it. The timings follow the scenes in record.js and the
animations on the Drawdy board: each effect sits on the moment its element lands.

    python3 trailer/soundtrack.py /tmp/soundtrack.wav
    ffmpeg -y -i /tmp/soundtrack.wav -c:a aac -b:a 192k trailer/soundtrack.m4a

Needs numpy and scipy. record.js lays trailer/soundtrack.m4a under the video when the file exists.
"""

import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 44100
LENGTH = 60.0
N = int(SR * LENGTH)
T = np.arange(N) / SR
RNG = np.random.default_rng(11)

# ---------- scene starts, in seconds, matching SCENES in record.js ----------
QUESTION, TITLE, REPLY, RULES, TOOL, SKILLS, CODE, INSTALL, END = 0.0, 11.0, 17.0, 28.0, 38.0, 45.0, 50.0, 53.5, 60.0
SLIDE = 0.6


def note(name):
    names = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
    key, octave = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((names[key] + (octave - 4) * 12 - 9) / 12)


def env(t, start, end, attack, release):
    return np.minimum(np.clip((t - start) / attack, 0, 1), np.clip((end - t) / release, 0, 1))


def smooth(x):
    return x * x * (3 - 2 * x)


def lowpass(x, hz, order=2):
    return sosfilt(butter(order, hz, btype="low", fs=SR, output="sos"), x)


def bandpass(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)


def highpass(x, hz, order=2):
    return sosfilt(butter(order, hz, btype="high", fs=SR, output="sos"), x)


# =====================================================================
# the music bed: drone, pad, bass and a plucked line, as before, re-timed
# =====================================================================
BED = np.zeros(N)


def pad_voice(freq, detune_cents=(0.0, -7.0, 7.0), level=1.0):
    out = np.zeros(N)
    for c in detune_cents:
        phase = 2 * np.pi * freq * 2 ** (c / 1200) * T
        out += 2 / np.pi * np.arcsin(np.sin(phase)) + 0.35 * np.sin(2 * phase)
    return out * level / len(detune_cents)


def bed_pluck(freq, at, length=2.6, level=1.0):
    i0, i1 = int(at * SR), min(N, int((at + length) * SR))
    if i0 >= N:
        return
    tt = np.arange(i1 - i0) / SR
    tone = np.sin(2 * np.pi * freq * tt) + 0.25 * np.sin(2 * np.pi * freq * 2 * tt)
    BED[i0:i1] += tone * np.exp(-tt * 2.2) * np.minimum(1, tt / 0.008) * level


PROGRESSION = [
    ("A2", ["A3", "C4", "E4"], ["A4", "C5", "E5", "G5"]),
    ("F2", ["F3", "A3", "C4"], ["F4", "A4", "C5", "E5"]),
    ("C3", ["C4", "E4", "G4"], ["G4", "C5", "E5", "G5"]),
    ("G2", ["G3", "B3", "D4"], ["G4", "B4", "D5", "F#5"]),
]
CHORD = 8.0

drone = pad_voice(note("A2"), level=0.5) + pad_voice(note("E3"), level=0.25)
BED += lowpass(drone, 420) * env(T, 0.0, END, 2.5, 2.0) * (0.55 + 0.45 * smooth(np.clip((T - 6.0) / (TITLE - 6.0), 0, 1))) * 0.22

t_chord, i = TITLE, 0
while t_chord < END:
    root, tones, _ = PROGRESSION[i % 4]
    gate = env(T, t_chord, min(END, t_chord + CHORD) + 1.2, 2.4, 2.4)
    pad = sum(pad_voice(note(n)) for n in tones) / 3
    bass = np.sin(2 * np.pi * note(root) * T) + 0.4 * np.sin(4 * np.pi * note(root) * T)
    BED += lowpass(pad, 1400) * gate * 0.16 + lowpass(bass, 200) * gate * 0.12
    t_chord += CHORD
    i += 1

t = TITLE + 1.0
while t < CODE - 1.0:
    arp = PROGRESSION[int((t - TITLE) // CHORD) % 4][2]
    step = 1.0 if t < REPLY else (0.5 if SKILLS <= t < CODE else 0.75)
    if RNG.random() < 0.85:
        bed_pluck(note(arp[int((t - TITLE) / step) % len(arp)]), t, level=0.26 if t < RULES else 0.3)
    t += step

BED *= 1.0 - 0.75 * env(T, CODE, INSTALL, 0.6, 1.0)  # the quiet scene: the pad alone
final = pad_voice(note("A3")) + pad_voice(note("C#4"), level=0.8) + pad_voice(note("E4"), level=0.8)
BED += lowpass(final, 1200) * env(T, INSTALL + 2.0, END, 2.5, 0.5) * 0.12
BED *= env(T, 0.0, END - 0.4, 0.01, 2.5)


def comb(x, delay_s, feedback):
    d = int(delay_s * SR)
    y = np.zeros_like(x)
    for k in range(0, len(x), d):
        chunk = x[k:k + d]
        prev = y[k - d:k] if k >= d else np.zeros(len(chunk))
        y[k:k + len(chunk)] = chunk + feedback * prev[:len(chunk)]
    return y


def reverb(x, mix=0.26):
    wet = sum(comb(x, s, g) for s, g in [(0.0297, 0.72), (0.0371, 0.70), (0.0411, 0.68), (0.0437, 0.66)]) / 4
    return x * (1 - mix * 0.7) + lowpass(wet, 3200) * mix


BED = reverb(BED)
BED = BED / (np.max(np.abs(BED)) + 1e-9) * 0.42

# =====================================================================
# the sound effects, one function per sound, placed on the board's animations
# =====================================================================
FX_L, FX_R = np.zeros(N), np.zeros(N)


def place(sig, at, level=1.0, pan=0.0):
    """Add a mono effect at a time, panned -1 (left) to 1 (right)."""
    i0 = int(at * SR)
    if i0 >= N:
        return
    sig = sig[: N - i0] * level
    FX_L[i0:i0 + len(sig)] += sig * np.cos((pan + 1) * np.pi / 4)
    FX_R[i0:i0 + len(sig)] += sig * np.sin((pan + 1) * np.pi / 4)


def layer(*sigs):
    """Mix effects of different lengths, each paired with its gain: layer((sig, gain), ...)."""
    out = np.zeros(max(len(x) for x, _ in sigs))
    for x, g in sigs:
        out[: len(x)] += x * g
    return out


def tt(seconds):
    return np.arange(int(seconds * SR)) / SR


def noise(seconds):
    return RNG.standard_normal(int(seconds * SR))


def pop(pitch=520.0):
    """A bubble pop: a sine that falls an octave fast, with a click in front."""
    t = tt(0.16)
    f = pitch * (1 + np.exp(-t * 60))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 28)
    click = highpass(noise(0.16), 2500) * np.exp(-t * 400) * 0.3
    return tone + click


def blip(pitch):
    """A short soft tap for each paragraph of the reply."""
    t = tt(0.12)
    return (np.sin(2 * np.pi * pitch * t) + 0.3 * np.sin(4 * np.pi * pitch * t)) * np.exp(-t * 45) * np.minimum(1, t / 0.003)


def wood(pitch=900.0):
    """A wood-block tick for each row of the reply that drops into place."""
    t = tt(0.09)
    body = np.sin(2 * np.pi * pitch * t) * np.exp(-t * 70) + 0.5 * np.sin(2 * np.pi * pitch * 2.7 * t) * np.exp(-t * 120)
    return body + bandpass(noise(0.09), 1500, 4000) * np.exp(-t * 300) * 0.4


def slap():
    """A sticky note slapped onto a board: a papery burst over a soft thump."""
    t = tt(0.25)
    paper = bandpass(noise(0.25), 400, 3500) * np.exp(-t * 38)
    thump = np.sin(2 * np.pi * (95 + 60 * np.exp(-t * 40)) * t) * np.exp(-t * 22)
    return paper * 0.8 + thump * 0.9


def chime(freqs, decay=1.4):
    """A bell-like chime from a few partials."""
    t = tt(decay * 2)
    out = np.zeros(len(t))
    for k, (f, a) in enumerate(freqs):
        out += a * np.sin(2 * np.pi * f * t) * np.exp(-t * (1.6 + k * 0.9) / decay)
    return out * np.minimum(1, t / 0.004)


def kaching():
    """A cash register: the drawer's clunk, then the bell."""
    t = tt(0.12)
    clunk = (np.sin(2 * np.pi * 140 * t) * np.exp(-t * 35) + bandpass(noise(0.12), 800, 5000) * np.exp(-t * 90) * 0.7)
    bell = chime([(2093, 1.0), (2637, 0.6), (3136, 0.45), (5274, 0.25), (6272, 0.15)], decay=1.1)
    coins = np.zeros(len(bell))
    for k in range(6):  # a little rattle of coins
        at = int((0.03 + 0.045 * k + RNG.random() * 0.02) * SR)
        c = chime([(RNG.uniform(3800, 6500), 0.35)], decay=0.08)
        coins[at:at + len(c)] += c[: len(coins) - at] * (0.8 - 0.1 * k)
    out = np.zeros(int(0.09 * SR) + len(bell))
    out[: len(clunk)] += clunk
    out[int(0.09 * SR):] += bell + coins
    return out


def whoosh(seconds=0.6, lo=300, hi=2600):
    """Air moving past: noise through a band that sweeps up and back down."""
    n = noise(seconds)
    t = tt(seconds)
    shape = np.sin(np.pi * t / seconds) ** 1.5
    out = np.zeros(len(n))
    steps = 24
    for k in range(steps):  # a cheap swept filter: blend fixed bands by position
        a, b = int(k * len(n) / steps), int((k + 1) * len(n) / steps)
        centre = lo + (hi - lo) * np.sin(np.pi * (k + 0.5) / steps)
        out[a:b] = bandpass(n, centre * 0.7, min(centre * 1.4, SR / 2 - 100))[a:b]
    return out * shape


def marker(seconds=0.7):
    """A felt marker drawn across a board: scratchy, bright noise with a little pressure wobble."""
    t = tt(seconds)
    grain = highpass(noise(seconds), 2200) * (0.6 + 0.4 * np.sin(2 * np.pi * 31 * t) ** 2)
    return grain * np.minimum(1, t / 0.04) * np.minimum(1, (seconds - t) / 0.08)


def riser(seconds, shape):
    """A soft rising tone that follows the token meter as it fills."""
    t = tt(seconds)
    p = shape(t / seconds)
    f = 180 * 2 ** (2.3 * p)
    phase = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(phase) + 0.3 * np.sin(2 * phase) + 0.15 * np.sin(3 * phase)
    return lowpass(tone, 2400) * (0.25 + 0.75 * p) * np.minimum(1, t / 0.3) * np.minimum(1, (seconds - t) / 0.05)


def whoop(f0, f1, seconds=0.9):
    """A bar growing: a rising glide."""
    t = tt(seconds)
    p = 1 - (1 - t / seconds) ** 3
    f = f0 * (f1 / f0) ** p
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / seconds) ** 0.7


def keyclick():
    t = tt(0.05)
    return bandpass(noise(0.05), 1800, 6000) * np.exp(-t * 180) + np.sin(2 * np.pi * 320 * t) * np.exp(-t * 120) * 0.4


def sparkle():
    out = np.zeros(int(0.9 * SR))
    for k in range(9):
        at = int(k * 0.07 * SR)
        c = chime([(RNG.uniform(3000, 7000), 0.5)], decay=0.12)
        out[at:at + len(c)] += c[: len(out) - at] * (1 - k / 10)
    return out


def tick_tock():
    t = tt(0.03)
    return bandpass(noise(0.03), 2500, 7000) * np.exp(-t * 300)


# transitions: a whoosh as each scene slides in
for s in (TITLE, REPLY, RULES, TOOL, SKILLS, CODE, INSTALL):
    place(whoosh(0.7), s - 0.05, 0.22, pan=0.4)

# 1. the question: the bubble pops in, every paragraph taps, the meter rises, and the till rings at 644
place(pop(560), QUESTION + 0.42, 0.55, pan=-0.1)
for k, at in enumerate([1.6, 3.0, 4.2, 5.2, 6.1, 6.9, 7.6, 8.2]):
    place(blip(note(["E5", "G5", "A5", "C6", "D6", "E6", "G6", "A6"][k])), QUESTION + at + 0.05, 0.22, pan=-0.35)
place(riser(8.5, lambda p: p ** 1.8), QUESTION + 1.5, 0.12, pan=0.45)
place(kaching(), QUESTION + 10.0, 0.42, pan=0.45)

# 2. the title: a tap as each letter lands, left to right, a marker for the underline, a pop for the sticker
for k in range(8):
    place(layer((blip(note(["A4", "C5", "D5", "E5", "G5", "A5", "C6", "D6"][k]) / 2), 1.0), (wood(700 + 40 * k), 0.4)), TITLE + 0.2 + 0.11 * k + 0.32, 0.3, pan=-0.6 + 1.2 * k / 7)
place(marker(0.7), TITLE + 1.25, 0.12, pan=0.0)
place(pop(380), TITLE + 3.3 + 0.25, 0.6, pan=0.7)

# 3. one reply, in order: a tick per row, a chime when the answer lands and again when it pulses
for k in range(11):
    at = REPLY + 0.4 + 0.45 * k + 0.22
    if k == 4:
        place(chime([(note("E6"), 1.0), (note("B6"), 0.4)], decay=0.9), at, 0.3, pan=-0.1)
    else:
        place(wood(820 + 25 * k), at, 0.32, pan=-0.2)
place(chime([(note("A5"), 1.0), (note("E6"), 0.6), (note("A6"), 0.3)], decay=1.2), REPLY + 6.25, 0.32, pan=-0.1)
place(whoosh(0.5, 600, 3000), REPLY + 7.25, 0.12, pan=0.6)

# 4. the rules: eight sticky notes slapped on, left to right
for k in range(8):
    place(slap(), RULES + 0.45 + 0.62 * k + 0.33, 0.55, pan=-0.6 + 1.2 * (k % 4) / 3)

# 5. one tool run: the row clicks in, the spinner ticks, the check dings, the cards pop
place(keyclick(), TOOL + 1.35, 0.4)
for k in range(9):
    place(tick_tock(), TOOL + 1.65 + 0.1 * k, 0.18, pan=0.5)
place(chime([(note("E5"), 1.0)], decay=0.5), TOOL + 2.6, 0.3, pan=0.5)
place(chime([(note("A5"), 1.0), (note("E6"), 0.3)], decay=0.9), TOOL + 2.72, 0.32, pan=0.5)
for k, at in enumerate([3.0, 3.5, 4.0]):
    place(pop(300 + 60 * k), TOOL + at + 0.15, 0.32, pan=-0.5 + 0.5 * k)

# 6. three skills: soft pops for the cards, a rising glide per bar, a plink for each number
for k, at in enumerate([0.3, 0.5, 0.7]):
    place(pop(340 + 40 * k), SKILLS + at + 0.12, 0.25, pan=-0.5 + 0.5 * k)
for k, (value, at) in enumerate([(63, 1.2), (644, 1.35), (778, 1.5), (893, 1.65)]):
    place(whoop(160, 160 + value * 0.7), SKILLS + at, 0.1, pan=-0.6 + 0.4 * k)
    place(chime([(1200 + value * 1.4, 1.0)], decay=0.25), SKILLS + at + 0.9, 0.22, pan=-0.6 + 0.4 * k)

# 7. your code stays yours: quiet, a pen drawing the empty signature line
place(marker(0.7) * 0.8, CODE + 1.7, 0.1, pan=0.1)

# 8. install and sign-off: typing, the till again on "Act now.", a sparkle for the star
for k in range(10):
    place(keyclick(), INSTALL + 0.3 + 0.055 * k + RNG.random() * 0.02, 0.22, pan=-0.2 + 0.04 * k)
place(kaching(), INSTALL + 2.25, 0.4, pan=0.0)
place(sparkle(), INSTALL + 2.8, 0.2, pan=0.35)

# =====================================================================
# the mix: the bed under the effects, a little room on the effects, a soft limiter
# =====================================================================
FX_L, FX_R = reverb(FX_L, 0.18), reverb(FX_R, 0.18)
shift = int(0.011 * SR)
bed_l, bed_r = BED, np.concatenate([np.zeros(shift), BED[:-shift]]) * 0.97 + BED * 0.03
mix = np.stack([bed_l + FX_L, bed_r + FX_R], axis=1)
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89

out = sys.argv[1] if len(sys.argv) > 1 else "soundtrack.wav"
wavfile.write(out, SR, (mix * 32767).astype(np.int16))
print(f"wrote {out}: {LENGTH:.0f}s, {SR} Hz, stereo, peak {np.max(np.abs(mix)):.2f}")
