from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SPARK = DOCS / "spark"

CHAPTERS = [
    "when-to-use.md",
    "architecture.md",
    "data-abstractions.md",
    "execution-model.md",
    "query-planning.md",
    "partition-shuffle.md",
    "memory-fault-tolerance.md",
    "deployment.md",
    "performance.md",
    "structured-streaming.md",
]


def body_words(markdown: str) -> list[str]:
    """Count Vietnamese/English prose words without front matter or HTML tags."""
    markdown = re.sub(r"\A---\n.*?\n---\n", "", markdown, flags=re.DOTALL)
    markdown = re.sub(r"<[^>]+>", " ", markdown)
    return re.findall(r"[\wÀ-ỹ]+", markdown, flags=re.UNICODE)


class SparkHandbookContentTests(unittest.TestCase):
    def test_all_chapters_have_numbered_editorial_hero(self) -> None:
        for index, filename in enumerate(CHAPTERS, start=1):
            with self.subTest(chapter=filename):
                text = (SPARK / filename).read_text(encoding="utf-8")
                self.assertIn('class="spark-chapter-hero"', text)
                self.assertIn(f'data-chapter="{index:02d}"', text)
                self.assertRegex(text, r'data-reading-minutes="\d+"')

    def test_all_chapters_include_a_deep_applied_case(self) -> None:
        for filename in CHAPTERS:
            with self.subTest(chapter=filename):
                text = (SPARK / filename).read_text(encoding="utf-8")
                self.assertRegex(text, r"(?m)^## \d+\. Thực chiến:")
                self.assertGreaterEqual(
                    len(body_words(text)),
                    1_250,
                    f"{filename} needs enough depth to work as a standalone chapter",
                )

    def test_spark_sources_are_version_pinned(self) -> None:
        for path in SPARK.glob("*.md"):
            with self.subTest(chapter=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("spark.apache.org/docs/latest/", text)

    def test_relative_markdown_links_resolve(self) -> None:
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+\.md(?:#[^)]+)?)\)")
        for path in SPARK.glob("*.md"):
            for target in link_pattern.findall(path.read_text(encoding="utf-8")):
                target_path = target.split("#", 1)[0]
                with self.subTest(chapter=path.name, target=target_path):
                    self.assertTrue((path.parent / target_path).resolve().is_file())


class SparkHandbookInterfaceTests(unittest.TestCase):
    def test_series_enhancement_is_loaded(self) -> None:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        script = DOCS / "javascripts" / "spark-handbook.js"
        self.assertTrue(script.is_file())
        self.assertIn("javascripts/spark-handbook.js", config)

    def test_series_styles_cover_progress_and_navigation(self) -> None:
        css = (DOCS / "stylesheets" / "article.css").read_text(encoding="utf-8")
        for selector in (
            ".spark-chapter-hero",
            ".spark-series-progress",
            ".spark-series-nav",
            ".spark-reading-progress",
        ):
            with self.subTest(selector=selector):
                self.assertIn(selector, css)


if __name__ == "__main__":
    unittest.main()
