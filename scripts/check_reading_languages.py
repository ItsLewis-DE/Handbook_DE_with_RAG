# /// script
# requires-python = ">=3.12"
# dependencies = ["playwright==1.63.0"]
# ///
"""Check translation structure and reading-language navigation on the built site."""
import re
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def main():
    for pair in [('airflow/architecture', 'airflow/architecture.en'),
                 ('postgres/postgres', 'postgres/postgres.en'),
                 ('postgres/p2', 'postgres/p2.en'),
                 ('index/index', 'index/index.en'),
                 ('ware_lake_lw/doc', 'ware_lake_lw/doc.en'),
                 ('spark/archi', 'spark/archi.en'),
                 ('spark/p2', 'spark/p2.en')]:
        vi, en = [(ROOT / f'docs/{name}.md').read_text() for name in pair]
        assert re.findall(r'^(#{2,6}) ', vi, re.M) == re.findall(r'^(#{2,6}) ', en, re.M)
        assert re.findall(r'^```(\w*)', vi, re.M) == re.findall(r'^```(\w*)', en, re.M)
        image_pattern = r'(?:src="|!\[[^\]]*\]\()([^"\)]+)'
        assert re.findall(image_pattern, vi) == re.findall(image_pattern, en), pair

    handler = partial(QuietHandler, directory=ROOT)
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}/site'
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(args=['--no-sandbox'])
            for viewport in ({'width': 1440, 'height': 900}, {'width': 390, 'height': 844}):
                page = browser.new_page(viewport=viewport)

                # Airflow switching and anchor preservation
                page.goto(f'{base}/airflow/architecture/#executor', wait_until='domcontentloaded')
                page.locator('[data-reading-language="en"]').click()
                page.wait_for_url('**/architecture.en/#executor')
                assert page.locator('html').get_attribute('lang') == 'en'
                assert page.locator('[data-reading-language="en"]').get_attribute('aria-current') == 'page'
                assert page.locator('#executor').count() == 1
                assert page.locator('[data-reading-language]').count() == 2
                page.evaluate("location.hash = '#critical-section'")
                page.locator('[data-reading-language="vi"]').click()
                page.wait_for_url('**/architecture/#critical-section')
                assert page.locator('html').get_attribute('lang') == 'vi'

                # PostgreSQL Part 2 keeps the layer anchor in both editions.
                page.goto(f'{base}/postgres/p2/#tang-3-bo-nho-em-va-giao-dich', wait_until='domcontentloaded')
                page.locator('[data-reading-language="en"]').click()
                page.wait_for_url('**/p2.en/#tang-3-bo-nho-em-va-giao-dich')
                assert page.locator('html').get_attribute('lang') == 'en'
                assert page.locator('#tang-3-bo-nho-em-va-giao-dich').count() == 1
                page.locator('[data-reading-language="vi"]').click()
                page.wait_for_url('**/p2/#tang-3-bo-nho-em-va-giao-dich')

                # PostgreSQL switching and anchor preservation
                page.goto(f'{base}/postgres/postgres/#1-phan-cap-logic-trong-postgresql', wait_until='domcontentloaded')
                page.locator('[data-reading-language="en"]').click()
                page.wait_for_url('**/postgres.en/#1-phan-cap-logic-trong-postgresql')
                assert page.locator('html').get_attribute('lang') == 'en'
                assert page.locator('[data-reading-language="en"]').get_attribute('aria-current') == 'page'
                assert page.locator('[id="1-phan-cap-logic-trong-postgresql"]').count() == 1
                assert page.locator('[data-reading-language]').count() == 2
                page.locator('[data-reading-language="vi"]').click()
                page.wait_for_url('**/postgres/#1-phan-cap-logic-trong-postgresql')
                assert page.locator('html').get_attribute('lang') == 'vi'

                # Index switching and anchor preservation
                page.goto(f'{base}/index/#1-database-luu-tru-du-lieu-nhu-the-nao', wait_until='domcontentloaded')
                page.locator('[data-reading-language="en"]').click()
                page.wait_for_url('**/index.en/#1-database-luu-tru-du-lieu-nhu-the-nao')
                assert page.locator('html').get_attribute('lang') == 'en'
                assert page.locator('[data-reading-language="en"]').get_attribute('aria-current') == 'page'
                assert page.locator('[id="1-database-luu-tru-du-lieu-nhu-the-nao"]').count() == 1
                assert page.locator('[data-reading-language]').count() == 2
                page.locator('[data-reading-language="vi"]').click()
                page.wait_for_url('**/index/#1-database-luu-tru-du-lieu-nhu-the-nao')
                assert page.locator('html').get_attribute('lang') == 'vi'

                # Fallback on untranslated article
                page.goto(f'{base}/assets/images/pip/ANIMATION/', wait_until='domcontentloaded')
                assert 'Chưa có bản tiếng Anh' in page.locator('.reading-language').inner_text()
                page.close()

            context = browser.new_context(java_script_enabled=False)
            page = context.new_page()
            page.goto(f'{base}/airflow/architecture/', wait_until='domcontentloaded')
            page.locator('[data-reading-language="en"]').click()
            page.wait_for_url('**/architecture.en/')
            assert page.locator('html').get_attribute('lang') == 'en'

            page.goto(f'{base}/postgres/postgres/', wait_until='domcontentloaded')
            page.locator('[data-reading-language="en"]').click()
            page.wait_for_url('**/postgres.en/')
            assert page.locator('html').get_attribute('lang') == 'en'

            page.goto(f'{base}/index/', wait_until='domcontentloaded')
            page.locator('[data-reading-language="en"]').click()
            page.wait_for_url('**/index.en/')
            assert page.locator('html').get_attribute('lang') == 'en'
            browser.close()
    finally:
        server.shutdown()
    print('PASS: translation structure, desktop/mobile switching, section anchors, fallback, and no-JS navigation.')


if __name__ == '__main__':
    main()
