#!/usr/bin/env python3
"""Compose the trailer's music bed.

One minute of slow, warm, synthesized music, written in code so the repo owns it
outright. Nothing is sampled. The structure follows the trailer's scenes: a low drone
under the opening reply, the pad and a plucked line from the title on, a soft tick as
every rule card lands, a drop to the pad alone for "Your code stays yours", and a fade
at the end.

    python3 trailer/music.py trailer/music.wav

Needs numpy and scipy. Encode to AAC with ffmpeg; render.js muxes trailer/music.m4a
into the video when the file exists.
"""

import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 44100
LENGTH = 60.0
N = int(SR * LENGTH)
T = np.arange(N) / SR

# ---------- scene markers, in seconds, matching trailer.html ----------
TITLE = 11.0
BLOCKS = 17.0
RULES = 28.0
CARDS = [28.6 + i * 0.85 for i in range(8)]
MODES = 45.0
QUIET = 50.5
CLOSE = 54.0
END = 60.0


def note(name):
    """Frequency of a note name such as A3 or F#4."""
    names = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
    key, octave = name[:-1], int(name[-1])
    semis = names[key] + (octave - 4) * 12 - 9  # relative to A4
    return 440.0 * 2 ** (semis / 12)


def env(t, start, end, attack, release):
    """A smooth gate between start and end, with attack and release in seconds."""
    a = np.clip((t - start) / attack, 0, 1)
    r = np.clip((end - t) / release, 0, 1)
    return np.minimum(a, r)


def smooth(x):
    return x * x * (3 - 2 * x)


def lowpass(x, hz, order=2):
    sos = butter(order, hz, btype="low", fs=SR, output="sos")
    return sosfilt(sos, x)


def pad_voice(freq, detune_cents=(0.0, -7.0, 7.0), level=1.0):
    """Three slightly detuned triangle-ish oscillators, softened: a warm pad tone."""
    out = np.zeros(N)
    for c in detune_cents:
        f = freq * 2 ** (c / 1200)
        phase = 2 * np.pi * f * T
        tri = 2 / np.pi * np.arcsin(np.sin(phase))
        out += tri + 0.35 * np.sin(2 * phase)
    return out * level / len(detune_cents)


def pluck(freq, at, length=2.6, level=1.0):
    """A soft plucked note: a sine with a touch of second harmonic and an exponential decay."""
    i0 = int(at * SR)
    i1 = min(N, int((at + length) * SR))
    if i0 >= N:
        return
    tt = np.arange(i1 - i0) / SR
    tone = np.sin(2 * np.pi * freq * tt) + 0.25 * np.sin(2 * np.pi * freq * 2 * tt)
    shape = np.exp(-tt * 2.2) * np.minimum(1, tt / 0.008)
    MIX[i0:i1] += tone * shape * level


def tick(at, level=1.0):
    """A short click for the rule cards: a bright tap over a low knock, so it reads through the pad."""
    i0 = int(at * SR)
    i1 = min(N, i0 + int(0.12 * SR))
    tt = np.arange(i1 - i0) / SR
    noise = np.random.default_rng(int(at * 10)).standard_normal(i1 - i0)
    body = (0.8 * np.sin(2 * np.pi * 1400 * tt) * np.exp(-tt * 90)
            + 0.6 * np.sin(2 * np.pi * 220 * tt) * np.exp(-tt * 40)
            + 0.5 * noise * np.exp(-tt * 400))
    MIX[i0:i1] += body * level


# ---------- harmony: a slow progression, eight seconds a chord, from the title on ----------
PROGRESSION = [  # (root for the bass, chord tones for the pad, arpeggio notes)
    ("A2", ["A3", "C4", "E4"], ["A4", "C5", "E5", "G5"]),
    ("F2", ["F3", "A3", "C4"], ["F4", "A4", "C5", "E5"]),
    ("C3", ["C4", "E4", "G4"], ["G4", "C5", "E5", "G5"]),
    ("G2", ["G3", "B3", "D4"], ["G4", "B4", "D5", "F#5"]),
]
CHORD_LEN = 8.0

