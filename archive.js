(() => {
  'use strict';
  const contrast=document.getElementById('photo-contrast');
  contrast?.addEventListener('click',()=>{
    const enabled=contrast.getAttribute('aria-pressed')!=='true';
    contrast.setAttribute('aria-pressed',String(enabled));
    contrast.textContent=enabled?'Normal photograph contrast':'Increase photograph contrast';
    document.body.classList.toggle('increase-photo-contrast',enabled);
  });
  function reveal(){
    let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}
    const element=document.getElementById(id);if(!element)return;
    let parent=element;while(parent){if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement;}
  }
  window.addEventListener('hashchange',reveal);reveal();
  const search=document.getElementById('people-search');
  search?.addEventListener('input',()=>{
    document.querySelectorAll('.archive-name-grid .name-card').forEach(card=>{card.open=Boolean(search.value.trim())&&!card.hidden;});
  });
})();
