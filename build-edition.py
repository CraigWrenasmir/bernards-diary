"""Build continuous reading, name finding aid and editorial references; no dependencies."""
from pathlib import Path
import json
import re
import html
import unicodedata
from collections import OrderedDict
ROOT = Path(__file__).resolve().parent
E = html.escape


def marked(text):
    return ''.join(f'<mark>{E(p)}</mark>' if p.startswith('[') else E(p) for p in re.split(r'(\[[^\]\n]+\])', text))


def header(title, page):
    nav = [('index.html','Diary'),('reading.html','Reading'),('index.html#scan-gallery','Photographs'),('journey.html','Journey'),('people.html','Names'),('history.html','Records')]
    links = ''.join(f'<a href="{url}"'+(' aria-current="page"' if url == page else '')+f'>{label}</a>' for url,label in nav)
    return f'''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><title>{E(title)} — Bernard Shambrook’s diary</title><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="enhancements.css"><link rel="stylesheet" href="edition.css"><link rel="stylesheet" href="monochrome.css"><script src="preferences.js" defer></script><script src="edition.js" defer></script></head><body><a class="skip-link" href="#main">Skip to content</a><header class="masthead"><a class="wordmark" href="index.html">Bernard Shambrook</a><nav aria-label="Main navigation">{links}</nav></header><main id="main" class="edition-main" data-page="{page}"><h1>{E(title)}</h1>'''


def footer():
    return '''</main><footer class="edition-footer"><p><a href="references.html">Sources</a> · <a href="corrections.html">Revisions</a> · <a href="complete-transcription.html">Complete transcription</a> · <a href="index.html#scan-gallery">Original photographs</a></p></footer></body></html>'''


THEMES = {
    'voyage': {'0904','0910','0911','0912','0928','0933'},
    'service': {'0905','0906','0907','0908','0911','0912','0913','0924','0926','0928','0929','0930','0933','0934'},
    'remembrance': {'0914','0915','0916','0917'},
    'everyday': {'0923','0925','0927','0928','0931','0932','0934'},
    'drawings': {'0908','0916','0917','0922'},
}


