# The trailer

`salesman-trailer.mp4` is a three-minute, 16:9 trailer for salesman, measured
against caveman. Everything in it comes from this repo: the benchmark replies in
`benchmarks/examples/`, the rule mirror in `skills/salesman/SKILL.md`, and the
numbers that `benchmarks/bench.py` prints. Everything said about caveman is from
its own README and skill file, with its numbers as it reports them.

Everything needed to render it again is in this folder.

| File | What it is |
|---|---|
| `trailer.html` | The whole film as one web page. A 1920 by 1080 stage where every animation is a CSS animation with an absolute delay on a single three-minute timeline. `window.seek(seconds)` moves the page to any moment, so it is rendered frame by frame instead of recorded |
| `render.js` | Opens the page in headless Chromium, seeks to each frame, screenshots it, and pipes the frames into ffmpeg. Muxes `music.m4a` in when it exists |
| `music.py` | Composes the soundtrack in code: a pad, a bass, a plucked line, a tick on every rule-card flip, a drop for the quiet scene. Nothing sampled, so the repo owns it |
| `music.m4a` | The soundtrack, as rendered by `music.py` and encoded with ffmpeg |
| `fonts/` | Caladea, Inter and DejaVu Sans Mono, with their license texts, so the page renders the same anywhere |

## Render

```bash
python3 trailer/music.py /tmp/music.wav && ffmpeg -y -i /tmp/music.wav -c:a aac -b:a 160k trailer/music.m4a
node trailer/render.js trailer/trailer.html trailer/salesman-trailer.mp4 30
```

The first line is only needed when `music.py` changes. Rendering needs
Playwright with Chromium, an ffmpeg with libx264, and Python with numpy and
scipy for the music. A short stretch renders faster for previews: add a start
and an end second, for example `30 45`, at the end of the render command.
Previews are silent.

## Scenes

| Time | Scene |
|---|---|
| 0:00 | Cold open. Caveman's line, then "Who said the trick was the point?" |
| 0:10 | Title |
| 0:20 | Same question. Caveman answers in 20 tokens at once. Salesman streams to 644 |
| 0:45 | Same fix. Caveman's `useMemo` block slides onto salesman's and matches it |
| 1:00 | The mirror. Eight of caveman's rules flip into salesman's. The last one keeps going |
| 1:35 | One reply, in order. Eleven blocks, the answer deep in the stack |
| 1:55 | One tool run. One status line, or a narration around the same row |
| 2:12 | Three skills, with their token counts |
| 2:30 | Honest numbers. The salesman bars run off the frame |
| 2:42 | Your code stays yours |
| 2:50 | Install, sign-off, credits |
