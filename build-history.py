#!/usr/bin/env python3
"""Build the records page; expose concise cited prose for the main diary page."""
from pathlib import Path
import json
from html import escape

ROOT = Path(__file__).resolve().parent
D = json.loads((ROOT / 'data/history.json').read_text())
SUMMARY = json.loads((ROOT / 'data/history-summary.json').read_text())
SOURCES = D['sources'] + SUMMARY.get('additionalSources', [])
S = {source['id']: source for source in SOURCES}
NUM = {source['id']: i + 1 for i, source in enumerate(SOURCES)}
assert len(S) == len(SOURCES), 'Duplicate source id'


def e(value):
    return escape(str(value), quote=True)


def refs(ids, source_page=''):
    for ident in ids:
        if ident not in S:
            raise ValueError('Unknown citation: ' + ident)
    return '<span class="history-cites">' + ''.join(
        f'<a href="{e(source_page)}#source-{e(ident)}" aria-label="Source {NUM[ident]}: {e(S[ident]["title"])}">[{NUM[ident]}]</a>'
        for ident in ids) + '</span>'


def paragraph(record, cls='', source_page=''):
    attribute = f' class="{e(cls)}"' if cls else ''
    return f'<p{attribute}>{e(record["text"])} {refs(record.get("refs", []), source_page)}</p>'


def render_summary(source_page='history.html'):
    """Three paragraphs, with citations pointing to the records page by default."""
    return ''.join(paragraph(record, source_page=source_page) for record in SUMMARY['summary'])


def render_war_context(source_page='history.html'):
    return ''.join(paragraph(record, source_page=source_page) for record in SUMMARY['warContext'])


def diary_links(ids):
    return '<p class="history-entry-links">' + ' · '.join(
        f'<a href="index.html#{e(ident)}">Photograph {e(ident)}</a>' for ident in ids) + '</p>'


def render_bibliography():
    entries = []
    for source in SOURCES:
        identifiers = ' · '.join(e(ident) for ident in source['recordIds'])
        extra = (f'<p class="history-source-extra"><a href="{e(source["documentUrl"])}">Digitised document page</a></p>'
                 if source.get('documentUrl') else '')
        if source['id'].startswith('diary-'):
            extra = '<p class="history-source-extra">' + ' · '.join(
                f'<a href="assets/photos/{e(ident)}.jpg">Photograph {e(ident)}</a>'
                for ident in source['recordIds']) + '</p>'
        note = SUMMARY['sourceNotes'].get(source['id'], '')
        entries.append(f'''<li id="source-{e(source['id'])}"><span class="history-source-number" aria-hidden="true">{NUM[source['id']]}</span><div><h3><a href="{e(source['url'])}">{e(source['title'])}</a></h3><p class="history-source-meta">{e(source['institution'])}. {identifiers + '. ' if identifiers else ''}Accessed 10 October 2026.</p><p>{e(note)}</p>{extra}</div></li>''')
    return '<ol class="history-source-list">' + ''.join(entries) + '</ol>'


def build():
    overview = render_summary(source_page='')
    timeline_text = {
        0: 'The 5th Light Horse roll records Bernard Edward Shambrook joining on this date, aged 19, a butcher from Pimlico, Townsville. His mother Elizabeth was his next of kin.',
        1: 'The WWII nominal roll records enlistment at Tamworth, NSW, from Wee Waa.',
        2: 'The notebook records leaving Sydney aboard Queen Elizabeth, then travelling through Fremantle and Trincomalee to Suez.',
        3: 'The notebook records marching into “1st Aust Corps Guard Btn” from “16 ITB Special wing”. June 12 appears beside a battalion-order reference; the precise transfer date remains uncertain.',
        4: 'The Tent 17 roster gives A/Sgt Shambrook B.E.; the ownership inscription says Sgt.',
        5: 'DVA records discharge as a private, with HQ Guard Battalion as his final posting.'
    }
    timeline = ''.join(
        f'<li><div class="history-date">{e(row["date"])}</div><div><h3>{e(row["title"])}</h3>'
        + paragraph({'text': timeline_text[i], 'refs': row['refs']}) + '</div></li>'
        for i, row in enumerate(D['timeline']))
    contexts = ''.join(
        f'<article><h3>{e(context["title"])}</h3>{paragraph(context)}{diary_links(context["diary"])}</article>'
        for context in SUMMARY['context'])
    archives = ''.join(
        f'<article><h3>{e(record["title"])}</h3><p class="history-query">{e(record["query"])}</p>'
        f'<p>{e(record["series"])} {refs(record["refs"])}</p>'
        f'<a class="history-text-link" href="{e(record["url"])}">Search the National Archives</a></article>'
        for record in D['archives']['records'])
    html = f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Service records and references for Bernard Edward Shambrook: 2076 in the First World War and NX40242 in the Second World War.">
