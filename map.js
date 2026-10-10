(() => {
  'use strict';
  const root = document.querySelector('.travel-section');
  const source = document.getElementById('travel-data');
  if (!root || !source) return;
  let data;
  try { data = JSON.parse(source.textContent); } catch (_) { return; }
  const { events, places, maps, config } = data;
  if (!events?.length) return;
  const $ = id => document.getElementById(id);
  const el = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (className) node.className = className;
    return node;
  };
  const link = (text, href) => { const node = el('a', text); node.href = href; return node; };
  const knownPosition = place => place && Number.isFinite(place.lat) && Number.isFinite(place.lon);
  let index = 0, view = 'voyage', map = null, layer = null, routeGroup = null, markerGroup = null;
  let ready = false, attempted = false, tileTimer = null, loaded = 0, failed = 0;
  let markers = {};
  const coarse = window.matchMedia('(pointer: coarse)').matches;
  const panel = $('travel-detail');
  const fallback = $('travel-fallback');
  const status = $('travel-map-status');
  const mapNode = $('travel-map');
  const viewButtons = [...root.querySelectorAll('[data-travel-view]')];

  function fallbackView(message = '') {
    fallback.hidden = false;
    mapNode.hidden = true;
    ready = false;
    $('travel-fit').disabled = true;
    $('travel-drag').hidden = true;
    status.textContent = message;
    status.hidden = !message;
    $('travel-fallback-image').src = config.views[view].fallback;
    $('travel-fallback-image').alt = maps[view].description;
    $('travel-fallback-link').href = config.views[view].fallback;
  }

  function theme() {
    if (!routeGroup) return;
    const dark = document.documentElement.dataset.theme === 'dark';
    routeGroup.eachLayer(route => route.setStyle({ color: dark ? '#e6e6e6' : '#303030' }));
  }

  function sources(event, className = 'travel-sources') {
    const p = el('p', undefined, className);
    if (event.readingQuote) p.append(document.createTextNode('Reading copy · '));
    event.sources.forEach((id, i) => {
      if (i) p.append(document.createTextNode(' · '));
      p.append(link(id, `index.html#${id}`));
    });
    return p;
  }

  function popup(placeId) {
    const holder = el('div', undefined, 'travel-popup');
    const place = places[placeId];
    holder.append(el('strong', place.name));
    const related = events.filter(event => event.place === placeId);
    related.forEach(event => {
      const row = el('p');
      row.append(el('span', event.dateLabel), document.createTextNode(' · '), link(event.quoteSource, `index.html#${event.quoteSource}`));
      if (event.kindLabel) row.append(el('span', event.kindLabel, 'travel-popup-kind'));
      holder.append(row);
    });
    if (placeId === 'rehovoth') holder.append(el('p', 'Recorded destination', 'travel-popup-note'));
    if (placeId === 'jerusalem') holder.append(el('p', 'Undated drawing', 'travel-popup-note'));
    return holder;
  }

  function markerIcon(pin, active) {
    const kind = pin.kind || '';
    return L.divIcon({
      className: `travel-marker ${kind} ${active ? 'is-current' : ''}`,
      html: `<span>${pin.label}</span>`,
      iconSize: [27, 27], iconAnchor: [13.5, 13.5], popupAnchor: [0, -17]
    });
  }

  function renderLayers(fit = false) {
    if (!map) return;
    routeGroup.clearLayers();
    markerGroup.clearLayers();
    markers = {};
    const selectedPlace = events[index].place;
    config.routes.filter(route => route.view === view).forEach(route => {
      L.polyline(route.points, {
        color: '#303030', weight: 2, opacity: .85,
        dashArray: route.kind === 'sea' ? '6 7' : null,
        interactive: false
      }).addTo(routeGroup);
    });
    maps[view].pins.forEach(pin => {
      const place = places[pin.place];
      if (!knownPosition(place)) return;
      const related = events.filter(event => event.place === pin.place);
      const marker = L.marker([place.lat, place.lon], {
        icon: markerIcon(pin, selectedPlace === pin.place),
        title: `${place.name}: ${related.map(event => event.dateLabel).join('; ')}`,
        alt: `${place.name}: ${related.map(event => event.dateLabel).join('; ')}`,
        keyboard: true, riseOnHover: true
      }).addTo(markerGroup);
      marker.bindPopup(popup(pin.place), { maxWidth: 300, maxHeight: 230, autoPan: true });
      marker.on('click', () => {
        const chosen = events[index].place === pin.place ? index : events.findIndex(event => event.id === pin.event);
        select(chosen, false);
      });
      markers[pin.place] = { marker, pin };
    });
    theme();
    if (fit) fitView();
  }

  function highlight() {
    for (const [place, entry] of Object.entries(markers)) {
      entry.marker.setIcon(markerIcon(entry.pin, events[index].place === place));
    }
  }

  function fitView() {
    if (!map || !ready) return;
    map.invalidateSize({ pan: false });
    map.fitBounds(config.views[view].bounds, { padding: [28, 28], animate: false });
  }

  function changeView(next, fit = true) {
    if (!config.views[next]) return;
    const changed = next !== view;
    view = next;
    root.dataset.mapView = view;
    viewButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.travelView === view)));
    $('travel-fallback-image').src = config.views[view].fallback;
    $('travel-fallback-image').alt = maps[view].description;
    $('travel-fallback-link').href = config.views[view].fallback;
    if (map && changed) renderLayers(fit);
    else if (fit) fitView();
  }

  function select(next, pan = true) {
    if (!Number.isInteger(next) || next < 0 || next >= events.length) return;
    index = next;
    const event = events[index];
    // Suez can be read in either view; other entries select their own map.
    const nextView = event.place === 'suez' && view === 'voyage' ? 'voyage' : event.view;
    changeView(nextView, true);
    panel.dataset.event = event.id;
    panel.replaceChildren(el('p', event.dateLabel, 'travel-date'), el('h3', event.title));
    if (event.readingQuote || event.quote) panel.append(el('blockquote', event.readingQuote || event.quote));
    panel.dataset.quoteVersion = event.readingQuote ? 'reading' : 'faithful';
    panel.append(sources(event));
    $('travel-entry').value = String(index);
    $('travel-range').value = String(index);
    $('travel-range').setAttribute('aria-valuetext', `${event.dateLabel}: ${event.title}`);
    $('travel-position').textContent = `${index + 1} / ${events.length}`;
    $('travel-previous').disabled = index === 0;
    $('travel-next').disabled = index === events.length - 1;
    root.querySelectorAll('[data-travel-index]').forEach(item => {
      if (Number(item.dataset.travelIndex) === index) item.setAttribute('aria-current', 'step');
      else item.removeAttribute('aria-current');
    });
    highlight();
    if (ready && pan && markers[event.place]) {
      const target = markers[event.place].marker.getLatLng();
      if (!map.getBounds().pad(-.1).contains(target)) map.panTo(target, { animate: false });
    }
  }

  function activate() {
    if (!map || ready) return;
    clearTimeout(tileTimer);
    ready = true;
    mapNode.hidden = false;
    fallback.hidden = true;
    status.hidden = true;
    $('travel-fit').disabled = false;
    $('travel-drag').hidden = !coarse;
    map.invalidateSize({ pan: false });
  }

  function initialiseMap() {
    if (attempted || !window.L) return;
    if (!/^https?:$/.test(location.protocol)) {
      fallbackView('Saved map. Open the hosted site for the interactive map.');
      return;
    }
    if (!navigator.onLine) {
      fallbackView('Offline: showing the saved map.');
      return;
    }
    attempted = true;
    mapNode.hidden = false;
    map = L.map(mapNode, {
      scrollWheelZoom: false, dragging: !coarse, touchZoom: true,
      doubleClickZoom: false, boxZoom: false, zoomControl: true,
      minZoom: 2, maxZoom: 13, worldCopyJump: false,
      zoomAnimation: false, fadeAnimation: false, markerZoomAnimation: false,
      attributionControl: true
    });
    map.attributionControl.setPrefix(false);
    mapNode.setAttribute('aria-describedby', 'travel-map-status');
    routeGroup = L.layerGroup().addTo(map);
    markerGroup = L.layerGroup().addTo(map);
    map.fitBounds(config.views[view].bounds, { padding: [28, 28], animate: false });
    layer = L.tileLayer(config.tileUrl, {
      maxZoom: 19,
      attribution: `&copy; <a href="${config.attributionUrl}">OpenStreetMap</a> contributors`,
      updateWhenIdle: true, keepBuffer: 0,
      // Standard browser cache and Referer behaviour meet OSM's web-client policy.
      referrerPolicy: 'strict-origin-when-cross-origin'
    });
    layer.on('loading', () => { loaded = 0; failed = 0; });
    layer.on('tileload', () => { loaded++; activate(); });
    layer.on('tileerror', () => { failed++; });
    layer.on('load', () => {
      if (!loaded && failed) {
        fallbackView('The online map is unavailable. Showing the saved map.');
        // Leaflet finishes its tile callback after firing load; detach next turn.
        setTimeout(() => { if (layer && map.hasLayer(layer)) map.removeLayer(layer); }, 0);
      }
    });
    layer.addTo(map);
    renderLayers(false);
    tileTimer = setTimeout(() => {
      if (!loaded) {
        fallbackView('The online map is unavailable. Showing the saved map.');
        if (layer && map.hasLayer(layer)) map.removeLayer(layer);
      }
    }, 10000);
    new ResizeObserver(() => { if (ready) map.invalidateSize({ pan: false }); }).observe(mapNode.parentElement);
    new MutationObserver(theme).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  }

  root.querySelectorAll('.travel-controls, .travel-step-controls').forEach(node => { node.hidden = false; });
  $('travel-fit').disabled = true;
  $('travel-previous').addEventListener('click', () => select(index - 1));
  $('travel-next').addEventListener('click', () => select(index + 1));
  $('travel-entry').addEventListener('change', event => select(Number(event.target.value)));
  $('travel-range').addEventListener('input', event => select(Number(event.target.value)));
  $('travel-fit').addEventListener('click', fitView);
  $('travel-drag').addEventListener('click', () => {
    if (!map) return;
    const enabled = !map.dragging.enabled();
    map.dragging[enabled ? 'enable' : 'disable']();
    $('travel-drag').setAttribute('aria-pressed', String(enabled));
    $('travel-drag').textContent = enabled ? 'Stop moving map' : 'Move map';
  });
  viewButtons.forEach(button => button.addEventListener('click', () => changeView(button.dataset.travelView)));
  root.querySelectorAll('[data-travel-index]').forEach(item => item.addEventListener('click', event => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    select(Number(item.dataset.travelIndex));
    $('travel-entry').focus({ preventScroll: true });
    root.scrollIntoView({ behavior: 'auto', block: 'start' });
  }));
  window.addEventListener('offline', () => {
    fallbackView('Offline: showing the saved map.');
    if (layer && map?.hasLayer(layer)) map.removeLayer(layer);
  });
  window.addEventListener('online', () => {
    if (!map) { attempted = false; initialiseMap(); }
    else if (layer && !map.hasLayer(layer)) {
      mapNode.hidden = false;
      map.invalidateSize({ pan: false });
      map.fitBounds(config.views[view].bounds, { padding: [28, 28], animate: false });
      layer.addTo(map);
    }
  });
  select(0, false);
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) { initialiseMap(); observer.disconnect(); }
    }, { rootMargin: '100px' });
    observer.observe(root);
  } else initialiseMap();
})();