def build_reading(pages):
    crop_path = ROOT/'data/source-crops.json'
    crops = json.loads(crop_path.read_text()).get('pages',{}) if crop_path.exists() else {}
    manifest={x['sourceFile'].split('.')[0]:x for x in json.loads((ROOT/'data/source-manifest.json').read_text())['originals']}
    out = [header('Reading','reading.html'),
        '<p class="edition-intro">The text in photograph order. Choose the faithful transcription or lightly modernised reading copy. Square brackets mark editorial additions and uncertainty.</p>',
        '<p class="edition-intro">Themes are editorial; filtered results retain photograph order.</p>',
        '<div class="edition-links"><a href="reader.html">Inspect a photograph</a><a href="faithful-transcription.txt" download>Faithful text</a><a href="reading-copy.txt" download>Reading copy</a></div>',
        '<div class="edition-controls" id="reading-controls" hidden><div class="edition-filter-row"><label>Search<input id="reading-search" type="search" placeholder="Name, place or phrase…"></label><label>Theme<select id="reading-theme"><option value="all">All photographs</option><option value="voyage">The voyage</option><option value="service">Service &amp; fellow soldiers</option><option value="remembrance">Remembrance</option><option value="everyday">Everyday life &amp; language</option><option value="drawings">Drawings</option></select></label><label>Photograph<select id="reading-jump"><option value="">Choose a photograph…</option>']
    for n,p in enumerate(pages,1):
        out.append(f'<option value="{p["id"]}">{n:02} · {E(p["title"])}</option>')
    out += ['</select></label></div><div class="edition-control-buttons" role="group" aria-label="Text edition"><button type="button" data-mode="reading" aria-pressed="true">Reading copy</button><button type="button" data-mode="faithful" aria-pressed="false">Faithful transcription</button><button type="button" id="reading-reset">Reset filters</button><button type="button" id="reading-print">Print selection</button></div><p class="edition-result" id="reading-result" role="status" aria-live="polite"></p></div><p id="reading-empty" class="edition-empty" hidden>No photographs match. Try a shorter search or reset the filters.</p>']
    for n,p in enumerate(pages,1):
        pid=p['id']; themes=' '.join(t for t,ids in THEMES.items() if pid[-4:] in ids)
        out.append(f'<article class="reading-article" id="{pid}" data-themes="{themes}"><p class="eyebrow">Photograph {n:02} of {len(pages)} · {pid}.HEIC</p><h2>{E(p["title"])}</h2><div class="reading-source-links"><a href="reader.html#{pid}">Inspect photograph</a><a href="assets/photos/{pid}.jpg">Full photograph</a><a href="assets/originals/{pid}.HEIC" download>HEIC file</a><a href="#{pid}" aria-label="Permanent link to photograph {n:02}">Permalink</a></div>')
        groups=OrderedDict()
        for i,s in enumerate(p['sections']):
            match=re.match(r'(Left|Right)\b',s['label'],re.I)
            side=match.group(1).lower() if match else 'full'
            groups.setdefault(side,[]).append((i,s))
        for side,sections in groups.items():
            crop=crops.get(pid,{}).get(side)
            src=crop['src'] if crop else f'assets/gallery/{pid}.jpg'
            caption=f'{pid} · {side.capitalize()} page crop.' if crop else f'{pid} · Full photograph.'
            full=src if crop else f'assets/photos/{pid}.jpg'
            width=crop['width'] if crop else manifest[pid]['galleryWidth']
            height=crop['height'] if crop else manifest[pid]['galleryHeight']
            out.append(f'<div class="reading-leaf"><figure><a href="{E(full,quote=True)}"><img src="{E(src,quote=True)}" data-source-crop="{str(bool(crop)).lower()}" alt="{E(caption,quote=True)}" width="{width}" height="{height}" loading="lazy"></a><figcaption>{E(caption)}</figcaption></figure><div>')
            for i,s in sections:
                out.append(f'<section class="reading-subsection" id="{pid}-s{i}"><h3>{E(s["label"])}</h3><div data-edition="reading" class="transcript-text">{marked(s["reading"])}</div><details class="faithful-alternate" data-edition="faithful"><summary>Faithful transcription</summary><div class="transcript-text">{marked(s["faithful"])}</div></details></section>')
            out.append('</div></div>')
        compact_path=ROOT/'data/page-reading-notes.json'
        compact=json.loads(compact_path.read_text()) if compact_path.exists() else {}
        if isinstance(compact,dict) and 'pages' in compact: compact=compact['pages']
        notes=compact.get(pid,[]) if isinstance(compact,dict) else []
        if isinstance(notes,str): notes=[notes]
        if notes:
            out.append('<div class="reading-page-note">'+''.join('<p>'+E(note)+'</p>' for note in notes)+f'<a href="complete-transcription.html#{pid}">Full notes</a></div>')
        out.append('</article>')
    out.append(footer());(ROOT/'reading.html').write_text('\n'.join(out)+'\n')


def slug(s):
    return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('-')