<meta name="theme-color" content="#ffffff"><title>Records — Bernard Shambrook</title>
<link rel="stylesheet" href="style.css"><link rel="stylesheet" href="enhancements.css"><link rel="stylesheet" href="history.css"><link rel="stylesheet" href="monochrome.css">
<script src="preferences.js" defer></script>
</head>
<body class="history-page">
<a class="skip-link" href="#history-main">Skip to records</a>
<header class="masthead"><a class="wordmark" href="index.html">Bernard Shambrook</a><nav aria-label="Main"><a href="index.html">Diary</a><a href="reading.html">Reading</a><a href="index.html#scan-gallery">Photographs</a><a href="journey.html">Journey</a><a href="people.html">Names</a><a href="history.html" aria-current="page">Records</a></nav></header>
<main id="history-main" class="history-main">
<section class="history-hero"><div><h1>Records</h1><div class="history-overview">{overview}</div></div><figure class="history-portrait"><a href="assets/portrait/bernard-shambrook-full.jpg"><img src="assets/portrait/bernard-shambrook.jpg" width="840" height="1120" alt="Bernard Shambrook standing in uniform"></a><figcaption>Portrait supplied by Craig. Date unknown. {refs(['family-portrait'])}</figcaption></figure></section>
<nav class="history-contents" aria-label="On this page"><a href="#identity">Identity</a><a href="#service-timeline">Service</a><a href="#open-questions">Birth details</a><a href="#wartime-context">Context</a><a href="#service-files">Service files</a><a href="#sources">Sources</a></nav>
<section class="history-section" id="identity"><h2>In the notebook</h2><blockquote>{e(D['identity']['quote'])}</blockquote><p>Tent 17 roster · IMG_0926 {refs(['diary-roster'])}</p><p>A/Sgt means acting sergeant. The DVA rank field records substantive rank at discharge, excluding acting and temporary appointments. {refs(['dva'])}</p>{diary_links(['IMG_0926'])}</section>
<section class="history-section" id="service-timeline"><h2>Service</h2><ol class="history-timeline">{timeline}</ol></section>
<section class="history-section" id="open-questions"><h2>Birth details</h2>{paragraph(SUMMARY['birth'])}</section>
<section class="history-section" id="wartime-context"><h2>Wartime context</h2>{render_war_context(source_page='')}<div class="history-context-grid">{contexts}</div></section>
<section class="history-section" id="service-files"><h2>Service files</h2><p>The complete personnel files would help resolve the birth details and his rank history. Neither individual dossier has yet been retrieved.</p><div class="history-archive-grid">{archives}</div></section>
<section class="history-section history-bibliography" id="sources"><h2>Sources</h2><p class="history-data-link"><a href="data/history.json" download>Research notes (JSON)</a> · <a href="data/history-summary.json" download>Reading summary and additional sources (JSON)</a> · <a href="references.html">Other sources</a></p>{render_bibliography()}</section>
</main>
<footer><p>Bernard Shambrook’s diary</p><p>Research checked 10 October 2026.</p><a href="index.html">Diary</a></footer>
</body>
</html>
'''
    (ROOT / 'history.html').write_text(html)
    print(f'Built history.html: {len(SOURCES)} sources, {len(D["timeline"])} timeline entries')


if __name__ == '__main__':
    build()
