# The trailer

`salesman-trailer.mp4` is a one-minute, 16:9 trailer for salesman. Everything in
it comes from this repo: the reply in `benchmarks/examples/salesman.md`, the
rules in `skills/salesman/SKILL.md`, and the numbers that `benchmarks/bench.py`
prints. Nothing else is on screen.

Everything needed to render it again is in this folder.

| File | What it is |
|---|---|
| `trailer.html` | The whole film as one web page. A 1920 by 1080 stage where every animation is a CSS animation with an absolute delay on a single one-minute timeline. `window.seek(seconds)` moves the page to any moment, so it is rendered frame by frame instead of recorded |
| `render.js` | Opens the page in headless Chromium, seeks to each frame, screenshots it, and pipes the frames into ffmpeg. The frames are split across parallel workers, one browser each, and joined at the end. Muxes `music.m4a` in when it exists |
| `music.py` | Composes the soundtrack in code: a pad, a bass, a plucked line, a tick as each rule card lands, a drop for the quiet scene. Nothing sampled, so the repo owns it |
| `music.m4a` | The soundtrack, as rendered by `music.py` and encoded with ffmpeg |
| `fonts/` | Caladea, Inter and DejaVu Sans Mono, with their license texts, so the page renders the same anywhere |

## Render

```bash
python3 trailer/music.py /tmp/music.wav && ffmpeg -y -i /tmp/music.wav -c:a aac -b:a 160k trailer/music.m4a
node trailer/render.js trailer/trailer.html trailer/salesman-trailer.mp4
```

The first line is only needed when `music.py` changes. Rendering needs
Playwright with Chromium, an ffmpeg with libx264, and Python with numpy and
scipy for the music. The render runs at 24 frames per second with one worker
per CPU core plus two; a full render takes about 80 seconds on four cores.
Optional arguments after the output path: frames per second, a start second,
an end second, and a worker count. A short stretch renders faster for previews,
for example `24 30 45`. Previews are silent.

## Scenes

| Time | Scene |
|---|---|
| 0:00 | The question. One ask, and the reply runs away from it: 644 tokens, counted as they stream |
| 0:11 | Title |
| 0:17 | One reply, in order. Eleven blocks, the answer deep in the stack |
| 0:28 | The rules. Eight cards, one rule each. The last one keeps going |
| 0:38 | One tool run. A narration before, a narration after |
| 0:45 | Three skills, with their token counts |
| 0:50 | Your code stays yours |
| 0:54 | Install, sign-off, credits |
