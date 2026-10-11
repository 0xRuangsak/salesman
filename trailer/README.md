# The trailer

`salesman-trailer.mp4` is a one-minute, 16:9 trailer for salesman, recorded from
a [Drawdy](https://drawdy.io) board. Everything on screen comes from this repo:
the reply in `benchmarks/examples/salesman.md`, the rules in
`skills/salesman/SKILL.md`, and the numbers that `benchmarks/bench.py` prints.

## How it is made

The film is a Drawdy board, "Salesman trailer", with one 1600 by 900 frame per
scene. Every element on it is a Drawdy element (text, shapes, sticky notes,
cards, a speech bubble, freehand strokes, Drawdy's bar chart) and carries a
Drawdy animation that plays when the board opens. The board is the source;
the frames are also its slides, in order, so it can be presented from Drawdy.

`record.js` opens the board in headless Chromium through a view link, one fresh
page per scene, with the camera locked on that scene's frame. Before the page
loads, the browser's frame timer is swapped for a virtual clock that holds at
zero while the board loads and then advances exactly one video frame per
screenshot, so the recording is smooth and the same on any machine. The scenes
are joined with slides that follow the layout of the board, and the soundtrack
is laid under them.

| File | What it is |
|---|---|
| `record.js` | Records the board scene by scene and cuts the video. The scene list, their frames and durations, is at the top |
| `soundtrack.py` | Composes the music bed and the sound effects in code: a pop for the question, taps for the reply, a rising tone with the token meter, a cash register at 644, paper slaps for the rules, a check for the tool run, glides for the bars. Nothing is sampled, so the repo owns it |
| `soundtrack.m4a` | The soundtrack, as rendered by `soundtrack.py` |
| `keyframes.py` | The helpers that wrote the board's animations: fades, drops, pops, slaps, bars growing from their base |

## Render

```bash
python3 trailer/soundtrack.py /tmp/soundtrack.wav
ffmpeg -y -i /tmp/soundtrack.wav -c:a aac -b:a 192k trailer/soundtrack.m4a
DRAWDY_VIEW_URL="<a view-only link to the board>" node trailer/record.js trailer/salesman-trailer.mp4
```

The first two lines are only needed when `soundtrack.py` changes. The view
link comes from the board's Share dialog; it is not stored in the repo.
Rendering needs Playwright with Chromium, an ffmpeg with libx264, network
access to drawdy.io, and Python with numpy and scipy for the soundtrack. A full
render takes about four minutes on four cores. Optional arguments after the
output path: frames per second, a worker count, and a single scene number to
record on its own for a preview.

## Scenes

| Time | Scene |
|---|---|
| 0:00 | The question. The reply arrives paragraph by paragraph while a token meter fills to 644, far past a normal agent's 63 |
| 0:11 | Title. The letters rise one by one, a green line is drawn under them, a sticker says 10.2x more words |
| 0:17 | One reply, in order. Eleven rows drop in, the answer lands fifth and pulses, an arrow marks it |
| 0:28 | The rules. Eight sticky notes are slapped on; the last one, "Always performs", keeps rocking |
| 0:38 | One tool run. A narration, the tool row with a spinner that turns into a check, three narration cards |
| 0:45 | Three skills, and Drawdy's bar chart of their token counts, the bars growing |
| 0:50 | Your code stays yours. An empty signature line |
| 0:53.5 | Install command, "Act now.", credits |
