# /// script
# requires-python = ">=3.12"
# dependencies = ["playwright==1.63.0"]
# ///
"""Run after mkdocs build: uv run scripts/check_pip_reading.py."""

import re
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from shutil import which
from threading import Thread

from playwright.sync_api import sync_playwright, expect


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def main():
    site = Path(__file__).resolve().parents[1] / "site"
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=site))
    Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path=which("google-chrome"))
            try:
                for scenario in ("nearby pointer", "moving pointer", "close chat", "no interaction", "mobile"):
                    page = browser.new_page(
                        reduced_motion="no-preference",
                        viewport={"width": 390, "height": 844} if scenario == "mobile" else {"width": 1280, "height": 720},
                        is_mobile=scenario == "mobile",
                        has_touch=scenario == "mobile",
                    )
                    page.add_init_script("Math.random = () => 0.5")
                    page.clock.install(time=1_800_000_000_000)
                    page.clock.pause_at(1_800_000_001_000)
                    page.goto(f"http://127.0.0.1:{server.server_port}/airflow/architecture/")
                    robot = page.locator(".pip-chat")
                    if scenario == "nearby pointer":
                        box = page.locator(".pip-mascot-wrapper").bounding_box()
                        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + 30)
                    elif scenario == "close chat":
                        page.locator(".pip-launcher").click()
                        page.clock.run_for(500)
                        page.keyboard.press("Escape")
                        expect(page.locator(".pip-launcher")).to_be_focused()

                    # Reaching for the book starts five seconds after mounting/resuming.
                    if scenario == "moving pointer":
                        page.clock.run_for(3_000)
                        box = page.locator(".pip-mascot-wrapper").bounding_box()
                        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + 30)
                        page.clock.run_for(1_000)
                        page.mouse.move(0, 0)
                        page.clock.run_for(999)
                    else:
                        page.clock.run_for(4_999)
                    assert robot.get_attribute("data-pose") not in ("opening", "reading")
                    page.clock.run_for(1)
                    expect(robot).to_have_attribute("data-pose", "opening")
                    for _ in range(3):
                        page.clock.run_for(350)
                        expect(robot).to_have_attribute("data-pose", "reading")
                        page.clock.run_for(1_000)
                        expect(page.locator(".pip-book-open")).to_have_css("opacity", "1")
                        expect(page.locator(".pip-book-closed")).to_have_css("opacity", "0")
                        # Both hands support the outside edges, leaving the pages visible.
                        hands = page.evaluate("""() => {
                            const book = document.querySelector('.pip-book-open').getBoundingClientRect();
                            return ['.pip-arm-left > ellipse', '.pip-hand'].map(selector => {
                                const hand = document.querySelector(selector).getBoundingClientRect();
                                return (hand.x + hand.width / 2 - book.x) / book.width;
                            });
                        }""")
                        assert 0 < hands[0] < .25, hands
                        assert .75 < hands[1] < 1, hands
                        # Reading has enough time for the delayed, two-line eye scan.
                        scan_end = page.locator(".pip-launcher .pip-eye-scan").evaluate("""node =>
                            node.getAnimations().find(a => a.animationName === 'pip-read')
                                .effect.getComputedTiming().endTime
                        """)
                        assert scan_end < 6800, "Pip looks up before finishing the eye scan"
                        page.clock.run_for(5_800)
                        expect(robot).to_have_attribute("data-pose", "looking-up")
                        expect(page.locator(".pip-book-open")).to_have_css("opacity", "1")
                        # Looking up does not release the book prematurely.
                        page.clock.run_for(650)
                        expect(robot).to_have_attribute("data-pose", "closing")
                        page.clock.run_for(1_000)
                        expect(robot).to_have_attribute("data-pose", "idle")
                        expect(page.locator(".pip-book-open")).to_have_css("opacity", "0")
                        # With random fixed at .5, the varied rest lasts 7.5 seconds.
                        for _ in range(29):
                            page.clock.run_for(250)
                            assert robot.get_attribute("data-pose") not in ("opening", "reading"), "Book reopened during its rest"
                        page.clock.run_for(249)
                        expect(robot).to_have_attribute("data-pose", "idle")
                        page.clock.run_for(1)
                        expect(robot).to_have_attribute("data-pose", "opening")
                    page.emulate_media(reduced_motion="reduce")
                    expect(robot).to_have_class(re.compile(r"\bis-paused\b"))
                    page.clock.run_for(20_000)
                    expect(robot).to_have_attribute("data-pose", "idle")
                    page.emulate_media(reduced_motion="no-preference")
                    expect(robot).not_to_have_class(re.compile(r"\bis-paused\b"))
                    page.clock.run_for(5_000)
                    expect(robot).to_have_attribute("data-pose", "opening")
                    page.locator(".pip-launcher").click()
                    page.clock.run_for(10_000)
                    expect(robot).to_have_attribute("data-pose", "idle")
                    expect(robot).to_have_class(re.compile(r"\bis-paused\b"))
                    print(f"PASS: {scenario}: staged reading; hands at book edges; varied rest; pause/resume")
                    page.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
