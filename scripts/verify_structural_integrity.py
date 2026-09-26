import re
from pathlib import Path

def check_pair(article_name, vi_path, en_path):
    print(f"\n================ Checking {article_name} ================")
    vi = Path(vi_path).read_text(encoding="utf-8")
    en = Path(en_path).read_text(encoding="utf-8")

    vi_h = re.findall(r"^(#{2,6}) (.*)$", vi, re.M)
    en_h = re.findall(r"^(#{2,6}) (.*)$", en, re.M)

    vi_h_levels = [h[0] for h in vi_h]
    en_h_levels = [h[0] for h in en_h]

    if vi_h_levels == en_h_levels:
        print(f"✓ Headings count and levels MATCH ({len(vi_h)} headings)")
    else:
        print(f"✗ Headings MISMATCH: VI={len(vi_h_levels)} vs EN={len(en_h_levels)}")
        for i in range(max(len(vi_h), len(en_h))):
            vh = vi_h[i] if i < len(vi_h) else ("NONE", "NONE")
            eh = en_h[i] if i < len(en_h) else ("NONE", "NONE")
            if vh[0] != eh[0]:
                print(f"  [{i:2d}] VI: {vh[0]} {vh[1][:40]} | EN: {eh[0]} {eh[1][:40]}")

    vi_code = re.findall(r"^```(\w*)", vi, re.M)
    en_code = re.findall(r"^```(\w*)", en, re.M)

    if vi_code == en_code:
        print(f"✓ Code blocks count and languages MATCH ({len(vi_code)} blocks)")
    else:
        print(f"✗ Code blocks MISMATCH: VI={len(vi_code)} vs EN={len(en_code)}")
        for i in range(max(len(vi_code), len(en_code))):
            vc = vi_code[i] if i < len(vi_code) else "NONE"
            ec = en_code[i] if i < len(en_code) else "NONE"
            if vc != ec:
                print(f"  [{i:2d}] VI: '{vc}' vs EN: '{ec}'")

    vi_img = re.findall(r'src="([^"]+)"', vi)
    en_img = re.findall(r'src="([^"]+)"', en)

    if vi_img == en_img:
        print(f"✓ Image paths MATCH ({len(vi_img)} images)")
    else:
        print(f"✗ Images MISMATCH: VI={vi_img} vs EN={en_img}")

if __name__ == "__main__":
    check_pair("Airflow", "docs/airflow/architecture.md", "docs/airflow/architecture.en.md")
    check_pair("PostgreSQL", "docs/postgres/postgres.md", "docs/postgres/postgres.en.md")
    check_pair("Database Index", "docs/index/index.md", "docs/index/index.en.md")
