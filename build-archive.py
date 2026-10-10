"""Build the scrolling archive from the editable text and existing page builders."""
from pathlib import Path
from collections import OrderedDict
import html
import json
import re
import runpy

ROOT=Path(__file__).resolve().parent
E=html.escape

def load(name): return json.loads((ROOT/'data'/name).read_text())

def related_section(id,title,intro,items):
    out=[f'<section class="archive-section" id="{id}"><h2>{title}</h2><p class="section-note">{intro}</p><div class="archive-finding-grid">']
    for pid,label,desc in items:
        out.append(f'<article><a href="#{pid}"><img src="assets/gallery/{pid}.jpg" width="800" height="600" loading="lazy" alt="{E(label)}"><h3>{E(label)}</h3></a><p>{E(desc)}</p></article>')
    return '\n'.join(out+['</div></section>'])

def people():
    groups=load('people-index.json')['groups']
    out=['<section class="archive-section" id="people"><h2>People</h2><p class="section-note">Names and source lines from the notebook. A surname may refer to more than one person.</p><div class="edition-controls" id="people-controls" hidden><label for="people-search">Find a name or number</label><input id="people-search" type="search" placeholder="Shambrook, 40242, Fred…"><p class="edition-result" id="people-result" role="status" aria-live="polite"></p></div><p id="people-empty" hidden>No matching names.</p>']
    letters=sorted({g['name'][0].upper() for g in groups})
    out.append('<nav class="name-alphabet" aria-label="Names by initial">'+''.join(f'<a href="#letter-{l}">{l}</a>' for l in letters)+'</nav>')
    for letter in letters:
        out.append(f'<section class="name-letter" id="letter-{letter}"><h3>{letter}</h3><div class="archive-name-grid">')
        for group in [g for g in groups if g['name'][0].upper()==letter]:
            out.append(f'<details class="name-card" id="name-{group["id"]}"><summary>{E(group["name"])}<span>{len(group["occurrences"])}</span></summary><ul class="name-occurrences">')
            for hit in group['occurrences']:
                out.append(f'<li><p class="name-quote">{E(hit["quote"])}</p><a class="name-source" href="#{hit["pageId"]}-s{hit["sectionIndex"]}">{E(hit["pageId"])} · {E(hit["section"])}</a></li>')
            out.append('</ul></details>')
        out.append('</div></section>')
    out.append('<p class="section-note"><a href="people.html">Full names index</a></p></section>')
    return '\n'.join(out)

