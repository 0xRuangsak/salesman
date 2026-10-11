"""Keyframe helpers used to write the animations on the trailer's Drawdy board.

A Drawdy element can carry one localAnimation: a few transform tracks (x, y offset, width and height
scale, rotation, opacity) sampled evenly over durationMs, at most 32 keyframes, starting when the
board opens. An entrance that starts late is therefore a hold followed by the move. Every scene is
recorded from a fresh page load, so the times here are milliseconds from the start of the scene.

    from keyframes import fade_up
    element["localAnimation"] = fade_up(1600, 420, 18)   # rises 18 units into place at 1.6 s
"""
import json
import math

GREEN, AMBER, GRAY = "#15a046", "#c76a04", "#868e96"  # each reads at 3:1 or better on light and dark boards


def clamp(x):
    return max(0.0, min(1.0, x))


def out_cubic(p):
    return 1 - (1 - p) ** 3


def out_back(p, s=1.70158):
    p -= 1
    return 1 + (s + 1) * p ** 3 + s * p ** 2


def prog(t, d, dur):
    return clamp((t - d) / dur) if dur > 0 else (1.0 if t >= d else 0.0)


def anim(total, **fns):
    """localAnimation from functions of t (ms), sampled evenly: enough keyframes for ~40 ms resolution,
    at most 32. A move that starts late gets fewer keyframes, so late moves are kept short and simple."""
    total = max(1, round(total))
    k = max(2, min(32, math.ceil(total / 40) + 1))
    tr = {}
    for name, fn in fns.items():
        tr[name] = [round(fn(total * i / (k - 1)), 3) for i in range(k)]
    return {"time": {"durationMs": total, "curve": "linear", "repeat": "none"},
            "animation": {"curve": "linear", "transform": tr}}


def fade_up(d, dur=500, dy=26):
    return anim(d + dur, opacity=lambda t: out_cubic(prog(t, d, dur)),
                y=lambda t: dy * (1 - out_cubic(prog(t, d, dur))))


def fade(d, dur=400):
    return anim(d + dur, opacity=lambda t: prog(t, d, dur))


def drop(d, dur=450, dy=-34):
    return anim(d + dur, opacity=lambda t: clamp(prog(t, d, dur) * 2.5),
                y=lambda t: dy * (1 - out_cubic(prog(t, d, dur))))


def pop(d, dur=550, s0=0.4, rot0=0.0, extra_total=0, after_rot=0.0):
    """Scale up with a small overshoot. After landing it may keep turning slowly (after_rot radians)."""
    total = d + dur + extra_total
    def s(t):
        return s0 + (1 - s0) * out_back(prog(t, d, dur))
    def r(t):
        p = prog(t, d, dur)
        return rot0 * (1 - out_cubic(p)) + after_rot * prog(t, d + dur, extra_total)
    fns = {"opacity": lambda t: clamp(prog(t, d, dur) * 3), "width": s, "height": s}
    if rot0 or after_rot:
        fns["rotation"] = r
    return anim(total, **fns)


def grow_up(d, dur, h, shape=out_cubic):
    """Height grows from the bottom edge: scale about the center plus an offset that pins the bottom."""
    def s(t):
        return max(0.002, shape(prog(t, d, dur)))
    return anim(d + dur, height=s, y=lambda t: h * (1 - s(t)) / 2)


def grow_right(d, dur, w, shape=out_cubic):
    """Width grows from the left edge."""
    def s(t):
        return max(0.002, shape(prog(t, d, dur)))
    return anim(d + dur, width=s, x=lambda t: -w * (1 - s(t)) / 2)


def slap(d, dur=520, rot0=0.22, wiggle_until=0, wiggle_amp=0.07, wiggle_period=1290):
    """A sticky note slapped onto the board: big and turned, then down with a small squash.
    With wiggle_until, it keeps rocking after it lands until that time."""
    total = max(d + dur, wiggle_until)
    def s(t):
        p = prog(t, d, dur)
        if p < 0.7:
            return 1.45 + (0.95 - 1.45) * out_cubic(p / 0.7)
        return 0.95 + 0.05 * out_cubic((p - 0.7) / 0.3)
    # the rocking starts on a keyframe and swings a quarter turn per keyframe, so it samples as an even
    # triangle wave instead of aliasing against Drawdy's evenly spaced keyframes
    step = total / 31
    w0 = math.ceil((d + dur) / step) * step
    def r(t):
        base = rot0 * (1 - out_cubic(prog(t, d, dur)))
        if wiggle_until and t >= w0 - 1:
            base += wiggle_amp * math.sin(2 * math.pi * (t - w0) / (4 * step))
        return base
    return anim(total, opacity=lambda t: clamp(prog(t, d, dur) * 3.5), width=s, height=s, rotation=r)


def dump(elements):
    return json.dumps(elements, ensure_ascii=False, separators=(",", ":"))
