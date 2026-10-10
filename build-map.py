#!/usr/bin/env python3
"""Build the reusable homepage journey fragment from the archive's journey data."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
journey = json.loads((ROOT / 'data/journey.json').read_text())
routes = json.loads((ROOT / 'data/map-routes.json').read_text())
payload = {'events': journey['events'], 'places': journey['places'], 'maps': journey['maps'], 'config': routes}
esc = html.escape

def source_links(event):
    return ('Reading copy · ' if event.get('readingQuote') else '') + ' · '.join(f'<a href="index.html#{esc(source)}">{esc(source)}</a>' for source in event['sources'])

first = journey['events'][0]
options = '\n'.join(f'<option value="{i}">{esc(e["dateLabel"])} — {esc(e["title"])}</option>' for i, e in enumerate(journey['events']))
entries = '\n'.join(f'''<li id="travel-{esc(e['id'])}"><span class="travel-timeline-date">{esc(e['dateLabel'])}</span> <a class="travel-timeline-entry" href="index.html#{esc(e['quoteSource'])}" data-travel-index="{i}">{esc(e['title'])}</a><span class="travel-timeline-source">{source_links(e)}</span></li>''' for i, e in enumerate(journey['events']))
serialized = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
text = f'''<section id="journey" class="travel-section" aria-labelledby="travel-heading">
  <h2 id="travel-heading">Journey</h2>
  <div class="travel-controls" hidden>
    <div class="travel-views" role="group" aria-label="Map view"><button type="button" data-travel-view="voyage" aria-pressed="true">Voyage</button><button type="button" data-travel-view="regional" aria-pressed="false">Palestine</button></div>
    <div class="travel-map-actions"><button type="button" id="travel-fit">Fit map</button><button type="button" id="travel-drag" aria-pressed="false" hidden>Move map</button></div>
  </div>
  <div class="travel-map-wrap">
    <div id="travel-map" aria-label="Map of places in Bernard's diary" hidden></div>
    <figure id="travel-fallback"><img id="travel-fallback-image" src="assets/maps/voyage.svg" width="1000" height="630" alt="Sydney, Fremantle, Trincomalee, Aden and Suez in the diary's order. Dashed connections are approximate." loading="lazy"><figcaption><a id="travel-fallback-link" href="assets/maps/voyage.svg">Open map</a> · <a href="assets/maps/regional.svg">Palestine map</a></figcaption></figure>
  </div>
  <p id="travel-map-status" class="travel-status" role="status" hidden></p>
  <p class="travel-map-note">{esc(routes['note'])} Modern map labels are shown.</p>
  <div class="travel-step-controls" hidden>
    <div class="travel-step-buttons"><button type="button" id="travel-previous" aria-label="Previous journey entry" disabled>Previous</button><span id="travel-position">1 / {len(journey['events'])}</span><button type="button" id="travel-next" aria-label="Next journey entry">Next</button></div>
    <label class="travel-select-label" for="travel-entry">Entry</label><select id="travel-entry">{options}</select>
    <label class="travel-range-label" for="travel-range">Journey position</label><input id="travel-range" type="range" min="0" max="{len(journey['events'])-1}" value="0" aria-valuetext="{esc(first['dateLabel'])}: {esc(first['title'])}">
  </div>
  <article id="travel-detail" class="travel-detail" aria-live="polite" aria-atomic="true">
    <p class="travel-date">{esc(first['dateLabel'])}</p><h3>{esc(first['title'])}</h3><blockquote>{esc(first.get('readingQuote') or first['quote'])}</blockquote><p class="travel-sources">{source_links(first)}</p>
  </article>
  <details class="travel-timeline"><summary>All entries <span>({len(journey['events'])})</span></summary><ol>{entries}</ol></details>
  <p class="travel-secondary-links"><a href="journey-record.html">Chronology and evidence</a> · <a href="JOURNEY-SOURCES.md">Map sources</a></p>
  <script type="application/json" id="travel-data">{serialized}</script>
</section>
'''
(ROOT / 'map-section.html').write_text(text)
print(f'Journey fragment: {len(journey["events"])} entries; {len(routes["routes"])} schematic routes.')
