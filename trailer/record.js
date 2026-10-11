// Records the salesman trailer from its Drawdy board, frame by frame, and cuts it into one video.
//
//   DRAWDY_VIEW_URL="https://drawdy.io/?canvas=<id>&token=<view token>" \
//     node trailer/record.js trailer/salesman-trailer.mp4 [fps] [workers] [only-scene]
//
// The board has one 1600 by 900 frame per scene. Every element on it carries a Drawdy animation that
// starts when the board opens, so each scene is recorded from its own fresh page load with the camera
// locked on its frame. Before the page loads, performance.now and requestAnimationFrame are replaced by
// a virtual clock that holds at zero while the board loads and then advances exactly one video frame
// per capture, so the recording is smooth and the same every time, however slow the machine.
// The scenes are joined with slides that follow the layout of the board, the soundtrack
// (trailer/soundtrack.m4a, made by trailer/soundtrack.py) is laid under it, and the result is encoded
// with libx264. Rendering needs Playwright with Chromium and an ffmpeg with libx264.
const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawn } = require("child_process");
const { chromium } = require("playwright");

const SCENES = [
  { name: "question", frame: [0, 0], seconds: 11 },
  { name: "title", frame: [1720, 0], seconds: 6 },
  { name: "reply", frame: [3440, 0], seconds: 11 },
  { name: "rules", frame: [5160, 0], seconds: 10 },
  { name: "tool run", frame: [0, 1020], seconds: 7 },
  { name: "skills", frame: [1720, 1020], seconds: 5 },
  { name: "code", frame: [3440, 1020], seconds: 3.5 },
  { name: "install", frame: [5160, 1020], seconds: 6.5 },
];
const FRAME = [1600, 900];
const VIEW = [1920, 1080];
const ZOOM = (VIEW[0] / FRAME[0]) * 1.01; // a hair past the frame, so its border stays out of shot
const SLIDE = 0.6; // seconds each transition overlaps the next scene
const FADE_IN = 0.5, FADE_OUT = 0.8;

const URL = process.env.DRAWDY_VIEW_URL;
const OUT = path.resolve(process.argv[2] || "salesman-trailer.mp4");
const FPS = Number(process.argv[3] || 30);
const WORKERS = Number(process.argv[4] || Math.min(4, os.cpus().length));
const ONLY = process.argv[5] != null ? Number(process.argv[5]) : null;
const SOUND = path.join(__dirname, "soundtrack.m4a");
const X264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-r", String(FPS)];
if (!URL) { console.error("Set DRAWDY_VIEW_URL to a view link of the board (Share, then copy a view-only link)."); process.exit(1); }

// The virtual clock, installed before any page script runs.
const CLOCK = `(() => {
  try { localStorage.setItem("theme", "dark"); } catch (e) {}
  const realRaf = window.requestAnimationFrame.bind(window);
  const realSetInterval = window.setInterval.bind(window), realClearInterval = window.clearInterval.bind(window);
  const vc = { t: 0, queue: new Map(), nextId: 1, pump: null };
  performance.now = () => vc.t;
  window.requestAnimationFrame = (cb) => { const id = vc.nextId++; vc.queue.set(id, cb); return id; };
  window.cancelAnimationFrame = (id) => { vc.queue.delete(id); };
  vc.step = (ms) => {
    vc.t += ms;
    const batch = [...vc.queue.values()]; vc.queue.clear();
    for (const cb of batch) { try { cb(vc.t); } catch (e) { console.error("frame callback", e); } }
  };
  vc.startPump = () => { if (!vc.pump) vc.pump = realSetInterval(() => vc.step(0), 16); };
  vc.stopPump = () => { if (vc.pump) { realClearInterval(vc.pump); vc.pump = null; } };
  vc.painted = () => new Promise((r) => realRaf(() => realRaf(r)));
  vc.startPump();
  window.__vc = vc;
})();`;

// Finds the board's editor engine (the object that owns the camera) by walking the React fiber tree.
const FIND_ENGINE = `window.__findEngine = () => {
  const seen = new WeakSet();
  const looks = (o) => o && typeof o === "object" && o.viewportManager && typeof o.viewportManager.setTransform === "function";
  const search = (v, depth) => {
    if (!v || typeof v !== "object" || seen.has(v) || depth > 4) return null;
    seen.add(v);
    if (looks(v)) return v;
    if (v instanceof Node || v instanceof Window) return null;
    let keys; try { keys = Object.keys(v); } catch (e) { return null; }
    for (const k of keys.slice(0, 60)) { let c; try { c = v[k]; } catch (e) { continue; } const r = search(c, depth + 1); if (r) return r; }
    return null;
  };
  const fiberKey = (el) => Object.keys(el).find((k) => k.startsWith("__reactFiber$"));
  const visited = new WeakSet();
  for (const el of document.querySelectorAll("*")) {
    const key = fiberKey(el); if (!key) continue;
    for (let f = el[key], up = 0; f && up < 200; up++, f = f.return) {
      if (visited.has(f)) break; visited.add(f);
      for (const v of [f.memoizedProps, f.stateNode && !(f.stateNode instanceof Node) ? f.stateNode : null]) { const r = search(v, 0); if (r) return r; }
      for (let h = f.memoizedState, i = 0; h && i < 50; i++, h = h.next) { const r = search(h.memoizedState, 0); if (r) return r; }
    }
  }
  return null;
};`;

function ffmpeg(args) {
  const p = spawn("ffmpeg", ["-y", "-loglevel", "error", ...args], { stdio: ["pipe", "inherit", "inherit"] });
  p.stdin.on("error", (e) => { p.failed = e; });
  p.done = new Promise((resolve, reject) => p.on("close", (c) => (c === 0 ? resolve() : reject(new Error("ffmpeg exited " + c)))));
  return p;
}

