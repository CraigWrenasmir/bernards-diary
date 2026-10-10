'use strict';
(() => {
  const controls=document.getElementById('reading-controls');
  const preferenceKey='bernard-diary-reading-mode';
  if(controls){
    const articles=[...document.querySelectorAll('.reading-article')];
    const search=document.getElementById('reading-search');
    const theme=document.getElementById('reading-theme');
    const jump=document.getElementById('reading-jump');
    const result=document.getElementById('reading-result');
    const buttons=[...controls.querySelectorAll('[data-mode]')];
    const corpus=new Map(articles.map(a=>[a,a.textContent.toLocaleLowerCase()]));
    let mode='reading';
    try{if(localStorage.getItem(preferenceKey)==='faithful')mode='faithful';}catch{}
    function setMode(next){
      mode=next;
      document.documentElement.classList.add('reading-enhanced');
      document.querySelectorAll('[data-edition]').forEach(el=>{
        if(el.tagName==='DETAILS')el.open=true;
        el.hidden=el.dataset.edition!==mode;
      });
      buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===mode)));
      try{localStorage.setItem(preferenceKey,mode);}catch{}
    }
    function filter(){
      const query=search.value.trim().toLocaleLowerCase();let visible=0;
      articles.forEach(a=>{
        a.hidden=!(corpus.get(a).includes(query)&&(theme.value==='all'||a.dataset.themes.split(' ').includes(theme.value)));
        if(!a.hidden)visible++;
      });
      result.textContent=`${visible} of ${articles.length} photographs · ${mode==='reading'?'reading copy':'faithful transcription'}`;
      document.getElementById('reading-empty').hidden=visible!==0;
    }
    function reset(){search.value='';theme.value='all';filter();}
    function revealHash(){
      const id=decodeURIComponent(location.hash.slice(1));
      const el=document.getElementById(id);
      const article=el?.closest('.reading-article');
      if(article){if(article.hidden)reset();requestAnimationFrame(()=>el.scrollIntoView({block:'start'}));}
    }
    controls.hidden=false;setMode(mode);filter();
    search.addEventListener('input',filter);theme.addEventListener('change',filter);
    buttons.forEach(b=>b.addEventListener('click',()=>{setMode(b.dataset.mode);filter();}));
    document.getElementById('reading-reset').addEventListener('click',reset);
    document.getElementById('reading-print').addEventListener('click',()=>window.print());
    jump.addEventListener('change',()=>{if(jump.value){reset();location.hash=jump.value;revealHash();}});
    window.addEventListener('hashchange',revealHash);revealHash();
    window.addEventListener('storage',e=>{if(e.key===preferenceKey){setMode(e.newValue==='faithful'?'faithful':'reading');filter();}});
  }
  const peopleControls=document.getElementById('people-controls');
  if(peopleControls){
    const search=document.getElementById('people-search');
    const cards=[...document.querySelectorAll('.name-card')];
    const letters=[...document.querySelectorAll('.name-letter')];
    const corpus=new Map(cards.map(c=>[c,c.textContent.toLocaleLowerCase()]));
    function filter(){
      const q=search.value.trim().toLocaleLowerCase();let visible=0;
      cards.forEach(c=>{c.hidden=!corpus.get(c).includes(q);if(!c.hidden)visible++;});
      letters.forEach(l=>l.hidden=![...l.querySelectorAll('.name-card')].some(c=>!c.hidden));
      document.getElementById('people-result').textContent=`${visible} of ${cards.length} name headings`;
      document.getElementById('people-empty').hidden=visible!==0;
    }
    peopleControls.hidden=false;search.addEventListener('input',filter);filter();
    function reveal(){
      const el=document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if(el?.matches('.name-card,.name-letter')){search.value='';filter();requestAnimationFrame(()=>el.scrollIntoView({block:'start'}));}
    }
    document.querySelectorAll('.name-alphabet a').forEach(a=>a.addEventListener('click',()=>{search.value='';filter();}));
    window.addEventListener('hashchange',reveal);reveal();
  }
})();