def main():
    pages=load('diary.json')['pages']
    reading=(ROOT/'reading.html').read_text()
    reading=reading[reading.index('<div class="edition-controls"'):reading.index('</main>')]
    reading=reading.replace('<h3>','<h4>').replace('</h3>','</h4>').replace('<h2>','<h3>').replace('</h2>','</h3>')
    reading=reading.replace('href="reading.html#','href="#')
    gallery=runpy.run_path(str(ROOT/'build-gallery.py'))['build_fragment'](pages)
    gallery=gallery.replace('href="complete-transcription.html#','href="#')
    history=runpy.run_path(str(ROOT/'build-history.py'))
    summary=history['render_summary'](source_page='history.html') if 'render_summary' in history else '<p><a href="history.html">Bernard’s service records and sources</a></p>'
    biography='<p class="service-biography">'+' '.join(E(record['text'])+' '+history['refs'](record['refs'], source_page='history.html') for record in history['SUMMARY']['overviewBiography'])+'</p>'
    map_fragment=(ROOT/'map-section.html').read_text() if (ROOT/'map-section.html').exists() else '<section class="archive-section" id="journey"><h2>Journey</h2><a href="journey.html">Map and chronology</a></section>'
    out=['''<!doctype html>
<html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Bernard Shambrook’s diary, 1941. Photographs, transcription, journey and service records."><meta name="color-scheme" content="light dark"><meta name="theme-color" content="#ffffff"><title>Bernard Shambrook’s diary</title>
<link rel="stylesheet" href="style.css"><link rel="stylesheet" href="portrait.css"><link rel="stylesheet" href="gallery.css"><link rel="stylesheet" href="edition.css"><link rel="stylesheet" href="enhancements.css"><link rel="stylesheet" href="monochrome.css"><link rel="stylesheet" href="assets/vendor/leaflet/leaflet.css"><link rel="stylesheet" href="map.css"><link rel="stylesheet" href="archive.css">
<script src="preferences.js"></script><script src="edition.js" defer></script><script src="gallery.js" defer></script><script src="archive.js" defer></script><script src="journey-data.js" defer></script><script src="assets/vendor/leaflet/leaflet.js" defer></script><script src="map.js" defer></script></head>
<body class="archive-home"><a class="skip-link" href="#diary">Skip to diary</a><header class="masthead"><a href="index.html" class="wordmark">Bernard Shambrook</a><nav aria-label="Main navigation"><a href="#journey">Journey</a><a href="#diary">Diary</a><a href="#lists">Lists &amp; rolls</a><a href="#cemeteries">Cemeteries</a><a href="#people">People</a><a href="#scan-gallery">Photographs</a><a href="#background">Records</a></nav></header>
<main id="main" class="archive-main">
<section class="archive-intro" aria-labelledby="site-title"><div><h1 id="site-title">Diary, 1941</h1><p>Bernard Edward Shambrook<br>NX40242</p><div class="diary-overview">''',biography,'''<p>Bernard kept this notebook during his Australian Army service in the Second World War. It follows his April 1941 voyage aboard <em>Queen Elizabeth</em>, from Sydney through Fremantle and Trincomalee to Suez, then his journey into Palestine. He records life on the ship, the canal and railway journeys, and later movements between camps.</p><p>Alongside the diary entries are tent and duty rolls, soldiers’ names and addresses, weapon and routine notes, Arabic words, currency calculations, and sketches of Suez and the cemeteries at Gaza and Jerusalem. He also copied names and inscriptions commemorating soldiers of the First World War.</p><p class="overview-dates">The dated travel and service entries run from April to August 1941. One Gaza heading may read June or September. The 1917–18 dates in the cemetery lists refer to the men remembered there.</p></div><div class="intro-actions"><a href="#diary">Read the diary</a><a href="#journey">View the journey</a></div></div><figure class="portrait-figure" id="bernard-portrait"><a href="assets/portrait/bernard-shambrook-full.jpg" aria-label="View full portrait of Bernard Shambrook"><img src="assets/portrait/bernard-shambrook.jpg" alt="Bernard Shambrook in military uniform and a feathered slouch hat" width="840" height="1120" fetchpriority="high"></a><figcaption>Family photograph. Date unknown.<span class="portrait-links"><a href="assets/originals/IMG_0569.heic" download>HEIC file</a></span></figcaption></figure></section>''',map_fragment,
    '''<section class="archive-section" id="diary"><h2>Diary pages</h2><p class="section-note">The reading copy, in notebook order. <a href="#about">About the transcription</a>.</p><div class="edition-links"><a href="faithful-transcription.txt" download>Faithful text ↓</a><a href="reading-copy.txt" download>Reading copy ↓</a><a href="complete-transcription.html">Complete transcription</a><a href="reader.html">Inspect a photograph</a><button type="button" id="photo-contrast" aria-pressed="false">Increase photograph contrast</button></div>''',reading,'</section>',
    related_section('lists','Lists and rolls','Selected pages from the notebook above.',[
        ('IMG_0905','Personnel lists','Names, service numbers and weapon notes.'),
        ('IMG_0926','Tent 17','Bernard’s name, service number and acting rank, alongside the other men in his tent.'),
        ('IMG_0928','Notes and addresses','A route list, practical notes and Fred Green’s address.')]),
    related_section('cemeteries','Cemetery pages','Names, inscriptions and drawings from the notebook.',[
        ('IMG_0915','Gaza','Names and dates from 1917–18. The heading’s 1941 month remains uncertain.'),
        ('IMG_0916','Gaza memorial','Bernard’s sketch and the memorial inscription.'),
        ('IMG_0917','Jerusalem War Cemetery','The gateway, path and grave markers.')]),people(),
    '<!-- GALLERY:START -->',gallery,'<!-- GALLERY:END -->',
    '<section class="archive-section archive-background" id="background"><h2>Background and records</h2>'+summary+'<p class="edition-links"><a href="history.html">Records and numbered sources</a><a href="references.html">Transcription and map sources</a></p></section>',
    '''<section class="archive-section archive-about" id="about"><h2>About</h2><p>From photographs supplied by Craig, Bernard’s great-grandson. All 28 diary photographs appear in the supplied order; filename gaps were deliberate. A photograph may show two pages.</p><p>The reading copy uses modern spelling and punctuation, with standard names where the photographs, parallel entries or records support them. The faithful transcription preserves the wording as closely as it can be read. <mark>[word?]</mark> marks an uncertain reading; <mark>[illegible]</mark> marks unreadable writing. Readings are open to correction.</p><p>The journey distinguishes recorded movements from addresses, drawings and memorial dates. Lines connect named places approximately; dates on cemetery pages are not arrival dates. Records provide context, with unresolved identifications noted.</p><p>Page crops and contrast controls help with reading. Full photographs and HEIC downloads are available throughout. Location metadata has been removed from the public HEIC copies; the supplied originals are retained privately.</p><div class="edition-links"><a href="corrections.html">Revisions</a><a href="corrections.html#reading-revisions">Reading-copy changes</a><a href="uncertain-readings.tsv" download>Uncertain readings ↓</a><a href="SOURCE-NOTES.md">Source notes</a></div></section></main><footer class="edition-footer"><p>Bernard Shambrook</p><p><a href="#site-title">Back to top</a> · <a href="history.html#sources">Sources</a> · <a href="complete-transcription.html">Complete transcription</a></p></footer></body></html>''']
    (ROOT/'index.html').write_text('\n'.join(out)+'\n')
    # The dedicated journey uses the same component as the archive.
    source=(ROOT/'index.html').read_text()
    head=source[:source.index('<main id="main"')]
    head=head.replace('<title>Bernard Shambrook’s diary</title>','<title>Journey — Bernard Shambrook’s diary</title>')
    head=re.sub(r'href="#([^"]+)"',r'href="index.html#\1"',head)
    journey=head+'<main class="archive-main">'+map_fragment.replace('<h2 id="travel-heading">Journey</h2>','<h1 id="travel-heading">Journey</h1>')+'<p class="edition-links"><a href="journey-record.html">Chronology and source passages</a><a href="journey-chronology.tsv" download>Download chronology</a><a href="JOURNEY-SOURCES.md">Geographic sources</a></p></main><footer class="edition-footer"><a href="index.html">Bernard Shambrook’s diary</a></footer></body></html>'
    (ROOT/'journey.html').write_text(journey+'\n')
    print('Generated scrolling archive: journey, 28 diary photographs, lists, cemeteries, people, gallery and records.')

if __name__=='__main__': main()