async function openBoard(browser) {
  const ctx = await browser.newContext({ viewport: { width: VIEW[0], height: VIEW[1] }, colorScheme: "dark", deviceScaleFactor: 1 });
  await ctx.addInitScript(CLOCK);
  await ctx.addInitScript(FIND_ENGINE);
  const page = await ctx.newPage();
  for (let attempt = 1; ; attempt++) {
    await page.goto(URL, { waitUntil: "domcontentloaded", timeout: 90000 });
    let ok = false;
    for (let i = 0; i < 30 && !ok; i++) {
      ok = await page.evaluate(() => document.querySelectorAll("canvas").length >= 4 && !!window.__findEngine());
      if (!ok) await page.waitForTimeout(1000);
    }
    if (ok) break;
    if (attempt >= 4) throw new Error("the board did not load");
  }
  await page.waitForTimeout(2500); // fonts and the board data settle; the clock is still at zero
  await page.addStyleTag({ content: "body * { visibility: hidden !important; } canvas { visibility: visible !important; }" });
  await page.evaluate(() => { for (const c of document.querySelectorAll("canvas")) if (c.width < 400) c.style.display = "none"; });
  return { ctx, page };
}

async function recordScene(browser, k, seg, log) {
  const s = SCENES[k];
  const seconds = s.seconds + (k < SCENES.length - 1 ? SLIDE : 0);
  const frames = Math.round(seconds * FPS);
  const { ctx, page } = await openBoard(browser);
  const [fx, fy] = s.frame;
  await page.evaluate(([cx, cy, z, vw, vh]) => {
    window.__engine = window.__findEngine();
    window.__engine.viewportManager.setTransform(z, { x: vw / 2 - cx * z, y: vh / 2 - cy * z });
  }, [fx + FRAME[0] / 2, fy + FRAME[1] / 2, ZOOM, VIEW[0], VIEW[1]]);
  const t0 = await page.evaluate(() => { window.__vc.stopPump(); window.__vc.step(0); return window.__vc.t; });
  if (t0 !== 0) throw new Error("animation clock moved during load: " + t0);
  const ff = ffmpeg(["-f", "image2pipe", "-framerate", String(FPS), "-c:v", "mjpeg", "-i", "-", ...X264, seg]);
  for (let i = 0; i < frames; i++) {
    if (i > 0) await page.evaluate((ms) => { window.__vc.step(ms); window.__vc.step(0); }, 1000 / FPS);
    await page.evaluate(() => window.__vc.painted());
    const buf = await page.screenshot({ type: "jpeg", quality: 95, clip: { x: 0, y: 0, width: VIEW[0], height: VIEW[1] } });
    if (ff.failed) throw ff.failed;
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
  }
  ff.stdin.end();
  await ff.done;
  await ctx.close();
  log(`scene ${k + 1} (${s.name}): ${frames} frames`);
}

(async () => {
  const t0 = Date.now();
  const log = (m) => process.stderr.write(`[${((Date.now() - t0) / 1000).toFixed(0)}s] ${m}\n`);
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "trailer-"));
  const todo = ONLY != null ? [ONLY - 1] : SCENES.map((_, k) => k);
  const segs = SCENES.map((_, k) => path.join(tmp, `scene-${k + 1}.mp4`));
  const queue = [...todo];
  await Promise.all(Array.from({ length: Math.min(WORKERS, todo.length) }, async () => {
    const browser = await chromium.launch(process.env.HTTPS_PROXY ? { proxy: { server: process.env.HTTPS_PROXY } } : {});
    for (let k; (k = queue.shift()) !== undefined;) await recordScene(browser, k, segs[k], log);
    await browser.close();
  }));

  if (ONLY != null) {
    fs.copyFileSync(segs[ONLY - 1], OUT);
  } else {
    // join: each scene slides in over the last SLIDE seconds of the one before, in the direction the
    // camera would travel across the board
    const inputs = segs.flatMap((s) => ["-i", s]);
    const hasSound = fs.existsSync(SOUND);
    if (hasSound) inputs.push("-i", SOUND);
    const parts = [];
    let prev = "[0:v]", start = 0;
    for (let k = 1; k < SCENES.length; k++) {
      start += SCENES[k - 1].seconds;
      const down = SCENES[k].frame[1] > SCENES[k - 1].frame[1];
      const label = `[v${k}]`;
      parts.push(`${prev}[${k}:v]xfade=transition=${down ? "slideup" : "slideleft"}:duration=${SLIDE}:offset=${start}${label}`);
      prev = label;
    }
    const total = SCENES.reduce((a, s) => a + s.seconds, 0);
    parts.push(`${prev}fade=t=in:st=0:d=${FADE_IN},fade=t=out:st=${total - FADE_OUT}:d=${FADE_OUT}[vout]`);
    const args = [...inputs, "-filter_complex", parts.join(";"), "-map", "[vout]"];
    if (hasSound) args.push("-map", `${SCENES.length}:a`, "-c:a", "aac", "-b:a", "192k", "-t", String(total));
    args.push(...X264, "-movflags", "+faststart", OUT);
    const join = ffmpeg(args); join.stdin.end(); await join.done;
    log(`joined ${SCENES.length} scenes, ${total} s, sound: ${hasSound}`);
  }
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log(JSON.stringify({ out: OUT, fps: FPS, scenes: todo.length, elapsed: Math.round((Date.now() - t0) / 1000) }));
})().catch((e) => { console.error("FAILED", e); process.exit(1); });
