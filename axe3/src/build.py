import sys, importlib, os, asyncio, json
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

# Browser used for the checks: $CHROME if set, else a system Chrome, else Playwright's own Chromium
# (install it once with: python3 -m playwright install chromium).
_chrome = os.environ.get("CHROME") or next((c for c in ("/usr/bin/google-chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome") if os.path.exists(c)), None)
BROWSER = dict(executable_path=_chrome, args=["--no-sandbox"]) if _chrome else {}
HERE = os.path.dirname(__file__); ROOT = os.path.dirname(HERE)
CSS = open(f"{HERE}/deck.css").read()
ALL = ["a1", "a2", "a3", "a4", "b1", "b2", "b3", "b4", "b5", "b6"]

def load(names):
    return [importlib.import_module(n).build() for n in names]

CHECK_JS = """() => { const out = [];
 document.querySelectorAll('section').forEach(sec => { const r = sec.getBoundingClientRect(); const bad = [];
  const limit = r.top + 1080 - 100;
  sec.querySelectorAll('.hd, .bd > *, .st-t, .st-s, .cv-t, .cv-s, .cv-b, .nx, .cols > *, .cl > *, .t-r, .row, .cd, .cd-l, .sy-r, .plot, .eqb svg').forEach(e => {
    const b = e.getBoundingClientRect();
    if (b.bottom > limit + 1 || b.right > r.left + 1920 - 120 || b.left < r.left + 100) bad.push(e.className + ' b=' + Math.round(b.bottom - r.top) + ' r=' + Math.round(b.right - r.left)); });
  const bd = sec.querySelector('.bd'); if (bd && bd.scrollHeight > bd.clientHeight + 2) bad.push('bd-scroll ' + bd.scrollHeight + '>' + bd.clientHeight);
  sec.querySelectorAll('.cd-l').forEach(p => { const c = p.parentElement.getBoundingClientRect(); if (p.getBoundingClientRect().right > c.right - 20 || p.scrollWidth > p.parentElement.clientWidth) bad.push('code line too long: ' + p.textContent.slice(0, 24)); });
  sec.querySelectorAll('.eqb svg, .sy-s svg').forEach(e => { const c = e.closest('.eqb, .sy-s').getBoundingClientRect(), b = e.getBoundingClientRect(); if (b.right > c.right + 2 || b.left < c.left - 2) bad.push('equation wider than its box'); });
  const hd = sec.querySelector('.hd'), b0 = sec.querySelector('.bd > *');
  if (hd && b0 && b0.getBoundingClientRect().top < hd.getBoundingClientRect().bottom - 1) bad.push('body overlaps header');
  sec.querySelectorAll('.plot p').forEach(p => { if (p.scrollWidth > p.clientWidth + 2) bad.push('label wider than box: ' + p.textContent.slice(0, 30));
    const pr = p.parentElement.getBoundingClientRect(), b = p.getBoundingClientRect();
    if (b.right > pr.right + 3 || b.left < pr.left - 3 || b.bottom > pr.bottom + 3 || b.top < pr.top - 3) bad.push('label outside figure: ' + p.textContent.slice(0, 30)); });
  if (bad.length) out.push(sec.id + ': ' + [...new Set(bad)].slice(0, 6).join(' | ')); });
 return out; }"""

async def shots(names):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(**BROWSER)
        for n in names:
            pg = await b.new_page(viewport={"width": 1920, "height": 1080})
            await pg.goto(f"file://{ROOT}/test/{n}.html"); await pg.wait_for_timeout(1200)
            try: await pg.evaluate("document.fonts.ready")
            except Exception: pass
            bad = await pg.evaluate(CHECK_JS)
            print(n, "overflow:", bad if bad else "none")
            if "--shots" in sys.argv:
                os.makedirs(f"{ROOT}/test/{n}", exist_ok=True)
                secs = await pg.query_selector_all("section")
                for i, s in enumerate(secs):
                    await s.screenshot(path=f"{ROOT}/test/{n}/s{i + 1:02d}.png")
            await pg.close()
        await b.close()

if __name__ == "__main__":
    names = [a for a in sys.argv[1:] if not a.startswith("--")] or ALL
    for n, S in zip(names, load(names)):
        root = f"{ROOT}/out/{n}"
        ids = build_deck(S, root, CSS)
        os.makedirs(f"{ROOT}/test", exist_ok=True)
        harness(S, root, f"{ROOT}/test/{n}.html")
        words = sum(len(strip(s["notes"]).split()) for s in S.slides)
        big = max(os.path.getsize(f"{root}/project/slides/{i}.html") for i in ids)
        print(f"{n}: {len(ids)} slides, {words} words of notes, largest slide {big // 1024} KB")
    asyncio.run(shots(names))
