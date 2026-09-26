"""Pair article translations and retain source section anchors across languages."""
import re
from pathlib import Path

from markdown.extensions.toc import slugify, unique


def on_page_markdown(markdown, page, config, files):
    language = page.meta.get('lang', 'vi')
    page.meta['lang'] = language
    group = config.extra.get('article_translations', {}).get(page.meta.get('translation_key'))
    if not group:
        return markdown
    page.meta['reading_languages'] = [
        {'lang': lang, 'label': 'English' if lang == 'en' else 'Tiếng Việt',
         'url': files.get_file_from_path(path).url}
        for lang, path in group.items()
    ]
    # Use the Vietnamese source's existing MkDocs anchors in both editions.
    source = (Path(config.docs_dir) / group['vi']).read_text(encoding='utf-8')
    headings = re.findall(r'^#{2,6} (.+)$', source, re.M)
    translated_headings = re.findall(r'^#{2,6} (.+)$', markdown, re.M)
    if len(translated_headings) != len(headings):
        raise ValueError(f"Translation heading count differs from the Vietnamese source: {page.file.src_uri}")
    used = set()
    anchors = iter(unique(slugify(heading, '-'), used) for heading in headings)
    return re.sub(r'^(#{2,6} .+)$', lambda match: f'{match[0]} {{#{next(anchors)}}}', markdown, flags=re.M)


def on_post_page(output, page, config):
    return output.replace('<html lang="vi"', f'<html lang="{page.meta.get("lang", "vi")}"', 1)
