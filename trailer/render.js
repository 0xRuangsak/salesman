// Renders trailer.html frame by frame in headless Chromium and encodes the frames with ffmpeg.
// The frames are split across parallel workers, each with its own browser and its own ffmpeg, and
// the segments are joined at the end. A separate browser per worker matters: pages that share one
// browser share its compositor, and the screenshots queue up behind it. If trailer/music.m4a exists
// next to the page, it is muxed in as the soundtrack of a full render.
// Usage: node trailer/render.js trailer/trailer.html trailer/salesman-trailer.mp4 [fps] [startSec] [endSec] [workers]
const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawn } = require("child_process");
const { chromium } = require("playwright");

const PAGE = path.resolve(process.argv[2]);
const OUT = path.resolve(process.argv[3]);
const FPS = Number(process.argv[4] || 24);
const START = Number(process.argv[5] || 0);
const END = process.argv[6] ? Number(process.argv[6]) : null;
const WORKERS = Number(process.argv[7] || Math.min(8, os.cpus().length + 2));
const MUSIC = path.join(path.dirname(PAGE), "music.m4a");
const X264 = ["-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-r", String(FPS)];

function ffmpeg(args) {
  const p = spawn("ffmpeg", ["-y", "-loglevel", "error", ...args], { stdio: ["pipe", "inherit", "inherit"] });
  p.stdin.on("error", (e) => { p.failed = e; });
  p.done = new Promise((resolve, reject) => p.on("close", (code) => (code === 0 ? resolve() : reject(new Error("ffmpeg exited " + code)))));
  return p;
}

(async () => {
  const errors = [];
  const open = async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
    page.on("pageerror", (e) => errors.push(e.message));
    await page.goto("file://" + PAGE);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(200);
    return { browser, page };
  };
  const probe = await open();
  const fonts = await probe.page.evaluate(() => ["Caladea", "Inter", "DejaVu Sans Mono"].map((f) => f + ":" + document.fonts.check("20px '" + f + "'")));
  const duration = END ?? (await probe.page.evaluate(() => window.DURATION));
  await probe.browser.close();
  const frames = Math.round((duration - START) * FPS);
  const hasMusic = fs.existsSync(MUSIC) && START === 0 && END === null;
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "trailer-"));
  const t0 = Date.now();
  let done = 0;
  const progress = setInterval(() => process.stderr.write(`frames ${done}/${frames} elapsed=${((Date.now() - t0) / 1000).toFixed(0)}s\n`), 10000);

  // each worker renders one contiguous run of frames into its own segment
  const per = Math.ceil(frames / WORKERS);
  const segments = await Promise.all(Array.from({ length: WORKERS }, async (_, k) => {
    const from = k * per, to = Math.min(frames, from + per);
    if (from >= to) return null;
    const { browser, page } = await open();
    const seg = path.join(tmp, `seg-${k}.mp4`);
    const ff = ffmpeg(["-f", "image2pipe", "-framerate", String(FPS), "-c:v", "mjpeg", "-i", "-", ...X264, seg]);
    for (let i = from; i < to; i++) {
      await page.evaluate((tt) => window.seek(tt), START + i / FPS);
      const buf = await page.screenshot({ type: "jpeg", quality: 94, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
      if (ff.failed) throw ff.failed;
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
      done++;
    }
    ff.stdin.end();
    await ff.done;
    await browser.close();
    return seg;
  }));
  clearInterval(progress);

  // join the segments, and the music when there is one
  const list = path.join(tmp, "segments.txt");
  fs.writeFileSync(list, segments.filter(Boolean).map((s) => `file '${s}'`).join("\n") + "\n");
  const args = ["-f", "concat", "-safe", "0", "-i", list];
  if (hasMusic) args.push("-i", MUSIC);
  args.push("-map", "0:v", "-c:v", "copy");
  if (hasMusic) args.push("-map", "1:a", "-c:a", "aac", "-b:a", "160k", "-shortest");
  args.push("-movflags", "+faststart", OUT);
  const join = ffmpeg(args);
  join.stdin.end();
  await join.done;
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log(JSON.stringify({ frames, fps: FPS, seconds: frames / FPS, workers: WORKERS, music: hasMusic, fonts, pageErrors: errors, elapsed: Math.round((Date.now() - t0) / 1000), out: OUT }));
})().catch((e) => { console.error("FAILED", e); process.exit(1); });
