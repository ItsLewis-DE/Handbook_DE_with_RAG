# Bundled webfonts

The site serves WOFF2 files from `docs/assets/fonts/` without contacting Google Fonts
at runtime. Font files retain Latin and Vietnamese shaping support,
so both precomposed (NFC) and decomposed (NFD) Vietnamese stay in the same font.
The browser downloads only the faces used on the page.

- **Manrope** retains the existing body typography (variable weights 200–800).
- **Inter** retains the UI typography (variable weights 100–900, normal and italic).
- **Lora** provides a consistent, softly curved serif for headings and editorial
  accents (variable weights 400–700, normal and italic). It replaces the previous
  system-dependent Iowan Old Style / Palatino / Georgia stack.
- **IBM Plex Mono** retains code and labels (400, 500, 600, 700; italic 400 and 700).
- **Dela Gothic One** retains the marquee typography (400).

Fonts are distributed under the SIL Open Font License. The corresponding
`*-OFL.txt` files retain each family's copyright and license notices. Font
sources come from a recorded revision of the Google Fonts repository and are
converted to WOFF2 without changing outlines or font names. Dela Gothic One is
subset to Latin, Vietnamese, combining marks, and symbols to avoid downloading
its large unused Japanese character set. Other families retain their full
character coverage. All characters for a face share one file, avoiding the
combining-mark fallback observed with separate Google Fonts unicode ranges.
`sources.json` records the source URLs and source/output SHA-256 hashes.

To refresh the assets from the project root, run:

```sh
uv run scripts/vendor_fonts.py
```

The script installs its isolated fonttools dependency, regenerates
`docs/stylesheets/fonts.css` and source metadata. Review
font and layout changes before publishing an update. It needs network access;
normal MkDocs builds and font rendering do not.

To verify fonts against a running local site:

```sh
uv run --with playwright==1.63.0 playwright install chromium
uv run scripts/check_fonts.py --url http://127.0.0.1:8000/
```

The check validates every file's checksum and Vietnamese glyph coverage, then
blocks external requests and checks Chromium's actual rendered fonts for NFC
and NFD text in every bundled face. Any system-font fallback fails the check.