def build_people(pages):
    config=json.loads((ROOT/'data/people-terms.json').read_text())
    names=[]
    for term in config['terms']:
        name=term if isinstance(term,str) else term['name']
        pattern=r'\b'+re.escape(name)+r'\b' if isinstance(term,str) else term['pattern']
        regex=re.compile(pattern,re.I);hits=[]
        for p in pages:
            for i,s in enumerate(p['sections']):
                for line in s['faithful'].splitlines():
                    match=regex.search(line)
                    if not match:continue
                    uncertain=any(a<=match.start()<b for a,b in ((m.start(),m.end()) for m in re.finditer(r'\[[^\]]*\?[^\]]*\]',line)))
                    hits.append({'pageId':p['id'],'section':s['label'],'sectionIndex':i,'quote':line,'uncertainName':uncertain})
        if hits:names.append({'name':name,'id':slug(name),'occurrences':hits,'allTentative':all(h['uncertainName'] for h in hits)})
    names.sort(key=lambda p:p['name'].casefold())
    (ROOT/'data/people-index.json').write_text(json.dumps({'description':config['description'],'groups':names},ensure_ascii=False,indent=2)+'\n')
    letters=sorted(set(n['name'][0].upper() for n in names))
    out=[header('Names','people.html'),
        '<p class="edition-intro">Names from the faithful transcription, with source excerpts and photographs.</p>',
        '<p class="edition-intro">A surname may refer to several people. Initials, spellings and numbers remain as written; service prefixes have not been added. Bracketed readings are tentative.</p>',
        '<div class="name-bio"><strong>Bernard Edward Shambrook</strong><br>The Tent 17 roster records <a href="index.html#IMG_0926">“NX40242 A/Sgt SHAMBROOK B.E.”</a>. See <a href="history.html">Records</a> for the WWII identification and provisional WWI connection.</div>',
        f'<div class="edition-controls" id="people-controls" hidden><div class="edition-filter-row"><label>Search names and source excerpts<input id="people-search" type="search" placeholder="For example: Shambrook, 40242 or Fred…"></label></div><p class="edition-result" id="people-result" role="status" aria-live="polite">{len(names)} name headings</p></div>',
        '<nav class="name-alphabet" aria-label="Surname alphabet">'+''.join(f'<a href="#letter-{letter}">{letter}</a>' for letter in letters)+'</nav><p id="people-empty" class="edition-empty" hidden>No names match that search.</p>']
    for letter in letters:
        out.append(f'<section class="name-letter" id="letter-{letter}"><h2>{letter}</h2><div class="name-grid">')
        for n in [n for n in names if n['name'][0].upper()==letter]:
            out.append(f'<article class="name-card" id="name-{n["id"]}"><h3>{E(n["name"])}</h3>')
            if n['allTentative']:out.append('<span class="tentative-name">Tentative reading</span>')
            out.append('<ul class="name-occurrences">')
            for h in n['occurrences']:
                pid=h['pageId'];out.append(f'<li><p class="name-quote">{marked(h["quote"])}</p><p class="name-source"><a href="index.html#{pid}">{pid} · {E(h["section"])}</a> · <a href="reading.html#{pid}-s{h["sectionIndex"]}">Read in context</a></p></li>')
            out.append('</ul></article>')
        out.append('</div></section>')
    out.append(footer());(ROOT/'people.html').write_text('\n'.join(out)+'\n')
    print(f'Generated continuous reader and {len(names)} source-linked name headings ({sum(len(n["occurrences"]) for n in names)} occurrences).')


def inline(s):
    s=E(s)
    s=re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',r'<a href="\2">\1</a>',s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
    return s


def markdown(s):
    out=[];para=[];in_list=False
    def flush():
        if para:out.append('<p>'+inline(' '.join(para))+'</p>');para.clear()
    for line in s.splitlines()+['']:
        if line.startswith('#'):
            flush()
            if in_list:out.append('</ul>');in_list=False
            m=re.match(r'(#+)\s*(.*)',line);level=min(4,len(m[1])+1)
            out.append(f'<h{level}>{inline(m[2])}</h{level}>')
        elif re.match(r'^[-*] ',line):
            flush()
            if not in_list:out.append('<ul>');in_list=True
            out.append('<li>'+inline(line[2:])+'</li>')
        elif not line.strip():
            flush()
            if in_list:out.append('</ul>');in_list=False
        else:para.append(line.strip())
    return '\n'.join(out)


def build_references():
    out=[header('Sources','references.html'),'<p class="edition-intro">The handwriting is the authority for the transcription. External records supply historical context and geographic reference points; they are not used to turn unreadable writing into certain text.</p><div class="edition-links"><a href="history.html#sources">Historical records</a><a href="corrections.html">Revisions</a><a href="SOURCE-NOTES.md">Transcription notes</a><a href="JOURNEY-SOURCES.md">Geographic sources</a></div><div class="reference-text">',markdown((ROOT/'SOURCE-NOTES.md').read_text()),markdown((ROOT/'JOURNEY-SOURCES.md').read_text()),'</div>',footer()]
    (ROOT/'references.html').write_text('\n'.join(out)+'\n')


