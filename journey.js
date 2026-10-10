(() => {
  'use strict';
  const data = window.JOURNEY_DATA;
  if (!data?.events?.length) return;
  const $ = id => document.getElementById(id);
  const make = (tag, text, cls) => {const el = document.createElement(tag); if (text !== undefined) el.textContent = text; if (cls) el.className = cls; return el;};
  let current = 0, view = 'voyage';
  const zooms = {};
  const pan = $('map-window'), canvas = $('map-viewport');
  function mapSize() {
    const zoom = zooms[view] ||= view === 'regional' ? Math.min(3, Math.max(1, 840 / pan.clientWidth)) : 1;
    canvas.style.width = `${pan.clientWidth * zoom}px`;
    pan.style.height = `${Math.min(480, Math.max(240, pan.clientWidth * .63))}px`;
    $('map-zoom-level').textContent = Math.round(zoom * 100) + '%';
    $('map-zoom-out').disabled = zoom <= 1; $('map-zoom-in').disabled = zoom >= 4;
    pan.classList.toggle('can-pan', zoom > 1);
    const overview = view === 'regional' && canvas.clientWidth < 650;
    $('map-pins').hidden = overview; $('map-overview-note').hidden = !overview;
  }
  function centreEntry() {
    const pin = data.maps[view].pins.find(pin => pin.place === data.events[current].place);
    $('map-centre').disabled = !pin;
    pan.scrollLeft = (pin ? pin.x / 1000 : .5) * canvas.clientWidth - pan.clientWidth / 2;
    pan.scrollTop = (pin ? pin.y / 630 : .5) * canvas.clientHeight - pan.clientHeight / 2;
  }
  function zoomMap(next) {
    const centreX = (pan.scrollLeft + pan.clientWidth / 2) / canvas.clientWidth;
    const centreY = (pan.scrollTop + pan.clientHeight / 2) / canvas.clientHeight;
    zooms[view] = Math.max(1, Math.min(4, next)); mapSize();
    pan.scrollLeft = centreX * canvas.clientWidth - pan.clientWidth / 2;
    pan.scrollTop = centreY * canvas.clientHeight - pan.clientHeight / 2;
  }
  function link(label, href, cls) {const el = make('a', label, cls); el.href = href; return el;}
  function drawMap() {
    const config = data.maps[view];
    $('map-window').dataset.extent = view;
    $('map-base').src = `assets/maps/${view}.svg`;
    $('map-base').alt = config.description;
    $('download-map').href = `assets/maps/${view}.svg`;
    $('open-map').href = `assets/maps/${view}.svg`;
    $('map-note').textContent = config.note;
    $('map-pins').replaceChildren();
    document.querySelectorAll('[data-view]').forEach(el => el.setAttribute('aria-pressed', String(el.dataset.view === view)));
    const currentEvent = data.events[current], currentPlace = currentEvent.place;
    for (const pin of config.pins) {
      const place = data.places[pin.place];
      const active = currentPlace === pin.place;
      const kind = active ? currentEvent.mapKind || '' : pin.kind || '';
      const button = make('button', pin.label, `map-pin ${kind}`);
      button.type = 'button'; button.style.left = `${pin.x / 10}%`; button.style.top = `${pin.y / 6.3}%`;
      button.title = place.name; button.setAttribute('aria-label', active ? `${place.name}: ${currentEvent.kindLabel}, ${currentEvent.dateLabel}` : `${place.name}: show diary entry`);
      button.setAttribute('aria-pressed', String(active)); button.dataset.place = pin.place; button.dataset.mapKind = kind;
      button.addEventListener('click', () => {if (!active) {select(data.events.findIndex(e => e.id === pin.event), false); document.querySelector(`[data-place="${pin.place}"]`)?.focus({preventScroll:true});}});
      $('map-pins').append(button);
    }
    mapSize(); centreEntry();
  }
  function renderDetail() {
    const e = data.events[current], panel = $('event-detail'); panel.replaceChildren();
    panel.dataset.event = e.id;
    panel.append(make('p', e.dateLabel, 'event-date'), make('span', e.kindLabel, `evidence-label ${e.caution ? 'caution' : ''}`), make('h3', e.title), make('p', e.description));
    if (e.quote) panel.append(make('blockquote', e.quote));
    if (e.note) panel.append(make('p', e.note, 'event-note'));
    const place = data.places[e.place];
    panel.append(make('p', place ? place.precision : 'No pin: the entry does not securely establish a geographic position.', 'geo-note'));
    const sources = make('div', undefined, 'event-sources');
    for (const source of e.sources) sources.append(link(`${source} ↗`, `index.html#${source}`));
    panel.append(sources);
    if (place) {
      const others = data.events.filter(item => item.place === e.place && item.id !== e.id);
      if (others.length) {const related = make('div', 'Other entries for this place', 'related-entries'); related.append(make('br')); for (const other of others) {const button = make('button', other.dateLabel); button.type = 'button'; button.addEventListener('click', () => select(data.events.indexOf(other))); related.append(button);} panel.append(related);}
    }
    $('entry-range').value = current;
    $('entry-range').setAttribute('aria-valuetext', `${e.dateLabel}: ${e.title}`);
    $('entry-position').textContent = `Entry ${current + 1} of ${data.events.length} · ${e.dateLabel}`;
    $('entry-previous').disabled = current === 0;
    $('entry-next').disabled = current === data.events.length - 1;
    document.querySelectorAll('.entry-button').forEach(el => el.setAttribute('aria-current', String(Number(el.dataset.index) === current)));
    document.querySelectorAll('[data-month]').forEach(el => el.setAttribute('aria-pressed', String(el.dataset.month === (e.month || 'undated'))));
  }
  function select(index, adjustView = true, updateHash = true) {
    if (index < 0 || index >= data.events.length) return;
    current = index;
    if (adjustView) view = data.events[current].view || view;
    if (updateHash) history.replaceState(null, '', `#${data.events[current].id}`);
    drawMap(); renderDetail();
  }
  function fromHash() {const idx = data.events.findIndex(e => `#${e.id}` === location.hash); if (idx >= 0) select(idx, true, false);}
  function revealEntry(index) {select(index); document.querySelector('.stepper').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth',block:'start'});}
  $('entry-range').max = data.events.length - 1;
  $('entry-range').addEventListener('input', () => select(Number($('entry-range').value)));
  $('entry-previous').addEventListener('click', () => select(current - 1));
  $('entry-next').addEventListener('click', () => select(current + 1));
  document.querySelectorAll('[data-view]').forEach(el => el.addEventListener('click', () => {view = el.dataset.view; drawMap();}));
  $('entry-count').textContent = `${data.events.length} records`;
  data.events.forEach((e, i) => {const li = make('li'), b = make('button', undefined, 'entry-button'); b.type = 'button'; b.dataset.index = i; b.append(make('span', e.dateLabel), document.createTextNode(e.title), make('small', e.kindLabel)); b.addEventListener('click', () => revealEntry(i)); li.append(b); $('entry-list').append(li);});
  const months = [...new Set(data.events.map(e => e.month || 'undated'))];
  for (const month of months) {const first = data.events.findIndex(e => (e.month || 'undated') === month); const b = make('button', month === 'undated' ? 'Uncertain / undated' : new Date(month + '-15T12:00:00').toLocaleDateString('en-AU', {month:'short'})); b.type = 'button'; b.dataset.month = month; b.addEventListener('click', () => revealEntry(first)); $('month-track').append(b);}
  function relatedSources(card, d) {if (d.relatedSources?.length) {const p = make('div', 'Related pages: ', 'related-pages'); d.relatedSources.forEach((id,i) => {if (i) p.append(document.createTextNode(' · ')); p.append(link(id, `index.html#${id}`));}); card.append(p);}}
  data.drawings.forEach(d => {const card = make('article', undefined, 'drawing-card'), a = link('', `index.html#${d.source}`), img = make('img'); img.src = `assets/companion/${d.source}.jpg`; img.alt = d.alt; img.loading = 'lazy'; img.width = d.width; img.height = d.height; a.append(img, make('h3', d.title)); card.append(a, make('p', d.dateNote, 'drawing-date'), make('p', d.caption), link('Transcription', `index.html#${d.source}`, 'source-link')); relatedSources(card,d); $('drawing-gallery').append(card);});
  data.themes.forEach((d, i) => {const card = make('article', undefined, 'daily-card'), a = link('', `index.html#${d.source}`, 'daily-main'); a.append(make('span', String(i + 1).padStart(2,'0'), 'card-number'), make('h3', d.title), make('p', d.caption), make('span', 'Transcription', 'source-link')); card.append(a); relatedSources(card,d); $('daily-gallery').append(card);});
  window.addEventListener('hashchange', fromHash);
  $('map-zoom-in').addEventListener('click', () => zoomMap((zooms[view] || 1) + .5));
  $('map-zoom-out').addEventListener('click', () => zoomMap((zooms[view] || 1) - .5));
  $('map-fit').addEventListener('click', () => zoomMap(1));
  $('map-centre').addEventListener('click', centreEntry);
  pan.addEventListener('keydown', event => {
    if (event.target !== pan) return;
    if (['+','=','-','0','Home','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(event.key)) event.preventDefault();
    if (event.key === '+' || event.key === '=') zoomMap((zooms[view] || 1) + .5);
    if (event.key === '-') zoomMap((zooms[view] || 1) - .5);
    if (event.key === '0' || event.key === 'Home') zoomMap(1);
    if (event.key === 'ArrowLeft') pan.scrollLeft -= 70; if (event.key === 'ArrowRight') pan.scrollLeft += 70;
    if (event.key === 'ArrowUp') pan.scrollTop -= 70; if (event.key === 'ArrowDown') pan.scrollTop += 70;
  });
  let drag = null;
  pan.addEventListener('pointerdown', event => {
    if (event.pointerType !== 'mouse' || event.button !== 0 || event.target.closest('button') || (zooms[view] || 1) <= 1) return;
    event.preventDefault(); pan.focus({preventScroll:true}); pan.setPointerCapture(event.pointerId);
    drag = {x:event.clientX, y:event.clientY, left:pan.scrollLeft, top:pan.scrollTop}; pan.classList.add('dragging');
  });
  pan.addEventListener('pointermove', event => {if (drag) {pan.scrollLeft = drag.left - event.clientX + drag.x; pan.scrollTop = drag.top - event.clientY + drag.y;}});
  const stopDrag = () => {drag = null; pan.classList.remove('dragging');};
  pan.addEventListener('pointerup', stopDrag); pan.addEventListener('pointercancel', stopDrag); pan.addEventListener('lostpointercapture', stopDrag);
  window.addEventListener('resize', () => {mapSize(); centreEntry();});
  select(0, true, false); fromHash();
})();
