// Renders trailer.html frame by frame in headless Chromium and pipes the frames into ffmpeg.
// If trailer/music.m4a exists next to the page, it is muxed in as the soundtrack.
// Usage: node trailer/render.js trailer/trailer.html trailer/salesman-trailer.mp4 [fps] [startSec] [endSec]
const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");
const { chromium } = require("playwright");

const PAGE = path.resolve(process.argv[2]);
const OUT = path.resolve(process.argv[3]);
const FPS = Number(process.argv[4] || 30);
const START = Number(process.argv[5] || 0);
const END = process.argv[6] ? Number(process.argv[6]) : null;
const MUSIC = path.join(path.dirname(PAGE), "music.m4a");

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("file://" + PAGE);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  const fonts = await page.evaluate(() => ["Caladea", "Inter", "DejaVu Sans Mono"].map((f) => f + ":" + document.fonts.check("20px '" + f + "'")));
  const duration = END ?? (await page.evaluate(() => window.DURATION));
  const frames = Math.round((duration - START) * FPS);

  const hasMusic = fs.existsSync(MUSIC) && START === 0 && END === null;
  const args = ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "mjpeg", "-i", "-"];
  if (hasMusic) args.push("-i", MUSIC);
  args.push("-map", "0:v");
  if (hasMusic) args.push("-map", "1:a", "-c:a", "aac", "-b:a", "160k", "-shortest");
  args.push("-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-r", String(FPS), "-movflags", "+faststart", OUT);
  const ff = spawn("ffmpeg", args, { stdio: ["pipe", "inherit", "inherit"] });
  const write = (buf) => new Promise((resolve, reject) => { if (ff.stdin.write(buf)) return resolve(); ff.stdin.once("drain", resolve); ff.stdin.once("error", reject); });

  const t0 = Date.now();
  for (let i = 0; i < frames; i++) {
    const t = START + i / FPS;
    await page.evaluate((tt) => window.seek(tt), t);
    await write(await page.screenshot({ type: "jpeg", quality: 94, clip: { x: 0, y: 0, width: 1920, height: 1080 } }));
    if (i % (FPS * 10) === 0) process.stderr.write(`frame ${i}/${frames} t=${t.toFixed(1)}s elapsed=${((Date.now() - t0) / 1000).toFixed(0)}s\n`);
  }
  ff.stdin.end();
  await new Promise((resolve) => ff.on("close", resolve));
  await browser.close();
  console.log(JSON.stringify({ frames, fps: FPS, seconds: frames / FPS, music: hasMusic, fonts, pageErrors: errors, out: OUT }));
})().catch((e) => { console.error("FAILED", e); process.exit(1); });