def build_corrections():
    path=ROOT/'data/corrections.json'
    if not path.exists():return
    data=json.loads(path.read_text())
    records=data if isinstance(data,list) else data.get('corrections',data.get('entries',[]))
    out=[header('Revisions','corrections.html'),'<p class="edition-intro">Changes checked against the photographs during the comparison review of 10 October 2026. Unresolved alternatives remain marked.</p><p class="edition-intro">“Earlier” refers to the transcription before that review.</p><div class="reference-text">']
    out.append('<p><a href="data/corrections.json" download>Revision data (JSON)</a>. Comparison source: <a href="https://craigwrenasmir.github.io/bernards-diary/">the other edition supplied by Craig</a>.</p>')
    for i,c in enumerate(records,1):
        pid=c.get('pageId',c.get('source',c.get('page','')))
        if isinstance(pid,list):pid=', '.join(pid)
        title=c.get('title',c.get('field',c.get('section',f'Revision {i}')))
        out.append(f'<article class="correction-card" id="revision-{i}"><p class="eyebrow">{E(str(pid))} · {E(str(c.get("confidence","Editorial review")))}</p><h2>{E(str(title))}</h2>')
        old=c.get('old',c.get('before',''));new=c.get('new',c.get('after',''))
        out.append('<div class="correction-pair"><div><h3>Earlier reading</h3><pre>'+E(str(old))+'</pre></div><div><h3>Reviewed reading</h3><pre>'+E(str(new))+'</pre></div></div>')
        out.append('<p>'+E(str(c.get('reason',c.get('rationale',c.get('note','')))))+'</p>')
        for match in sorted(set(re.findall(r'IMG_\d{4}',str(pid)))):out.append(f'<p><a href="index.html#{match}">Inspect {match}</a> · <a href="reading.html#{match}">Read in context</a></p>')
        out.append('</article>')
    if isinstance(data,dict) and data.get('pageAudit'):
        out.append('<h2>Page review</h2><p>Revised and retained readings for each photograph.</p>')
        for audit in data['pageAudit']:
            pid=audit['pageId']
            out.append(f'<details class="reading-notes"><summary>{E(pid)}</summary><p>{E(audit["assessment"])}</p><p><a href="index.html#{pid}">Inspect photograph</a></p></details>')
    reading_path=ROOT/'data/reading-revisions.json'
    if reading_path.exists():
        out.append('<h2 id="reading-revisions">Reading-copy revisions</h2><p>Standard spellings and readings clarified by comparison. The faithful text is unchanged.</p><p><a href="data/reading-revisions.json" download>Reading revision data</a></p>')
        revision_data=json.loads(reading_path.read_text())
        items=revision_data if isinstance(revision_data,list) else revision_data.get('revisions',revision_data.get('changes',[]))
        for i,item in enumerate(items,1):
            pid=item.get('pageId','')
            out.append(f'<article class="correction-card" id="reading-revision-{i}"><h3>{E(str(pid))} · {E(str(item.get("section",item.get("sectionIndex",""))))}</h3><div class="correction-pair"><div><h4>Earlier reading copy</h4><pre>{E(str(item.get("old","")))}</pre></div><div><h4>Revised reading copy</h4><pre>{E(str(item.get("new","")))}</pre></div></div><p>{E(str(item.get("reason",item.get("rationale",""))))}</p><a href="index.html#{E(str(pid))}">Read page</a></article>')
            evidence_links=[]
            for evidence in item.get('evidence',[]):
                url=evidence.get('url')
                if url:
                    label=evidence.get('title',evidence.get('reference','Source'))
                    evidence_links.append(f'<a href="{E(url,quote=True)}">{E(label)}</a>')
            if evidence_links: out.append('<p class="reading-page-note">Evidence: '+' · '.join(evidence_links)+'</p>')
    out.extend(['</div>',footer()]);(ROOT/'corrections.html').write_text('\n'.join(out)+'\n')


if __name__=='__main__':
    pages=json.loads((ROOT/'data/diary.json').read_text())['pages']
    build_reading(pages);build_people(pages);build_references();build_corrections()