MIX = np.zeros(N)

# the drone under the opening reply: the tonic, low and quiet, swelling into the title
drone = pad_voice(note("A2"), level=0.5) + pad_voice(note("E3"), level=0.25)
drone_env = env(T, 0.0, END, 2.5, 2.0) * (0.55 + 0.45 * smooth(np.clip((T - 6.0) / (TITLE - 6.0), 0, 1)))
MIX += lowpass(drone, 420) * drone_env * 0.22

# the pad and the bass, chord by chord, from the title to the end
chord_i = 0
t_chord = TITLE
while t_chord < END:
    root, tones, _ = PROGRESSION[chord_i % len(PROGRESSION)]
    start, stop = t_chord, min(END, t_chord + CHORD_LEN)
    gate = env(T, start, stop + 1.2, 2.4, 2.4)
    pad = sum(pad_voice(note(n), level=1.0) for n in tones) / len(tones)
    bass = np.sin(2 * np.pi * note(root) * T) + 0.4 * np.sin(2 * np.pi * note(root) * 2 * T)
    MIX += lowpass(pad, 1400) * gate * 0.16
    MIX += lowpass(bass, 200) * gate * 0.12
    t_chord += CHORD_LEN
    chord_i += 1

# the plucked line: a slow arpeggio, denser in the skills scene, gone in the quiet scene
rng = np.random.default_rng(7)
t = TITLE + 1.0
while t < QUIET - 1.0:
    chord = PROGRESSION[int((t - TITLE) // CHORD_LEN) % len(PROGRESSION)]
    arp = chord[2]
    step = 1.0 if t < BLOCKS else (0.5 if MODES <= t < QUIET else 0.75)
    freq = note(arp[int((t - TITLE) / step) % len(arp)])
    level = 0.28 if t < RULES else 0.34
    if rng.random() < 0.85:
        pluck(freq, t, level=level)
    t += step

# a tick as each rule card lands
for f in CARDS:
    tick(f, level=0.55)

# the quiet scene: everything but the pad drops out
quiet = 1.0 - 0.75 * env(T, QUIET, CLOSE, 0.6, 1.0)
MIX *= quiet

# a final held chord that resolves, and a fade to silence
final = pad_voice(note("A3"), level=1.0) + pad_voice(note("C#4"), level=0.8) + pad_voice(note("E4"), level=0.8)
MIX += lowpass(final, 1200) * env(T, CLOSE + 2.0, END, 2.5, 0.5) * 0.12
MIX *= env(T, 0.0, END - 0.4, 0.01, 2.5)

# ---------- space: a small feedback-comb reverb, mixed in lightly ----------
def comb(x, delay_s, feedback):
    d = int(delay_s * SR)
    y = np.zeros_like(x)
    for k in range(0, len(x), d):
        chunk = x[k:k + d]
        prev = y[k - d:k] if k >= d else np.zeros(len(chunk))
        y[k:k + len(chunk)] = chunk + feedback * prev[:len(chunk)]
    return y


wet = sum(comb(MIX, s, g) for s, g in [(0.0297, 0.72), (0.0371, 0.70), (0.0411, 0.68), (0.0437, 0.66)]) / 4
wet = lowpass(wet, 3200)
mono = MIX * 0.82 + wet * 0.26

# a little width: the wet signal slightly delayed on the right
shift = int(0.011 * SR)
right = mono.copy()
right[shift:] = MIX[shift:] * 0.82 + wet[:-shift] * 0.26
stereo = np.stack([mono, right], axis=1)
stereo = stereo / (np.max(np.abs(stereo)) + 1e-9) * 0.74

out = sys.argv[1] if len(sys.argv) > 1 else "music.wav"
wavfile.write(out, SR, (stereo * 32767).astype(np.int16))
print(f"wrote {out}: {LENGTH:.0f}s, {SR} Hz, stereo, peak {np.max(np.abs(stereo)):.2f}")
