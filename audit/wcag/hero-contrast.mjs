// Erfasst den Hero-Hintergrund (Text ausgeblendet) + Element-Rects/Farben fuer die WCAG-Pixelmessung
// von Text UEBER Bild (1.4.3). Analyse: analyze_contrast.py.
// Lauf: node audit/wcag/hero-contrast.mjs <url> <width> <height> <outBgPng> <outJson> [selectorsCSV]
//   (Dev-Server noetig; Chrome-Pfad ggf. anpassen.)
import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';

const [, , url, wArg, hArg, outPng, outJson, selCsv] = process.argv;
const W = +wArg || 390, H = +hArg || 844;
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = 9355;
const SELS = (selCsv || '.b-hero .b-eyebrow|.b-hero h1|.b-hero .b-lead').split('|');

const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, '--hide-scrollbars',
  '--no-first-run', '--no-default-browser-check', '--user-data-dir=' + process.env.TEMP + '/cdp-contrast-' + W, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function wsUrl() { for (let i = 0; i < 40; i++) { try { const r = await fetch(`http://localhost:${PORT}/json/list`); const t = await r.json(); const p = t.find(x => x.type === 'page'); if (p?.webSocketDebuggerUrl) return p.webSocketDebuggerUrl; } catch {} await sleep(250); } throw new Error('no devtools'); }
function mk(ws) { let id = 0; const p = new Map(); ws.addEventListener('message', e => { const m = JSON.parse(e.data); if (m.id && p.has(m.id)) { p.get(m.id)(m); p.delete(m.id); } }); return (method, params = {}) => new Promise(res => { const i = ++id; p.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); }); }
const ws = new WebSocket(await wsUrl()); await new Promise(r => ws.addEventListener('open', r));
const send = mk(ws);
async function evalJs(expr) { const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true }); return r.result?.result?.value; }
await send('Page.enable'); await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 2, mobile: true });
await send('Page.navigate', { url }); await sleep(2400);
await evalJs(`(()=>{try{localStorage.setItem('aurea-consent-v1','all')}catch(e){};location.reload();return 1})()`);
await sleep(3200);
const expr = `(() => {
  const sels = ${JSON.stringify(SELS)};
  const out = { dpr: window.devicePixelRatio, vw: innerWidth, vh: innerHeight, items: [] };
  for (const s of sels) {
    const e = document.querySelector(s); if (!e) continue;
    const r = e.getBoundingClientRect(); if (r.width < 1 || r.height < 1) continue;
    const cs = getComputedStyle(e);
    out.items.push({ sel: s, x: r.left, y: r.top, w: r.width, h: r.height, color: cs.color, fontSize: parseFloat(cs.fontSize), fontWeight: cs.fontWeight });
    e.style.visibility = 'hidden';
  }
  return JSON.stringify(out);
})()`;
const data = await evalJs(expr);
writeFileSync(outJson, data);
const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
writeFileSync(outPng, Buffer.from(shot.result.data, 'base64'));
console.log('OK ' + outPng + ' | ' + outJson + ' | items=' + JSON.parse(data).items.length);
ws.close(); chrome.kill(); process.exit(0);
