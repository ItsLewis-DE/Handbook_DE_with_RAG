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

                    # The first read starts exactly five seconds after mounting/resuming.
                    if scenario == "moving pointer":
                        page.clock.run_for(3_000)
                        box = page.locator(".pip-mascot-wrapper").bounding_box()
                        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + 30)
                        page.clock.run_for(1_000)
                        page.mouse.move(0, 0)
                        page.clock.run_for(999)
                    else:
                        page.clock.run_for(4_999)
                    assert robot.get_attribute("data-pose") != "reading"
                    page.clock.run_for(1)
                    expect(robot).to_have_attribute("data-pose", "reading")
                    for _ in range(3):
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
                        page.clock.run_for(2_500)
                        expect(robot).to_have_attribute("data-pose", "idle")
                        # Allow the book to finish closing, then require a full 5s rest.
                        page.clock.run_for(650)
                        expect(page.locator(".pip-book-open")).to_have_css("opacity", "0")
                        for _ in range(19):
                            page.clock.run_for(250)
                            assert robot.get_attribute("data-pose") != "reading", "Book reopened before a full 5s rest"
                        page.clock.run_for(249)
                        expect(robot).to_have_attribute("data-pose", "idle")
                        page.clock.run_for(1)
                        expect(robot).to_have_attribute("data-pose", "reading")
                    page.emulate_media(reduced_motion="reduce")
                    expect(robot).to_have_class(re.compile(r"\bis-paused\b"))
                    page.clock.run_for(20_000)
                    expect(robot).to_have_attribute("data-pose", "idle")
                    page.emulate_media(reduced_motion="no-preference")
                    expect(robot).not_to_have_class(re.compile(r"\bis-paused\b"))
                    page.clock.run_for(5_000)
                    expect(robot).to_have_attribute("data-pose", "reading")
                    page.locator(".pip-launcher").click()
                    page.clock.run_for(10_000)
                    expect(robot).to_have_attribute("data-pose", "idle")
                    expect(robot).to_have_class(re.compile(r"\bis-paused\b"))
                    print(f"PASS: {scenario}: waits 5s after book closes; hands at book edges; pause/resume works")
                    page.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
