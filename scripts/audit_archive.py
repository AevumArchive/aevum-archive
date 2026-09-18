#!/usr/bin/env python3
"""Audit the static Aevum Archive without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SITE_PREFIX = "/aevum-archive/"
TEXT_SUFFIXES = {".html", ".css", ".js", ".json"}
SKIP_PREFIXES = ("http:", "https:", "mailto:", "tel:", "data:", "javascript:", "//", "#")
INTENTIONAL_ENTRY_POINTS = {
    "codex/magic.html",  # Legacy redirect retained for old bookmarks.
    "lore/locations/the-bridge.html",  # Legacy redirect after the dimension reorganization.
    "npcs/willy.html",  # Hidden encounter opened by willy-watcher.js rather than navigation.
    "top-characters/index.html",  # Legacy leaderboard redirect.
}


def repository_files() -> set[str]:
    return {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts
    }


FILES = repository_files()
HTML_FILES = sorted(path for path in FILES if path.endswith(".html"))


def resolve_reference(source: str, raw_reference: str) -> str | None:
    reference = unquote(raw_reference.strip())
    if not reference or reference.lower().startswith(SKIP_PREFIXES):
        return None

    path = urlsplit(reference).path
    if not path:
        return None
    if path in {"/aevum-archive", SITE_PREFIX}:
        return "index.html"
    if path.startswith(SITE_PREFIX):
        relative = path[len(SITE_PREFIX) :]
    elif path.startswith("/"):
        return None
    else:
        relative = (PurePosixPath(source).parent / path).as_posix()

    parts: list[str] = []
    for part in PurePosixPath(relative).parts:
        if part in {"", "."}:
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    normalized = "/".join(parts)
    if path.endswith("/") or not normalized:
        normalized = f"{normalized}/index.html".lstrip("/")
    return normalized


class ArchiveHTMLParser(HTMLParser):
    def __init__(self, source: str) -> None:
        super().__init__(convert_charrefs=True)
        self.source = source
        self.ids: list[str] = []
        self.links: set[str] = set()
        self.issues: list[str] = []
        self.title_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.append(attributes["id"] or "")
        if tag == "title":
            self.title_count += 1
        if tag == "img" and "alt" not in attributes:
            self.issues.append(f"{self.source}: image is missing alt text ({attributes.get('src', '')})")

        attribute_name = "href" if tag in {"a", "link"} else "src" if tag in {"img", "script", "source"} else None
        if attribute_name and attributes.get(attribute_name):
            target = resolve_reference(self.source, attributes[attribute_name] or "")
            if target:
                self.links.add(target)


def audit_html() -> tuple[list[str], dict[str, set[str]]]:
    issues: list[str] = []
    graph: dict[str, set[str]] = {path: set() for path in HTML_FILES}
    for relative in HTML_FILES:
        parser = ArchiveHTMLParser(relative)
        parser.feed((ROOT / relative).read_text(encoding="utf-8"))
        issues.extend(parser.issues)
        duplicates = sorted(name for name, count in Counter(parser.ids).items() if count > 1)
        if duplicates:
            issues.append(f"{relative}: duplicate ids: {', '.join(duplicates)}")
        if parser.title_count != 1:
            issues.append(f"{relative}: expected one title element, found {parser.title_count}")
        for target in parser.links:
            if target not in FILES:
                issues.append(f"{relative}: missing target {target}")
            elif target.endswith(".html"):
                graph[relative].add(target)
    return issues, graph


def audit_css() -> list[str]:
    issues: list[str] = []
    url_pattern = re.compile(r"url\(\s*['\"]?([^)'\"]+)", re.IGNORECASE)
    import_pattern = re.compile(r"@import\s+['\"]([^'\"]+)", re.IGNORECASE)
    for relative in sorted(path for path in FILES if path.endswith(".css")):
        text = (ROOT / relative).read_text(encoding="utf-8")
        references = [*url_pattern.findall(text), *import_pattern.findall(text)]
        for reference in references:
            target = resolve_reference(relative, reference)
            if target and target not in FILES:
                issues.append(f"{relative}: missing target {target}")
    return issues


def audit_json() -> list[str]:
    issues: list[str] = []
    for relative in sorted(path for path in FILES if path.endswith(".json")):
        try:
            json.loads((ROOT / relative).read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            issues.append(f"{relative}: invalid JSON ({error})")
    return issues


def audit_absolute_runtime_paths() -> list[str]:
    issues: list[str] = []
    absolute_pattern = re.compile(r"/aevum-archive/[A-Za-z0-9_./-]+")
    for relative in sorted(path for path in FILES if Path(path).suffix in TEXT_SUFFIXES):
        text = (ROOT / relative).read_text(encoding="utf-8")
        for reference in absolute_pattern.findall(text):
            raw_path = urlsplit(reference).path
            if raw_path.startswith(SITE_PREFIX):
                directory = ROOT / raw_path[len(SITE_PREFIX) :]
                if raw_path.endswith("/") and directory.is_dir():
                    continue
            target = resolve_reference(relative, reference)
            if not target:
                continue
            candidates = {target}
            if not Path(target).suffix:
                candidates.add(f"{target.rstrip('/')}/index.html")
            if not any(candidate in FILES for candidate in candidates):
                issues.append(f"{relative}: unresolved runtime path {reference}")
    return issues


def reachable_pages(graph: dict[str, set[str]]) -> set[str]:
    seen = {"index.html"}
    pending = ["index.html"]
    while pending:
        source = pending.pop()
        for target in graph.get(source, set()):
            if target not in seen:
                seen.add(target)
                pending.append(target)
    return seen


def main() -> int:
    html_issues, graph = audit_html()
    issues = sorted(set([*html_issues, *audit_css(), *audit_json(), *audit_absolute_runtime_paths()]))
    reachable = reachable_pages(graph)
    orphans = sorted(set(HTML_FILES) - reachable - {"404.html"} - INTENTIONAL_ENTRY_POINTS)

    print(f"HTML pages: {len(HTML_FILES)}")
    print(f"Reachable from index: {len(reachable)}")
    print(f"Broken or malformed references: {len(issues)}")
    print(f"Unlinked pages: {len(orphans)}")
    if issues:
        print("\nErrors:")
        for issue in issues:
            print(f"- {issue}")
    if orphans:
        print("\nUnlinked pages:")
        for orphan in orphans:
            print(f"- {orphan}")
    return 1 if issues or orphans else 0


if __name__ == "__main__":
    sys.exit(main())
