import os
import asyncio, subprocess, time, sys
from playwright.async_api import async_playwright

# Browser used for the checks: $CHROME if set, else a system Chrome, else Playwright's own Chromium
# (install it once with: python3 -m playwright install chromium).
_chrome = os.environ.get("CHROME") or next((c for c in ("/usr/bin/google-chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome") if os.path.exists(c)), None)
BROWSER = dict(executable_path=_chrome, args=["--no-sandbox"]) if _chrome else {}
SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
TEST = os.path.join(os.path.dirname(SITE), "test"); os.makedirs(TEST, exist_ok=True)

async def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8765", "--directory", SITE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch(**BROWSER)
            pg = await b.new_page(viewport={"width": 1280, "height": 900}); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            await pg.goto("http://localhost:8765/index.html"); await pg.wait_for_timeout(800)
            await pg.screenshot(path=f"{TEST}/site_home.png")
            for n in range(1, 11):
                await pg.evaluate(f"location.hash = '#session-{n}'"); await pg.wait_for_timeout(700)
                info = await pg.evaluate("""() => { const s = document.getElementById('session'); const bad = [];
                  s.querySelectorAll('.figwrap').forEach(w => { if (w.getBoundingClientRect().width > w.parentElement.clientWidth + 2) bad.push('fig too wide'); });
                  if (document.documentElement.scrollWidth > window.innerWidth + 2) bad.push('page scrolls sideways');
                  return { blocks: s.querySelectorAll('.blk').length, widgets: [...s.querySelectorAll('.widget')].map(w => w.dataset.w + ':' + (w.querySelector('.read') ? w.querySelector('.read').textContent.slice(0, 60) : 'NO READ')), quiz: s.querySelectorAll('.qopt').length, bad }; }""")
                print(n, info)
                if n in (1, 6, 10):
                    wdg = await pg.query_selector(".widget")
                    if wdg:
                        await wdg.scroll_into_view_if_needed(); await pg.wait_for_timeout(200)
                        await pg.screenshot(path=f"{TEST}/site_s{n}.png")
            # interaction smoke test
            await pg.evaluate("location.hash = '#session-3'"); await pg.wait_for_timeout(600)
            await pg.evaluate("""() => { const i = document.querySelector('.widget input[type=range]'); i.value = 9; i.dispatchEvent(new Event('input')); document.querySelector('.qopt').click(); }""")
            print("after slider:", await pg.evaluate("document.querySelector('.widget .read').textContent"), "| quiz why shown:", await pg.evaluate("!document.querySelector('.qwhy').hidden"))
            await pg.set_viewport_size({"width": 400, "height": 800}); await pg.wait_for_timeout(400)
            print("mobile sideways scroll:", await pg.evaluate("document.documentElement.scrollWidth > window.innerWidth + 2"))
            await pg.screenshot(path=f"{TEST}/site_mobile.png")
            print("errors:", errs[:5])
            await b.close()
    finally:
        srv.terminate()
asyncio.run(main())
