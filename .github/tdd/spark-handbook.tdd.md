# Spark handbook — TDD evidence

## Source and user journeys

The journeys were derived during this implementation; no separate plan file was supplied.

1. As a data engineer, I can read the Spark series in a deliberate order and always know the current, previous and next chapter.
2. As an operator, I can move from each mental model to a realistic diagnosis or decision workflow with measurable evidence.
3. As a mobile reader, I can read long prose, tables and chapter navigation without content touching or overflowing the viewport.

## RED → GREEN report

| Task | RED evidence | GREEN evidence | Guarantee |
| --- | --- | --- | --- |
| Chapter structure and depth | `.venv/bin/python -m unittest tests/test_spark_handbook.py -v` reported 26 failures because heroes, applied cases and UI assets did not exist | The same target passes 6/6 tests | Ten deep-dive chapters have numbered metadata, a standalone applied case and at least 1,250 prose words |
| Stable references and links | The version-pinning test failed on two `/latest/` URLs in `overview.md` | Version and relative-link tests pass | Spark documentation links are pinned to 4.2.0 and local Markdown links resolve |
| Reading interface | Tests failed because progress/navigation selectors and `spark-handbook.js` were absent | Interface tests pass; the script is loaded by `mkdocs.yml` | The built site contains a chapter map, reading progress and previous/next navigation hooks |
| Integration | Not applicable before implementation | `.venv/bin/mkdocs build --strict --site-dir /private/tmp/architecture-handbook-spark-site` succeeds | MkDocs can render all content and assets in strict mode |
| Runtime syntax | Not applicable before implementation | `node --check docs/javascripts/spark-handbook.js` exits 0 | The progressive-enhancement script parses successfully |

## Visual verification

The locally built site was inspected at desktop and 390 × 844 mobile viewports. The pass covered:

- hero hierarchy and long Vietnamese title wrapping;
- the 5 × 2 desktop chapter grid and horizontal mobile chapter rail;
- visible current-step treatment and live reading-progress semantics;
- mobile previous/next cards, official sources and body gutters;
- tables and long-form content remaining inside the reading column.

Visual inspection caught a real specificity conflict where MkDocs forced the generated chapter list to `display: flow-root`; the selector was tightened and the rendered grid was rechecked.

## Coverage and known gaps

This repository is a static MkDocs publication and has no application coverage runner. The test suite validates all ten Spark source files, their internal links, versioned sources and required UI assets. Browser behavior was verified against the generated site; there is not yet an automated browser runner in the repository.

## Checkpoint evidence

- RED: `7c41b58 test: define Spark handbook depth and interface guarantees`
- GREEN: `dbd80dd feat: deepen Spark handbook chapters and reading experience`

If these commits are later squashed, preserve this RED/GREEN summary in the squash commit or PR body.
