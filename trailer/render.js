// Renders trailer.html frame by frame in headless Chromium and pipes the frames into ffmpeg.
// Usage: node render.js <trailer.html> <out.mp4> [fps] [startSec] [endSec]
const path = require("path");
const { spawn } = require("child_process");
const { chromium } = require("playwright");

const FILE = "file://" + path.resolve(process.argv[2]);
const OUT = path.resolve(process.argv[3]);
const FPS = Number(process.argv[4] || 30);
const START = Number(process.argv[5] || 0);
const END = process.argv[6] ? Number(process.argv[6]) : null;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto(FILE);
  await page.waitForTimeout(500);
  await page.evaluate(() => document.fonts.ready);
  const duration = END ?? (await page.evaluate(() => window.DURATION));
  const frames = Math.round((duration - START) * FPS);

  const ff = spawn("ffmpeg", [
    "-y", "-loglevel", "error",
    "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "mjpeg", "-i", "-",
    "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p", "-r", String(FPS),
    "-movflags", "+faststart", OUT
  ], { stdio: ["pipe", "inherit", "inherit"] });

  const write = (buf) => new Promise((resolve, reject) => {
    if (ff.stdin.write(buf)) return resolve();
    ff.stdin.once("drain", resolve); ff.stdin.once("error", reject);
  });

  const t0 = Date.now();
  for (let i = 0; i < frames; i++) {
    const t = START + i / FPS;
    await page.evaluate((tt) => window.seek(tt), t);
    const buf = await page.screenshot({ type: "jpeg", quality: 93, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
    await write(buf);
    if (i % (FPS * 10) === 0) process.stderr.write(`frame ${i}/${frames} t=${t.toFixed(1)}s elapsed=${((Date.now() - t0) / 1000).toFixed(0)}s\n`);
  }
  ff.stdin.end();
  await new Promise((resolve) => ff.on("close", resolve));
  await browser.close();
  console.log(JSON.stringify({ frames, fps: FPS, seconds: frames / FPS, pageErrors: errors, out: OUT }));
})().catch((e) => { console.error("FAILED", e); process.exit(1); });
