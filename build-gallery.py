#!/usr/bin/env python3
"""Build the scan gallery from data/diary.json using only the Python standard library.

By default, update ONLY the content between <!-- GALLERY:START --> and
<!-- GALLERY:END --> in index.html, if both exist. No intermediate file is
written. Use --output PATH to also save a fragment; --fragment-only requires
--output and leaves index.html untouched. Run from any working directory.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import re

SITE = Path(__file__).resolve().parent
START = "<!-- GALLERY:START -->"
END = "<!-- GALLERY:END -->"


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def build_fragment(pages: list[dict]) -> str:
    pages = sorted(pages, key=lambda page: page["id"])
    ids = [page["id"] for page in pages]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("The gallery needs a non-empty set of unique source IDs.")
    if any(not re.fullmatch(r"IMG_\d{4}", source_id) for source_id in ids):
        raise ValueError("Unexpected source ID; expected IMG_NNNN.")
    cards = []
    for number, page in enumerate(pages, 1):
        source_id = page["id"]
        title = html.escape(page["title"], quote=True)
        label = f"Photograph {number:02d}"
        cards.append(f'''      <li class="scan-gallery-card" data-scan-id="{source_id}" data-scan-title="{title}">
        <a class="scan-gallery-preview" data-scan-open href="assets/photos/{source_id}.jpg" target="_blank" rel="noopener" aria-label="Enlarge {label.lower()}: {title}">
          <img src="assets/gallery/{source_id}.jpg" alt="{label}: {title}" width="600" height="600" loading="lazy" decoding="async">
          <span class="scan-gallery-enlarge">Enlarge <span aria-hidden="true">↗</span></span>
        </a>
        <div class="scan-gallery-card-copy"><p class="scan-gallery-number">{label} · {source_id}</p><h3>{title}</h3>
          <div class="scan-gallery-card-links"><a data-scan-read href="complete-transcription.html#{source_id}">Transcription</a><a href="assets/originals/{source_id}.HEIC" download="{source_id}.HEIC">HEIC file ↓</a></div>
        </div>
      </li>''')
    return f'''<section class="scan-gallery" id="scan-gallery" aria-labelledby="scan-gallery-title">
  <div class="scan-gallery-heading"><div><h2 id="scan-gallery-title">Photographs</h2></div><p>{len(pages)} photographs, in filename order.</p></div>
  <p class="scan-gallery-note">JPEG previews. Downloadable HEIC files have location metadata removed. Photograph numbers are not original page numbers.</p>
  <ol class="scan-gallery-grid">
{chr(10).join(cards)}
  </ol>
  <noscript><p class="scan-gallery-note">Enlarge opens the full JPEG photograph in a new tab. The original-file and transcription links also work without JavaScript.</p></noscript>
  <dialog id="scan-gallery-dialog" class="scan-gallery-dialog" aria-labelledby="scan-gallery-modal-title" aria-describedby="scan-gallery-help">
    <div class="scan-gallery-modal-header"><div><p id="scan-gallery-position" class="scan-gallery-number" aria-live="polite" aria-atomic="true"></p><h2 id="scan-gallery-modal-title">Diary photograph</h2></div><button type="button" id="scan-gallery-close" aria-label="Close photograph viewer" autofocus>Close ×</button></div>
    <div class="scan-gallery-toolbar"><div class="scan-gallery-navigation"><button type="button" id="scan-gallery-previous" aria-label="Previous diary photograph">← Previous</button><button type="button" id="scan-gallery-next" aria-label="Next diary photograph">Next →</button></div><div class="scan-gallery-zoom"><label for="scan-gallery-zoom">Zoom</label><input type="range" id="scan-gallery-zoom" min="100" max="400" step="25" value="100" aria-describedby="scan-gallery-zoom-value"><output id="scan-gallery-zoom-value" for="scan-gallery-zoom">100%</output></div></div>
    <div class="scan-gallery-viewport" id="scan-gallery-viewport" tabindex="0" role="region" aria-label="Enlarged photograph; scroll to explore when zoomed"><div id="scan-gallery-canvas" class="scan-gallery-canvas"><img id="scan-gallery-image" class="scan-gallery-image" alt="" src="assets/photos/{ids[0]}.jpg"></div></div>
    <div class="scan-gallery-modal-footer"><div class="scan-gallery-modal-links"><a id="scan-gallery-transcription" href="complete-transcription.html#{ids[0]}">Transcription</a><a id="scan-gallery-full" href="assets/photos/{ids[0]}.jpg" target="_blank" rel="noopener">Open full JPEG ↗</a><a id="scan-gallery-original" href="assets/originals/{ids[0]}.HEIC" download="{ids[0]}.HEIC">Download HEIC ↓</a></div><p id="scan-gallery-help">← / → change photographs; Escape closes. Arrow keys adjust the focused zoom slider. Scroll to view enlarged detail.</p></div>
  </dialog>
</section>
'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optionally save an HTML fragment at this path.")
    parser.add_argument("--fragment-only", action="store_true", help="Do not update index.html even when gallery markers exist.")
    args = parser.parse_args()
    if args.fragment_only and args.output is None:
        parser.error("--fragment-only requires --output PATH")
    data = json.loads((SITE / "data" / "diary.json").read_text(encoding="utf-8"))
    fragment = build_fragment(data["pages"])
    if args.output is not None:
        atomic_write(args.output, fragment)
        print(f"Wrote {len(data['pages'])} gallery cards to {args.output}")
    index = SITE / "index.html"
    if args.fragment_only or not index.exists():
        return
    current = index.read_text(encoding="utf-8")
    if START not in current and END not in current:
        print("No gallery markers in index.html; the page was not changed.")
        return
    if current.count(START) != 1 or current.count(END) != 1:
        raise ValueError("Expected exactly one complete pair of gallery markers in index.html.")
    start = current.index(START) + len(START)
    end = current.index(END)
    if end < start:
        raise ValueError("Gallery markers are in the wrong order.")
    updated = current[:start] + "\n" + fragment + current[end:]
    if updated != current:
        atomic_write(index, updated)
    print("Updated only the marked gallery region in index.html.")


if __name__ == "__main__":
    main()
