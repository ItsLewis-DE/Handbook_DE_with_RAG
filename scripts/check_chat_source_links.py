# /// script
# requires-python = ">=3.12"
# dependencies = ["playwright==1.63.0"]
# ///
"""Verify that chat citation links open the expected documentation section."""

import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright


REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = REPO_ROOT / "site"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def main():
    handler = partial(QuietHandler, directory=SITE_DIR)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    Thread(target=server.serve_forever, daemon=True).start()
    origin = f"http://127.0.0.1:{server.server_port}"
    expected_url = f"{origin}/airflow/architecture/#executor"

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.route(
                "http://127.0.0.1:8001/chat",
                lambda route: route.fulfill(
                    status=200,
                    content_type="application/json",
                    body=json.dumps({
                        "answer": "Executor chạy trong Scheduler. [S1]",
                        "sources": [{
                            "id": "S1",
                            "title": "Kiến trúc Apache Airflow",
                            "heading": "Các component trong Airflow > Executor",
                            "url": "airflow/architecture/#executor",
                            "chunk_id": "regression-test",
                        }],
                        "status": "answered",
                    }),
                ),
            )

            page.goto(f"{origin}/airflow/architecture/")
            page.locator(".pip-launcher").click()
            page.locator(".pip-composer textarea").fill("Executor là gì?")
            page.locator(".pip-composer textarea").press("Enter")
            source_link = page.locator(".pip-source__link")
            source_link.wait_for()
            resolved_url = source_link.evaluate("node => node.href")
            source_link.click()
            page.wait_for_load_state("domcontentloaded")
            assert page.url == expected_url, (
                f"Citation resolved to {resolved_url} and opened {page.url}; "
                f"expected {expected_url}"
            )
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    print(f"Chat citation opened the expected section: {expected_url}")


if __name__ == "__main__":
    main()
