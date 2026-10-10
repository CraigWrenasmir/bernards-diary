(() => {
  'use strict';
  const key = 'bernard-diary-theme';
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  const get = (name, fallback = '') => {try {return localStorage.getItem(name) || fallback;} catch (_) {return fallback;}};
  const set = (name, value) => {try {localStorage.setItem(name, value);} catch (_) { /* Reading remains usable when browser storage is unavailable. */ }};
  let choice = get(key, 'light');
  if (!['light', 'dark', 'system'].includes(choice)) choice = 'light';
  function apply() {
    document.documentElement.dataset.theme = choice === 'system' ? (system.matches ? 'dark' : 'light') : choice;
    document.documentElement.dataset.themePreference = choice;
    document.querySelectorAll('[data-theme-select]').forEach(select => {select.value = choice;});
  }
  function init() {
    const header = document.querySelector('.masthead');
    if (!header || header.querySelector('[data-theme-select]')) return;
    const label = document.createElement('label'); label.className = 'theme-preference'; label.textContent = 'Appearance';
    const select = document.createElement('select'); select.dataset.themeSelect = ''; select.setAttribute('aria-label', 'Appearance');
    for (const [value, text] of [['system', 'System'], ['light', 'Light'], ['dark', 'Dark']]) {
      const option = document.createElement('option'); option.value = value; option.textContent = text; select.append(option);
    }
    select.value = choice;
    select.addEventListener('change', () => {choice = select.value; set(key, choice); apply();});
    label.append(select); header.append(label);
    const nav = header.querySelector('nav');
    if (nav) {
      nav.id ||= 'site-navigation';
      const toggle = document.createElement('button');
      toggle.type = 'button'; toggle.className = 'site-menu-toggle'; toggle.textContent = 'Menu';
      toggle.setAttribute('aria-controls', nav.id); toggle.setAttribute('aria-expanded', 'false');
      const closeMenu = () => {header.removeAttribute('data-menu-open'); toggle.setAttribute('aria-expanded', 'false');};
      toggle.addEventListener('click', () => {
        const open = !header.hasAttribute('data-menu-open');
        header.toggleAttribute('data-menu-open', open); toggle.setAttribute('aria-expanded', String(open));
      });
      nav.addEventListener('click', event => {if (event.target.closest('a')) closeMenu();});
      header.addEventListener('keydown', event => {if (event.key === 'Escape' && header.hasAttribute('data-menu-open')) {closeMenu(); toggle.focus();}});
      header.insertBefore(toggle, nav); header.setAttribute('data-menu-ready', '');
    }
  }
  window.BERNARD_PREFERENCES = {get, set};
  apply();
  system.addEventListener('change', apply);
  window.addEventListener('storage', event => {if (event.key === key) {choice = get(key, 'light'); apply();}});
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
