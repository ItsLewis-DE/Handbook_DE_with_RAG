# /// script
# requires-python = ">=3.12"
# dependencies = ["fonttools[woff]==4.65.0", "playwright==1.63.0"]
# ///
"""Check bundled fonts and actual Vietnamese rendering against a running site."""

import argparse
import hashlib
import json
from pathlib import Path
import unicodedata
from urllib.parse import urlsplit

from fontTools.ttLib import TTFont
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = (
    "Tiếng Việt ĂÂĐÊÔƠƯăâđêôơư "
    "aàáảãạăằắẳẵặâầấẩẫậeèéẻẽẹêềếểễệiìíỉĩị"
    "oòóỏõọôồốổỗộơờớởỡợuùúủũụưừứửữựyỳýỷỹỵ"
)
SAMPLE += SAMPLE.upper()


def check_assets():
    directory = ROOT / "docs/assets/fonts"
    manifest = json.loads((directory / "sources.json").read_text())
    faces = []
    for family in manifest:
        for record in family["files"]:
            path = directory / record["file"]
            assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"], path
            font = TTFont(path)
            missing = set(map(ord, SAMPLE)) - font.getBestCmap().keys()
            assert not missing, (path.name, sorted(missing))
            name = font["name"].getDebugName(16) or font["name"].getDebugName(1)
            # Variable Manrope's legacy name is "Manrope ExtraLight".
            if family["family"] == "manrope":
                name = "Manrope"
            style = "italic" if font["head"].macStyle & 2 else "normal"
            weight = font["OS/2"].usWeightClass
            faces.append((name, style, weight))
    print(f"PASS: Vietnamese glyph coverage and checksums for {len(faces)} faces")
    return faces


def check_rendering(url, faces):
    origin = urlsplit(url).netloc
    external = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        def route_request(route):
            if urlsplit(route.request.url).netloc == origin:
                route.continue_()
            else:
                external.append(route.request.url)
                route.abort()

        page.route("**/*", route_request)
        response = page.goto(url)
        assert response and response.ok, url
        session = page.context.new_cdp_session(page)
        session.send("DOM.enable")
        session.send("CSS.enable")
        for family, style, weight in faces:
            for form in ("NFC", "NFD"):
                page.evaluate("""([family, style, weight, text]) => {
                    document.querySelector('#font-probe')?.remove();
                    const element = document.createElement('div');
                    element.id = 'font-probe';
                    element.style.font = `${style} ${weight} 32px "${family}"`;
                    element.textContent = text;
                    document.body.append(element);
                }""", [family, style, weight, unicodedata.normalize(form, SAMPLE)])
                page.evaluate("document.fonts.ready")
                root = session.send("DOM.getDocument")["root"]["nodeId"]
                node = session.send("DOM.querySelector", {"nodeId": root, "selector": "#font-probe"})
                fonts = session.send("CSS.getPlatformFontsForNode", node)["fonts"]
                assert fonts and all(font["isCustomFont"] for font in fonts), (family, style, form, fonts)
        assert not any("fonts.googleapis.com" in u or "fonts.gstatic.com" in u for u in external), external
        browser.close()
    print(f"PASS: {len(faces) * 2} NFC/NFD rendering checks, no system-font fallback or font CDN requests")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8000/")
    args = parser.parse_args()
    check_rendering(args.url, check_assets())
