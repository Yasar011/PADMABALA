// Padmabala S portfolio: menu panel, scroll-lit statements, swatch image swap,
// scroll reveal, chapter scrollspy, keyboard-accessible lightbox.
document.documentElement.classList.add('js');
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

// 1. Menu panel
const btn = document.querySelector('.menu-btn'), menu = document.getElementById('menu');
if (btn && menu) {
  const set = (open) => {
    menu.hidden = !open;
    btn.setAttribute('aria-expanded', open);
    btn.querySelector('span').textContent = open ? 'Close' : 'Menu';
    if (open) menu.querySelector('a').focus();
  };
  btn.addEventListener('click', () => set(menu.hidden));
  menu.addEventListener('click', (ev) => { if (ev.target.closest('a')) set(false); });
  document.addEventListener('keydown', (ev) => { if (ev.key === 'Escape' && !menu.hidden) { set(false); btn.focus(); } });
}

// 2. Statements light up word by word as they scroll through the viewport
const lit = [];
document.querySelectorAll('.words:not(.label)').forEach((p) => {
  const walk = document.createTreeWalker(p, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walk.nextNode()) nodes.push(walk.currentNode);
  nodes.forEach((t) => {
    const frag = document.createDocumentFragment();
    t.textContent.split(/(\s+)/).forEach((s) => {
      if (!s.trim()) { frag.append(s); return; }
      const w = document.createElement('span'); w.className = 'w'; w.textContent = s; frag.append(w);
    });
    t.replaceWith(frag);
  });
  lit.push([p, [...p.querySelectorAll('.w')]]);
});
const paint = () => {
  const vh = innerHeight;
  lit.forEach(([p, ws]) => {
    const r = p.getBoundingClientRect();
    const k = reduce ? 1 : Math.min(1, Math.max(0, (vh * 0.85 - r.top) / (r.height + vh * 0.3)));
    const n = Math.round(k * ws.length);
    ws.forEach((w, i) => w.classList.toggle('on', i < n));
  });
};
if (lit.length) { addEventListener('scroll', paint, { passive: true }); addEventListener('resize', paint); paint(); }

// 3. Collection swatches swap the main image
document.querySelectorAll('.s-item').forEach((it) => {
  const main = it.querySelector('.s-img img'), bs = it.querySelectorAll('.sw-btn');
  bs.forEach((b, i) => {
    b.setAttribute('aria-pressed', i === 0);
    b.addEventListener('click', () => {
      main.src = b.dataset.src;
      bs.forEach((o) => o.setAttribute('aria-pressed', o === b));
    });
  });
});

// 4. Gentle reveal on scroll
const rv = document.querySelectorAll('main section:not(.hero-full):not(.opener), .garment, .s-item, .spec');
if ('IntersectionObserver' in window && !reduce) {
  const io = new IntersectionObserver((es) => es.forEach((en) => {
    if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
  }), { rootMargin: '0px 0px -8% 0px' });
  rv.forEach((el) => { el.classList.add('rv'); io.observe(el); });
}

// 5. Chapter nav: mark the chapter in view
const links = [...document.querySelectorAll('.chnav a')];
if (links.length && 'IntersectionObserver' in window) {
  const spy = new IntersectionObserver((es) => es.forEach((en) => {
    if (!en.isIntersecting) return;
    links.forEach((a) => a.setAttribute('aria-current', a.hash === '#' + en.target.id ? 'true' : 'false'));
  }), { rootMargin: '-40% 0px -55% 0px' });
  links.forEach((a) => { const t = document.querySelector(a.hash); if (t) spy.observe(t); });
}

// 6. Lightbox for work images (not heroes, cards, inline thumbs or menu)
const imgs = [...document.querySelectorAll('main img')]
  .filter((i) => !i.closest('.opener, .hero-full, .s-item, .statement, .bleed-line'));
if (imgs.length && window.HTMLDialogElement) {
  const d = document.createElement('dialog');
  d.className = 'lightbox';
  d.setAttribute('aria-label', 'Image viewer');
  d.innerHTML = '<button class="lb-btn lb-close" type="button">Close</button>' +
    '<button class="lb-btn lb-prev" type="button" aria-label="Previous image">←</button>' +
    '<button class="lb-btn lb-next" type="button" aria-label="Next image">→</button><img alt=""><p></p>';
  document.body.append(d);
  const big = d.querySelector('img'), cap = d.querySelector('p');
  let cur = 0;
  const show = (n) => {
    cur = (n + imgs.length) % imgs.length;
    big.src = imgs[cur].currentSrc || imgs[cur].src; big.alt = imgs[cur].alt;
    cap.textContent = `${imgs[cur].alt} — ${cur + 1} / ${imgs.length}`;
  };
  imgs.forEach((im, n) => {
    im.classList.add('zoomable');
    im.tabIndex = 0;
    im.setAttribute('role', 'button');
    im.setAttribute('aria-label', 'Enlarge: ' + im.alt);
    im.addEventListener('click', () => { show(n); d.showModal(); });
    im.addEventListener('keydown', (ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); show(n); d.showModal(); } });
  });
  d.querySelector('.lb-close').onclick = () => d.close();
  d.querySelector('.lb-prev').onclick = () => show(cur - 1);
  d.querySelector('.lb-next').onclick = () => show(cur + 1);
  d.addEventListener('click', (ev) => { if (ev.target === d || ev.target === big) d.close(); });
  d.addEventListener('keydown', (ev) => { if (ev.key === 'ArrowLeft') show(cur - 1); if (ev.key === 'ArrowRight') show(cur + 1); });
  d.addEventListener('close', () => imgs[cur].focus());
}
