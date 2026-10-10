(() => {
  'use strict';
  const pages = window.DIARY_DATA?.pages || [];
  if (!pages.length) return;
  const $ = id => document.getElementById(id);
  let storedMode; try {storedMode = localStorage.getItem('bernard-diary-reading-mode');} catch (_) {}
  let current = 1, mode = ['faithful','reading'].includes(storedMode) ? storedMode : 'faithful', enhanced = false, leaf = 'full';
  const crops = window.DIARY_CROPS || {};
  function saveMode() {try {localStorage.setItem('bernard-diary-reading-mode', mode);} catch (_) {}}
  const make = (tag, text, className) => { const el = document.createElement(tag); if (text !== undefined) el.textContent = text; if (className) el.className = className; return el; };
  const isUncertain = value => /\?|illegible|unclear|obscured/i.test(value);
  function markedText(container, text) {
    const re = /\[[^\]\n]+\]/g;
    let start = 0;
    for (const match of text.matchAll(re)) {
      container.append(document.createTextNode(text.slice(start, match.index)));
      const marked = make(isUncertain(match[0]) ? 'mark' : 'span', match[0], isUncertain(match[0]) ? '' : 'editorial-marker');
      container.append(marked); start = match.index + match[0].length;
    }
    container.append(document.createTextNode(text.slice(start)));
  }
  function listPages() {
    const term = $('search').value.trim().toLocaleLowerCase();
    const list = $('page-list'); list.replaceChildren(); let found = 0;
    pages.forEach((page, index) => {
      const haystack = JSON.stringify([page.title, page.id, page.sections, page.notes, page.uncertainties]).toLocaleLowerCase();
      if (term && !haystack.includes(term)) return;
      found++;
      const link = make('a', undefined, 'page-list-item'); link.href = `#${page.id}`;
      if (current === index) link.setAttribute('aria-current', 'page');
      const img = make('img'); img.src = `assets/thumbs/${page.id}.jpg`; img.alt = ''; img.loading = 'lazy'; img.width = 37; img.height = 43;
      const label = make('span'); label.append(make('small', `Photograph ${String(index + 1).padStart(2, '0')}`), document.createTextNode(page.title));
      link.append(img, label); link.addEventListener('click', event => {event.preventDefault(); navigate(index);}); list.append(link);
    });
    $('result-count').textContent = term ? `${found} of ${pages.length}` : String(pages.length);
    $('empty-search').hidden = found > 0;
  }
  function render() {
    const page = pages[current];
    $('position').textContent = `Photograph ${current + 1} of ${pages.length}`;
    $('previous').disabled = current === 0; $('next').disabled = current === pages.length - 1;
    $('source-name').textContent = page.id + '.HEIC'; $('page-title').textContent = page.title;
    $('permalink').href = `#${page.id}`;
    renderImage();
    $('transcription').replaceChildren();
    page.sections.forEach(section => {
      const wrap = make('section', undefined, 'text-section'); wrap.append(make('h4', section.label));
      const side = /^left\b/i.test(section.label) ? 'left' : /^right\b/i.test(section.label) ? 'right' : null;
      if (side && crops[page.id]?.[side]) {
        const show = make('button', `${side[0].toUpperCase() + side.slice(1)} page`, 'section-photo'); show.type = 'button';
        show.addEventListener('click', () => {leaf = side; renderImage(); $('enlarge').click();}); wrap.append(show);
      }
      const text = make('div', undefined, `transcript-text ${mode}`); markedText(text, section[mode]); wrap.append(text); $('transcription').append(wrap);
    });
    $('editorial-notes').replaceChildren();
    if (page.notes.length) { $('editorial-notes').append(make('h4', 'Editorial notes')); page.notes.forEach(note => $('editorial-notes').append(make('p', note))); }
    $('uncertainties').replaceChildren();
    page.uncertainties.forEach(item => { const li = make('li'); li.append(make('strong', `${item.section}: ${item.reading} `), document.createTextNode(item.note)); $('uncertainties').append(li); });
    $('uncertainty-panel').hidden = !page.uncertainties.length;
    $('uncertainty-panel').open = false;
    $('uncertainty-summary').textContent = `Uncertain readings (${page.uncertainties.length})`;
    $('mode-description').textContent = mode === 'faithful' ? 'Original wording and line breaks. Square brackets are editorial; highlighted readings remain uncertain.' : 'Lightly modernised spelling and punctuation. Uncertain readings remain marked.';
    document.querySelectorAll('[data-mode]').forEach(button => {const selected = button.dataset.mode === mode; button.setAttribute('aria-selected', String(selected)); button.tabIndex = selected ? 0 : -1;});
    $('transcription').setAttribute('aria-labelledby', `mode-${mode}`);
    listPages();
  }
  function renderImage() {
    const page = pages[current], crop = crops[page.id]?.[leaf];
    const img = $('page-image'); img.src = crop ? crop.src : `assets/photos/${page.id}.jpg`;
    img.alt = `${page.title}: ${crop ? leaf + ' page view of ' : ''}photograph ${current + 1} of Bernard Shambrook’s notebook`;
    img.classList.toggle('high-contrast', enhanced);
    $('image-link').href = `assets/photos/${page.id}.jpg`;
    $('original-link').href = `assets/originals/${page.id}.HEIC`;
    $('original-link').download = `${page.id}.HEIC`;
    $('image-caption').textContent = `Source photograph ${String(current + 1).padStart(2, '0')} · ${page.id}${crop ? ' · ' + crop.label : ''}`;
    $('source-view-controls').hidden = !crops[page.id];
    $('crop-note').hidden = !crop;
    document.querySelectorAll('[data-leaf]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.leaf === leaf)));
  }
  document.querySelectorAll('[data-leaf]').forEach(button => button.addEventListener('click', () => {leaf = button.dataset.leaf; renderImage();}));
  function navigate(index, updateHash = true) {
    leaf = 'full';
    current = Math.max(0, Math.min(pages.length - 1, index));
    if (updateHash) history.replaceState(null, '', `#${pages[current].id}`);
    render();
  }
  function fromHash() { const idx = pages.findIndex(page => '#' + page.id === location.hash); if (idx >= 0) { navigate(idx, false); $('reader').scrollIntoView({behavior: 'instant'}); } }
  $('previous').addEventListener('click', () => navigate(current - 1));
  $('next').addEventListener('click', () => navigate(current + 1));
  $('search').addEventListener('input', listPages);
  document.querySelectorAll('[data-mode]').forEach(button => {
    button.addEventListener('click', () => {mode = button.dataset.mode; saveMode(); render();});
    button.addEventListener('keydown', event => {if (['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) {event.preventDefault();mode = event.key === 'Home' ? 'faithful' : event.key === 'End' ? 'reading' : mode === 'faithful' ? 'reading' : 'faithful';saveMode();render();$(`mode-${mode}`).focus();}});
  });
  $('contrast').addEventListener('click', () => {enhanced = !enhanced;$('contrast').setAttribute('aria-pressed',String(enhanced));$('contrast').textContent = enhanced ? 'Original contrast' : 'Increase contrast';$('page-image').classList.toggle('high-contrast', enhanced);});
  $('enlarge').addEventListener('click', () => {const page = pages[current];$('zoom-title').textContent = page.id + (leaf === 'full' ? ' · Full photograph' : ' · ' + leaf + ' page');$('zoom').value = '100';$('zoom-image').src = $('page-image').src;$('zoom-image').alt = $('page-image').alt;$('zoom-image').style.width = '100%';$('zoom-image').classList.toggle('high-contrast',enhanced);$('image-dialog').showModal();$('zoom').focus();});
  $('zoom').addEventListener('input', () => {$('zoom-image').style.width = $('zoom').value + '%';});
  $('close-dialog').addEventListener('click', () => $('image-dialog').close());
  $('image-dialog').addEventListener('click', event => {if (event.target === $('image-dialog')) $('image-dialog').close();});
  window.addEventListener('hashchange', fromHash);
  if (matchMedia('(max-width: 850px)').matches) $('browse-details').open = false;
  render();fromHash();
})();
