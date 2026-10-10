(() => {
  'use strict';
  const gallery = document.getElementById('scan-gallery');
  const dialog = document.getElementById('scan-gallery-dialog');
  // Ordinary JPEG links remain usable if the browser does not support dialogs.
  if (!gallery || !dialog || typeof dialog.showModal !== 'function') return;
  const cards = Array.from(gallery.querySelectorAll('[data-scan-id]'));
  if (!cards.length) return;
  const byId = suffix => document.getElementById(`scan-gallery-${suffix}`);
  const photograph = byId('image');
  const viewport = byId('viewport');
  const canvas = byId('canvas');
  const zoom = byId('zoom');
  const reader = document.getElementById('reader');
  const hasReader = Boolean(reader && window.DIARY_DATA?.pages?.length);
  const hasContinuousReader = Boolean(document.querySelector('.reading-article'));
  let current = 0;
  let opener = null;
  let restoreOpener = true;

  const plainClick = event => event.button === 0 && !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey;

  function readTranscription(event, index) {
    if (!(hasReader || hasContinuousReader) || !plainClick(event)) return;
    event.preventDefault();
    if (dialog.open) {
      // This action moves focus into the reader rather than back to the gallery.
      restoreOpener = false;
      dialog.close();
    }
    const oldURL = location.href;
    history.replaceState(null, '', `#${cards[index].dataset.scanId}`);
    // The existing reader listens for hashchange. Dispatch even for an unchanged
    // hash so a repeated transcription link still updates and reveals the reader.
    window.dispatchEvent(new HashChangeEvent('hashchange', {oldURL, newURL: location.href}));
    if (hasContinuousReader) {
      const article = document.getElementById(cards[index].dataset.scanId);
      article?.scrollIntoView({block: 'start', behavior: 'instant'});
      const heading = article?.querySelector('h3,h2');
      if (heading) { heading.tabIndex = -1; heading.focus({preventScroll: true}); }
    } else {
      reader.scrollIntoView({block: 'start', behavior: 'instant'});
      document.getElementById('page-title')?.focus({preventScroll: true});
    }
  }

  function fitPhotograph(centre = false) {
    if (!dialog.open || !photograph.naturalWidth) return;
    const padding = 32;
    const ratio = photograph.naturalHeight / photograph.naturalWidth;
    const availableWidth = Math.max(1, viewport.clientWidth - padding);
    const availableHeight = Math.max(1, viewport.clientHeight - padding);
    const fittedWidth = Math.min(availableWidth, availableHeight / ratio);
    const imageWidth = fittedWidth * Number(zoom.value) / 100;
    const imageHeight = imageWidth * ratio;
    photograph.style.width = `${imageWidth}px`;
    photograph.style.height = `${imageHeight}px`;
    canvas.style.width = `${Math.max(viewport.clientWidth, imageWidth + padding)}px`;
    canvas.style.height = `${Math.max(viewport.clientHeight, imageHeight + padding)}px`;
    if (centre) {
      viewport.scrollLeft = Math.max(0, (canvas.offsetWidth - viewport.clientWidth) / 2);
      viewport.scrollTop = Math.max(0, (canvas.offsetHeight - viewport.clientHeight) / 2);
    }
  }

  function render(index) {
    current = Math.max(0, Math.min(cards.length - 1, index));
    const card = cards[current];
    const id = card.dataset.scanId;
    const title = card.dataset.scanTitle;
    byId('modal-title').textContent = title;
    byId('position').textContent = `Photograph ${current + 1} of ${cards.length} · ${id}`;
    photograph.alt = `${title}: photograph ${current + 1} of Bernard Shambrook’s notebook`;
    photograph.src = `assets/photos/${id}.jpg`;
    byId('transcription').href = `${hasReader || hasContinuousReader ? 'index.html' : 'complete-transcription.html'}#${id}`;
    byId('full').href = `assets/photos/${id}.jpg`;
    byId('original').href = `assets/originals/${id}.HEIC`;
    byId('original').download = `${id}.HEIC`;
    const active = document.activeElement;
    byId('previous').disabled = current === 0;
    byId('next').disabled = current === cards.length - 1;
    if (active === byId('previous') && byId('previous').disabled) (byId('next').disabled ? byId('close') : byId('next')).focus();
    if (active === byId('next') && byId('next').disabled) (byId('previous').disabled ? byId('close') : byId('previous')).focus();
    zoom.value = '100';
    byId('zoom-value').value = '100%';
    viewport.scrollLeft = 0;
    viewport.scrollTop = 0;
    fitPhotograph();
  }

  cards.forEach((card, index) => {
    const readLink = card.querySelector('[data-scan-read]');
    if ((hasReader || hasContinuousReader) && readLink) {
      readLink.href = `index.html#${card.dataset.scanId}`;
      readLink.addEventListener('click', event => readTranscription(event, index));
    }
    const link = card.querySelector('[data-scan-open]');
    link.setAttribute('aria-haspopup', 'dialog');
    link.setAttribute('aria-controls', dialog.id);
    link.addEventListener('click', event => {
      if (!plainClick(event)) return;
      event.preventDefault();
      opener = link;
      restoreOpener = true;
      render(index);
      dialog.showModal();
      byId('close').focus();
      fitPhotograph();
    });
  });

  function move(delta) {
    const next = current + delta;
    if (next >= 0 && next < cards.length) render(next);
  }
  byId('previous').addEventListener('click', () => move(-1));
  byId('next').addEventListener('click', () => move(1));
  byId('close').addEventListener('click', () => dialog.close());
  byId('transcription').addEventListener('click', event => readTranscription(event, current));
  dialog.addEventListener('close', () => {
    if (restoreOpener && opener?.isConnected) opener.focus({preventScroll: true});
  });
  dialog.addEventListener('keydown', event => {
    if (event.ctrlKey || event.metaKey || event.altKey || event.target.matches('input, select, textarea, [contenteditable="true"]')) return;
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      move(event.key === 'ArrowLeft' ? -1 : 1);
    }
  });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
  });
  zoom.addEventListener('input', () => {
    byId('zoom-value').value = `${zoom.value}%`;
    fitPhotograph(true);
  });
  photograph.addEventListener('load', () => fitPhotograph());
  if (typeof ResizeObserver === 'function') new ResizeObserver(() => fitPhotograph()).observe(viewport);
  else window.addEventListener('resize', () => fitPhotograph());
})();
