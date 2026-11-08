"""Checks for the static design mockups published at /mockups/ on GitHub Pages.

The mockups are served under a path prefix, so every link between them must be
relative and must resolve to a file that is shipped alongside them.
"""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

import pytest

ROOT = Path(__file__).resolve().parents[1]
MOCKUPS = ROOT / "docs" / "mockups"
PAGES = sorted(MOCKUPS.glob("*.html"))
EXPECTED_PAGES = {"index.html", "01-library.html", "02-notebook.html", "03-search.html"}


class _RefCollector(HTMLParser):
    """Collects href/src references and robots meta content from one page."""

    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []
        self.robots: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "meta" and values.get("name") == "robots":
            self.robots = values.get("content")
        for name in ("href", "src"):
            value = values.get(name)
            if value:
                self.refs.append(value)


def _parse(page: Path) -> _RefCollector:
    collector = _RefCollector()
    collector.feed(page.read_text(encoding="utf-8"))
    return collector


def _is_local(ref: str) -> bool:
    parts = urlsplit(ref)
    return not parts.scheme and not parts.netloc and not ref.startswith("#")


def test_all_screens_exist() -> None:
    assert EXPECTED_PAGES <= {page.name for page in PAGES}


@pytest.mark.parametrize("page", PAGES, ids=lambda page: page.name)
def test_local_references_resolve(page: Path) -> None:
    missing = []
    for ref in _parse(page).refs:
        if not _is_local(ref):
            continue
        assert not ref.startswith("/"), f"{page.name}: {ref} must be relative to work under /mockups/"
        target = urlsplit(ref).path
        if target and not (MOCKUPS / target).is_file():
            missing.append(ref)
    assert not missing, f"{page.name} links to missing files: {missing}"


@pytest.mark.parametrize("page", PAGES, ids=lambda page: page.name)
def test_pages_are_not_indexed(page: Path) -> None:
    robots = _parse(page).robots or ""
    assert "noindex" in robots, f"{page.name} needs <meta name='robots' content='noindex'>"
