# The trailer

`salesman-trailer.mp4` is a three-minute, 16:9, silent trailer for salesman,
measured against caveman. Everything in it comes from this repo: the benchmark
replies in `benchmarks/examples/`, the rule mirror in `skills/salesman/SKILL.md`,
and the numbers that `benchmarks/bench.py` prints. Everything said about caveman
is from its own README and skill file, with its numbers as it reports them.

## How it is made

- `trailer.html` is the whole film as one web page: a 1920 by 1080 stage where
  every animation is a CSS animation with an absolute delay on a single
  three-minute timeline. `window.seek(seconds)` moves the page to any moment,
  so it can be rendered frame by frame instead of recorded.
- `render.js` opens the page in headless Chromium, seeks to each frame, takes a
  screenshot, and pipes the frames into ffmpeg, which encodes H.264.

To re-render after editing the page:

```bash
node trailer/render.js trailer/trailer.html trailer/salesman-trailer.mp4 30
```

It needs Playwright with Chromium, and an ffmpeg with libx264. A preview of a
short stretch is faster: add a start and end second, for example `30 45` at the
end of the command.

## Scenes

| Time | Scene |
|---|---|
| 0:00 | Cold open. Caveman's line, then "Who said the trick was the point?" |
| 0:10 | Title |
| 0:20 | Same question. Caveman answers in 20 tokens at once. Salesman streams to 644 |
| 0:45 | Same fix. The two `useMemo` blocks match |
| 1:00 | The mirror. Eight of caveman's rules flip into salesman's |
| 1:35 | Anatomy of one reply, block by block. The answer is deep in the stack |
| 1:55 | A tool run. One status line, or a narration around the same row |
| 2:12 | The three modes, with their token counts |
| 2:30 | Honest numbers |
| 2:42 | Your code stays yours |
| 2:50 | Install, sign-off, credits |
