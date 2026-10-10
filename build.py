"""Regenerate the diary's readable files after editing data/diary.json.

Run: python3 build.py
Uses only the Python standard library. Does not touch photographs.
"""
from pathlib import Path
import csv
import html
import json
import re

ROOT = Path(__file__).resolve().parent


def marked(text):
    parts = re.split(r'(\[[^\]\n]+\])', text)
    result = []
    for part in parts:
        safe = html.escape(part)
        if part.startswith('['):
            tag = 'mark' if re.search(r'\?|illegible|unclear|obscured', part, re.I) else 'span'
            result.append(f'<{tag} class="editorial-marker">{safe}</{tag}>')
        else:
            result.append(safe)
    return ''.join(result)


def main():
    data = json.loads((ROOT / 'data/diary.json').read_text(encoding='utf-8'))
    pages = data['pages']
    assert len(pages) == 28, 'Expected all 28 supplied photographs'
    assert len({page['id'] for page in pages}) == 28, 'Duplicate photograph IDs'
    for page in pages:
        assert (ROOT / f"assets/photos/{page['id']}.jpg").exists()
        assert (ROOT / f"assets/thumbs/{page['id']}.jpg").exists()
        for section in page['sections']:
            assert section['faithful'].strip() and section['reading'].strip(), page['id']
    (ROOT / 'diary-data.js').write_text('window.DIARY_DATA = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')
    convention = ('Square brackets are editorial: [word?] is tentative; [illegible] marks unreadable writing. '
                  'Titles and section labels are editorial. Photograph numbers are not original page numbers. '
                  'The photographs remain the source of record.\n')
    for mode, filename, label in [('faithful', 'faithful-transcription.txt', 'Faithful transcription'), ('reading', 'reading-copy.txt', 'Lightly modernised reading copy')]:
        lines = ['BERNARD SHAMBROOK’S DIARY', label, '', convention]
        for number, page in enumerate(pages, 1):
            lines.extend(['', '=' * 65, f"PHOTOGRAPH {number:02} — {page['id']}.HEIC", page['title'], '=' * 65])
            for section in page['sections']:
                lines.extend(['', section['label'], '', section[mode]])
            if mode == 'faithful' and page['notes']:
                lines.extend(['', 'EDITORIAL NOTES'] + ['- ' + note for note in page['notes']])
            if mode == 'faithful' and page['uncertainties']:
                lines.extend(['', 'UNCERTAIN READINGS'] + [f"- {item['section']} — {item['reading']}: {item['note']}" for item in page['uncertainties']])
        (ROOT / filename).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    with (ROOT / 'uncertain-readings.tsv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['Photograph', 'Source file', 'Section', 'Reading', 'Editorial note'])
        for number, page in enumerate(pages, 1):
            for item in page['uncertainties']:
                writer.writerow([number, page['id'] + '.HEIC', item['section'], item['reading'], item['note']])
    body = ['<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Complete transcription — Bernard Shambrook’s diary</title><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="enhancements.css"><link rel="stylesheet" href="monochrome.css"><script src="preferences.js" defer></script></head><body><header class="masthead"><a class="wordmark" href="index.html">Bernard Shambrook</a><nav aria-label="Main navigation"><a href="index.html">Diary</a><a href="reading.html">Reading</a><a href="index.html#scan-gallery">Photographs</a><a href="journey.html">Journey</a><a href="people.html">Names</a><a href="history.html">Records</a></nav></header><main class="complete">',
            '<h1>Complete transcription</h1>',
            '<p class="intro-note">Both text versions, in photograph order. Print using your browser.</p>',
            '<nav><a href="index.html">Transcription</a><a href="faithful-transcription.txt" download>Faithful text</a><a href="reading-copy.txt" download>Reading copy</a><a href="uncertain-readings.tsv" download>Uncertain readings</a></nav>',
            '<p class="edition-note">' + html.escape(convention) + '</p>']
    for number, page in enumerate(pages, 1):
        pid = html.escape(page['id'])
        body.extend([f'<section id="{pid}"><p class="eyebrow">Photograph {number:02} · {pid}.HEIC</p><h2>{html.escape(page["title"])}</h2>',
                     f'<p class="photo-ref"><a href="index.html#{pid}">Compare with the photograph</a> · <a href="assets/photos/{pid}.jpg">Open full image</a></p>'])
        for mode, label in [('faithful', 'Faithful transcription'), ('reading', 'Reading copy')]:
            body.append(f'<h3>{label}</h3>')
            for section in page['sections']:
                body.append('<p class="eyebrow">' + html.escape(section['label']) + '</p><div class="transcript-text">' + marked(section[mode]) + '</div>')
        if page['notes']:
            body.append('<h3>Editorial notes</h3>')
            for note in page['notes']:
                body.append('<p class="edition-note">' + html.escape(note) + '</p>')
        if page['uncertainties']:
            body.append('<h3>Uncertain readings</h3><ul>')
            for item in page['uncertainties']:
                body.append('<li>' + html.escape(item['section'] + ' — ' + item['reading'] + ': ' + item['note']) + '</li>')
            body.append('</ul>')
        body.append('</section>')
    body.append('</main></body></html>')
    (ROOT / 'complete-transcription.html').write_text('\n'.join(body) + '\n', encoding='utf-8')
    (ROOT / '.nojekyll').touch()
    print(f'Generated reader data, two text editions, complete HTML and uncertainty register for {len(pages)} photographs.')


if __name__ == '__main__':
    main()
    if (ROOT / 'build-journey.py').exists():
        import runpy
        runpy.run_path(str(ROOT / 'build-journey.py'), run_name='__main__')
    if (ROOT / 'build-gallery.py').exists():
        import runpy
        runpy.run_path(str(ROOT / 'build-gallery.py'), run_name='__main__')

    for builder in ["build-history.py", "build-edition.py", "build-map.py", "build-archive.py"]:
        if (ROOT / builder).exists():
            import runpy
            runpy.run_path(str(ROOT / builder), run_name="__main__")
