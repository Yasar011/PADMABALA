"""Build the Padmabala S portfolio website.

Images come only from PADMABALA.pdf (extracted into work/assets by the extraction step).
Run from the repo root:  python tools/build.py  [path/to/work/assets]
Writes img/*.webp and the HTML pages next to this tools/ folder.
"""
import glob, html, os, sys
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SITE, '..', 'work', 'assets')
OUT_IMG = os.path.join(SITE, 'img')
os.makedirs(OUT_IMG, exist_ok=True)
SIZES = {'xl': 2000, 'l': 1500, 'm': 1000, 's': 600}
_done = {}
e = html.escape


def src(n):
    hits = glob.glob(os.path.join(ASSETS, '*', f'{n:03d}_*'))
    assert hits, f'image #{n} not found in {ASSETS}'
    return hits[0]


def img(n, alt, size='l', cls='', eager=False):
    """Convert source #n to WebP (once; largest size requested wins) and return an <img> tag."""
    target = SIZES[size]
    out = os.path.join(OUT_IMG, f'{n:03d}.webp')
    if _done.get(n, 0) < target:
        im = Image.open(src(n))
        im = im.convert('RGBA') if im.mode in ('RGBA', 'LA', 'P') else im.convert('RGB')
        im.thumbnail((target, target), Image.LANCZOS)
        im.save(out, 'WEBP', quality=80, method=6)
        _done[n] = target
    w, h = Image.open(out).size
    load = 'eager" fetchpriority="high' if eager else 'lazy'
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="img/{n:03d}.webp" width="{w}" height="{h}" alt="{e(alt)}" loading="{load}" decoding="async">'


def chip_hex(n):
    """Sample the colour of one of her Pantone chip images."""
    im = Image.open(src(n)).convert('RGB')
    return '#%02X%02X%02X' % im.getpixel((im.width // 2, int(im.height * .3)))


def fig(n, alt, cap='', size='l', cls=''):
    c = f'<figcaption>{cap}</figcaption>' if cap else ''
    return f'<figure class="{cls}">{img(n, alt, size)}{c}</figure>'


# ---------- page shell ----------
FONTS = ('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;'
         '1,6..72,300;1,6..72,400&family=Hanken+Grotesk:wght@400;500;600&display=swap')
PROJECTS = [  # href, title, chip, year, sub, main image, alt, swatch thumbs
    ('raw.html', 'RAW — The Unmasked Emotion', 'Couture', '2026', 'Seven garments · Team collection', 19,
     'Model in a sculptural grey draped headpiece, hands raised to the face', [68, 83, 74]),
    ('bleed-bloom.html', 'Bleed &amp; Bloom', 'Print &amp; dye', '2025', 'Brand-based project · Aniclothing', 182,
     'Model on a rock against blue sky in a hand-painted print dress', [176, 147, 177]),
    ('contained.html', 'Contained', 'Ready-to-wear', '2025', 'Brand-based project · Haderlump', 241,
     'Model seated against a brick wall in a black jacket, corset and pleated skirt', [185, 235, 222]),
    ('in-between.html', 'The In Between', 'Denim', '2025', 'Denim collection · AW 26/27', 305,
     'Model in a navy denim look caught in a web of red yarn', [308, 294, 264]),
]
DOTS = '<svg width="10" height="10" viewBox="0 0 10 10" aria-hidden="true"><circle cx="2" cy="2" r="1.3"/><circle cx="8" cy="2" r="1.3"/><circle cx="2" cy="8" r="1.3"/><circle cx="8" cy="8" r="1.3"/></svg>'


def page(fname, title, desc, body, accent='#990213', accent_dark='#D69038'):
    thumbs = ''.join(f'<a class="m-item" href="{h}">{img(n, alt, "m")}<span class="label">{t}</span></a>'
                     for h, t, chip, yr, sub, n, alt, th in PROJECTS)
    doc = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="img/305.webp">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet"><link rel="stylesheet" href="style.css">
<style>:root{{--accent:{accent};--accent-dark:{accent_dark}}}</style>
</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="bar">
  <button class="pill menu-btn" type="button" aria-expanded="false" aria-controls="menu"><span>Menu</span>{DOTS}</button>
  <a class="pill pill--ghost mark" href="index.html">Padmabala S</a>
  <a class="pill pill--ghost right" href="#contact">Contact</a>
</header>
<div id="menu" class="menu" hidden>
  <div class="menu-in">
    <div class="m-grid">{thumbs}</div>
    <nav class="m-links" aria-label="Main">
      <a href="index.html">Home</a><a href="index.html#work">Collections</a><a href="info.html">Info</a><a href="#contact">Contact</a>
    </nav>
  </div>
</div>
<main id="main">{body}</main>
<footer id="contact" class="foot invert">
  <p class="label">Contact</p>
  <p class="foot-big"><a href="mailto:padmabalas05@gmail.com">padmabalas05@gmail.com</a></p>
  <ul class="foot-links">
    <li><a class="pill" href="https://www.behance.net/padmabala" rel="noopener">Behance</a></li>
    <li><a class="pill" href="https://www.linkedin.com/in/padmabalaS" rel="noopener">LinkedIn</a></li>
  </ul>
  <p class="label foot-small">Padmabala S — B.Des Fashion Design, NIFT Jodhpur, 2023–2027</p>
</footer>
<script src="main.js" defer></script>
</body></html>'''
    open(os.path.join(SITE, fname), 'w', encoding='utf-8').write(doc)


def proj_nav(prev, nxt):
    p = f'<a href="{prev[0]}"><span class="label">Previous</span>{prev[1]}</a>' if prev else '<span></span>'
    n = f'<a class="next" href="{nxt[0]}"><span class="label">Next</span>{nxt[1]}</a>' if nxt else '<span></span>'
    return f'<nav class="pnav" aria-label="Collections">{p}{n}</nav>'


CH = ['Brief', 'Audience &amp; research', 'Ideation &amp; process', 'Execution &amp; impact']


def case(glance_rows, chapters):
    """Case-study body: at-a-glance card, sticky chapter nav, then the four chapters (assignment brief order)."""
    ids = ['brief', 'research', 'process', 'outcome']
    g = ''.join(f'<div><dt class="label">{k}</dt><dd>{v}</dd></div>' for k, v in glance_rows)
    nav = ''.join(f'<a href="#{i}"><span>{n + 1:02d}</span> {t}</a>' for n, (i, t) in enumerate(zip(ids, CH)))
    body = ''.join(f'<div class="chapter" id="{i}"><h2 class="ch-head"><span class="label">{n + 1:02d}</span>{t}</h2>{c}</div>'
                   for n, (i, t, c) in enumerate(zip(ids, CH, chapters)))
    return (f'<section class="glance" aria-label="Case study at a glance"><p class="label">Case study at a glance</p><dl>{g}</dl></section>'
            f'<nav class="chnav" aria-label="Case study chapters">{nav}</nav>{body}')


def chips(items):
    out = ''.join(f'<li><span class="sw" style="background:{h}"></span><b>{e(nm)}</b><span class="label">{e(code)}</span></li>'
                  for nm, code, h in items)
    return f'<ul class="chips">{out}</ul>'


def swatches(hexes, note):
    out = ''.join(f'<li><span class="sw" style="background:{h}"></span><span class="label">{h}</span></li>' for h in hexes)
    return f'<ul class="swatches">{out}</ul><p class="label note">{note}</p>'


def opener(no, title, kind, year, n, alt, lead, pos='50% 35%'):
    """Full-bleed photo, then title and a scroll-revealed statement."""
    return f'''<section class="opener">
  <div class="op-img">{img(n, alt, 'xl', eager=True).replace('<img ', f'<img style="object-position:{pos}" ', 1)}</div>
  <div class="op-txt">
    <p class="label">No.{no} · {kind} · {year}</p>
    <h1 class="display">{title}</h1>
    <p class="words">{lead}</p>
  </div>
</section>'''


def inl(n, alt):
    return img(n, alt, 's', 'inl')


# ---------- HOME ----------
def shop_item(h, t, chip, yr, sub, n, alt, th):
    sw = ''.join(f'<button class="sw-btn" type="button" data-src="img/{k:03d}.webp" aria-label="Show another image from {t}">{img(k, "", "s")}</button>'
                 for k in [n] + th)
    return f'''<article class="s-item">
  <a class="s-img" href="{h}">{img(n, alt, 'l')}</a>
  <div class="s-row"><a href="{h}"><span class="label strong">{t}</span> <span class="tag">{chip}</span></a><span class="label strong">{yr}</span></div>
  <p class="label">{sub}</p>
  <div class="s-sw">{sw}</div>
</article>'''


home = f'''<section class="hero-full">
  {img(305, 'Model in a navy denim look caught in a web of red yarn, from The In Between', 'xl', eager=True)}
  <p class="label hero-cap">Padmabala S — Fashion design portfolio, 2026</p>
  <a class="pill hero-cta" href="#work">View collections</a>
</section>
<section class="statement">
  <p class="words big-words">Padmabala S {inl(121, 'Watercolour motif')} is a fashion design student at <a href="info.html">NIFT Jodhpur</a>, specialising in heritage &amp; couture. She treats the environment as a living archive {inl(48, 'Illustration from RAW')} where life experiences and artistic observations are translated into <a href="#work">thoughtful silhouettes</a>.</p>
  <a class="mini" href="raw.html">{img(93, 'RAW on the IGNUS 2026 runway', 's')}<span class="label strong">RAW — Winning Collection, Spectrum’26</span></a>
</section>
<section id="work" class="shop" aria-label="Collections">
  <h2 class="sec-title">Four collections</h2>
  <p class="label center">Couture · Print &amp; dye · Ready-to-wear · Denim</p>
  <div class="s-grid">{''.join(shop_item(*p) for p in PROJECTS)}</div>
</section>
<section class="bleed-line">
  {img(181, 'Bleed & Bloom look on a rocky landscape', 'xl')}
  <p>Treating the environment as a living archive.</p>
</section>
<section class="band invert">
  <p class="label">Recognition</p>
  <ul class="awards">
    <li><b>Winning Collection</b><span class="label">Spectrum’26, NIFT Jodhpur — RAW</span></li>
    <li><b>1st Runner-Up Collection</b><span class="label">IGNUS’26, IIT Jodhpur — RAW</span></li>
    <li><b>1st Runner-Up</b><span class="label">Antarang fashion show 2025, Ignus, IIT Jodhpur</span></li>
  </ul>
  <a class="pill pill--light more" href="info.html">About Padmabala</a>
</section>'''
page('index.html', 'Padmabala S — Fashion Design Portfolio',
     'Portfolio of Padmabala S, B.Des Fashion Design student (Heritage & Couture) at NIFT Jodhpur.', home)

# ---------- INFO ----------
SKILLS = ['Fashion illustration', 'Pattern making', 'Draping', 'Print design', 'Garment construction', 'Luxury couture',
          'Surface embellishments', 'Trend forecasting research', 'Fashion styling', 'Time management',
          'Teamwork &amp; collaboration', 'Communication', 'Presentation']
info = f'''<section class="info">
  <div class="info-head">
    <p class="label">Info</p>
    <h1 class="display">Padmabala <em>S</em></h1>
    <p class="lead">I am a third-year Fashion Design student who treats the environment as a living archive, where life experiences and artistic observations are translated into thoughtful silhouettes. I take an artistic approach to design, focusing on conceptual storytelling rather than a single style. I enjoy exploring diverse textiles and creative techniques to build unique, conceptually strong collections. I am artistically driven and eager for new experiences that will help me grow as a designer.</p>
  </div>
  <figure class="info-portrait">{img(8, 'Portrait of Padmabala S in a black leather jacket', 's')}<figcaption>Padmabala S</figcaption></figure>
  <dl class="cv">
    <div><dt class="label">Education</dt><dd>Bachelor of Design (Fashion Design)<br>Specialisation: Heritage &amp; Couture<br>National Institute of Fashion Technology, Jodhpur<br><span class="label">2023–2027</span></dd></div>
    <div><dt class="label">Achievements</dt><dd><ul>
      <li>1st position — Spectrum 2026, NIFT Jodhpur</li>
      <li>1st runner-up — Antarang fashion show 2026, Ignus, IIT Jodhpur</li>
      <li>1st runner-up — Antarang fashion show 2025, Ignus, IIT Jodhpur</li>
      <li>Craft Research Document on Kota Doria — July 2025</li></ul></dd></div>
    <div><dt class="label">Skills</dt><dd><ul class="cols">{''.join(f'<li>{s}</li>' for s in SKILLS)}</ul></dd></div>
    <div><dt class="label">Software</dt><dd>Adobe Photoshop · Adobe Illustrator · Adobe Lightroom · Procreate · CLO 3D</dd></div>
    <div><dt class="label">Languages</dt><dd>English · Malayalam · Hindi</dd></div>
  </dl>
</section>'''
page('info.html', 'Info — Padmabala S', 'About, education, skills and achievements of Padmabala S.', info)

# ---------- RAW ----------
G = [  # (title, text from her PDF, illustration, large photo, small photo)
    ('The façade', 'The first garment shows a person presenting themselves in a clean and controlled way. The silhouette looks polished, composed and socially acceptable, representing the outer version we create to hide what truly exists inside.', 52, 56, 55),
    ('First cracks', 'The second garment shows the person slowly starting to reveal their true self. Distorted forms and shifting layers represent the first cracks in the illusion, where the hidden identity begins to come forward.', 58, 59, 61),
    ('Disclosure', 'The third garment represents the identity being disclosed. Darker layers and heavier construction show discomfort and frustration, as the person feels exposed and wounded, struggling between hiding again or accepting the truth.', 62, 63, 64),
    ('Outburst', 'The fourth garment shows anger and emotional outburst. Dramatic movement and heavy construction represent all the suppressed feelings finally coming out after being hidden for so long.', 48, 68, 70),
    ('Numbness', 'The fifth garment shows complete numbness. The hood represents refusing to be socially available, while the heavy silhouette shows the weight carried inside. The fringe details represent confusion slowly turning into acceptance.', 72, 74, 73),
    ('Shock', 'The sixth garment represents shock after the outburst. The person feels frozen and emotionally drained, the restricted form showing something dying deep inside while silence takes over outside.', 77, 80, 79),
    ('Acceptance', 'The final garment represents complete acceptance. The outer layers are removed and the person stands as their true self, no longer hiding behind illusion, fear or social expectations. What was once buried beneath performance and survival is now worn openly, with nothing left to prove and nothing left to conceal.', 81, 85, 84),
]
raw_chips = [('Estate Blue', '19-4027 TCX', chip_hex(37)), ('Espresso', '19-1103 TCX', chip_hex(38)),
             ('Arona', '16-4109 TPG', chip_hex(39)), ('Silver Blue', '16-4706 TPX', chip_hex(40)),
             ('Deep Teal', '19-4914 TCX', chip_hex(41)), ('Cabernet', '19-1724 TCX', chip_hex(42)),
             ('Biking Red', '19-1650 TPX', chip_hex(43)), ('Stalactite', '11-4101 TCX', chip_hex(44)),
             ('Red Dahlia', '19-1555 TCX', chip_hex(45))]
garments = ''.join(f'''<article class="garment {'flip' if i % 2 else ''}">
  <div class="g-txt"><p class="g-no">{i + 1:02d}</p><h3>{t}</h3><p>{tx}</p></div>
  <figure class="g-ill">{img(ill, f'Illustration of garment {i + 1}', 'm')}<figcaption>Sketch — garment {i + 1:02d}</figcaption></figure>
  <figure class="g-big">{img(big, f'Garment {i + 1}, final shoot', 'l')}<figcaption>Garment {i + 1:02d} — final</figcaption></figure>
  <figure class="g-small">{img(sm, f'Garment {i + 1}, detail', 'm')}</figure>
</article>''' for i, (t, tx, ill, big, sm) in enumerate(G))
POEM = ['I thought I had mastered it', 'The art of hiding', 'Put up these walls,', 'But they seem to be colliding',
        'I woke up early', 'And practiced my smile', 'I don’t know why,', 'It never reaches my eyes', 'So I cover it up',
        'With the mask I’ve built', 'Hoping they can’t see', 'That it often tilts', 'How do I laugh', 'With all this rage inside',
        'Wouldn’t it be better', 'If I just went', 'quiet?']
raw = opener(1, 'RAW', 'Avant-garde couture', 2026, 19, 'Model in a sculptural grey draped headpiece, hands raised to the face',
             'The Unmasked Emotion — a team collection of seven garments on duality, delusion and chaos.') + case(
    [('Brief', 'Spectrum 2026 fashion show — theme “Vibhram”, seven garments'),
     ('Team', 'Team RAW — five designers, one of them Padmabala'),
     ('Process', 'Mood research, illustration, seven-garment narrative'),
     ('Outcome', 'Winning Collection, Spectrum’26 · 1st Runner-Up Collection, IGNUS’26')],
    [f'''<section class="concept two">
  <div><p class="label">Fashion show brief</p><p class="big">Create a collection taking the Spectrum 2026 theme (Vibhram) as inspiration.</p>
  <p class="body">Maximum six participants: five designers and one stylist. Each team develops a collection of seven garments, judged over three jury rounds.</p></div>
  <div><p class="label">Concept</p><p class="body">This collection deals with what we perceive as reality vs what it actually is. The version of ourselves that we reveal as a package wrapped up with a bow — is it the same on the inside, or is the exterior an illusion created to withhold our true selves?</p>
  <p class="body">It explores the themes of duality, delusion and chaos. How we build a wall around ourselves, brick by brick, and what happens when it starts to crack, bit by bit, until there’s no place to hide anymore.</p></div>
</section>''',
     f'''<section class="mood invert">
  <div class="poem"><p class="label">Mood — a poem</p><p>{'<br>'.join(POEM)}</p></div>
  <div class="mood-grid">{''.join(fig(n, a, '', 'm') for n, a in [(25, 'Painted mood reference: hands over a face'), (32, 'Mood reference: figure behind frosted glass'), (33, 'Mood reference: kneeling figure with smoke-like faces'), (35, 'Mood reference: a translucent mask')])}</div>
</section>
<section class="palette"><p class="label">Colour — Pantone</p>{chips(raw_chips)}</section>''',
     f'''<section class="lineup"><p class="label">Line-up — seven garments, one emotional arc</p>
  <div class="lineup-row">{''.join(img(n, f'Illustration, garment {i + 1}', 'm') for i, n in enumerate([52, 51, 47, 48, 46, 50, 49]))}</div></section>
<section class="garments"><p class="label">Sketch to garment</p>{garments}</section>''',
     f'''<section class="runway invert"><p class="label">Runway — IGNUS 2026, IIT Jodhpur</p>
  <div class="runway-grid">{''.join(img(n, 'RAW on the IGNUS 2026 runway', 'm') for n in [88, 89, 90, 91, 92, 93])}</div></section>
<section class="team">
  <div><p class="label">Impact</p>
  <p class="big">Winning Collection at Spectrum’26 and 1st Runner-Up Collection at IGNUS’26.</p>
  <p class="body">Team RAW is a collective of five fashion design students who came together to present the collection: Ayushi Mahajan, Gunisha Rathi, Mahika Rai, Naynika Mitial and Padmabala.</p></div>
  {fig(101, 'Team RAW on stage at the show', 'Team RAW on stage', 'l')}
</section>''']) + proj_nav(None, ('bleed-bloom.html', 'Bleed &amp; Bloom'))
page('raw.html', 'RAW — The Unmasked Emotion — Padmabala S', 'Avant-garde couture team collection, 2026. Winning Collection at Spectrum’26.', raw, '#87161B', '#E0707A')

# ---------- BLEED & BLOOM ----------
steps = [(129, 'Texture', 'Texture exploration using watercolour.'), (121, 'Motif', 'Watercolour hand-painted motifs.'),
         (166, 'Dye', 'Ice-dyed fabric (georgette).'), (169, 'Embellish', 'Sequins and beads.'),
         (164, 'Drape', 'Pleating done by draping.'), (170, 'Finish', 'Embroidery details.')]
bb = opener(2, 'Bleed <em>&amp;</em> Bloom', 'Print &amp; tie-dye, brand-based project', 2025, 176, 'Model reclining on rocks in a hand-painted ochre slip dress',
            'Fruits and flowers, what if they share the same skin; both reaching, both ripening, both beautifully impermanent.', '50% 45%') + case(
    [('Brief', 'Brand-based print &amp; tie-dye collection for Aniclothing'),
     ('Audience', 'Women, 22–35, upper-middle to affluent, urban India'),
     ('Process', 'Watercolour textures, hand-painted motifs, repeats, ice dye, draping'),
     ('Outcome', 'Print range, five-look range plan, final outdoor shoot')],
    [f'''<section class="concept two">
  <div><p class="label">Brief</p><p class="big">Develop a print and dye-led collection in the language of Aniclothing.</p></div>
  <div><p class="label">Concept</p><p class="body">Fruits and flowers, what if they share the same skin; both reaching, both ripening, both beautifully impermanent. Where colour deepens, softens, and spills into something new. Inspired by the tropics in their quieter hours, saturated in some places, soft and dissolving in others. And then what comes after: dusty, muted, warm like memory, like dusk, like something willingly being let go.</p>
  <p class="label words">Playful · Ease · Warmth · Abundance</p></div>
</section>''',
     f'''<section class="brand">
  <div class="brand-txt"><p class="label">Brand study — Aniclothing</p>
  <p class="body">Aniclothing is a contemporary pret wear brand founded by Shivani Aggarwal, a Parsons School of Design alumna. Known for vibrant self hand-painted prints, minimal silhouettes and maximal personality, the brand bridges Western design sensibilities with cultural roots. Every piece is elegant, effortless and proudly made in India.</p></div>
  <div class="brand-txt"><p class="label">Client profile</p><p class="big">Young, fashion-forward women who are digitally active and style-conscious.</p>
  <p class="body">Age 22–35 · Female · Upper-middle to affluent · Urban India with global appeal. They seek clothing that is visually distinctive, artisanal and expressive, and are willing to invest in premium pret wear that truly stands out.</p></div>
</section>
<section class="palette">{swatches(['#D69038', '#E9BD76', '#AC8472', '#C4A9A2', '#555335', '#4F3215'], 'Sampled from the final garments and painted swatches. Board references Pantone 14-1911, 14-0846, 15-3920, 16-0430, 17-0535 and 16-1358 TPX.')}</section>''',
     f'''<section class="motifs"><p class="label">Motif &amp; texture explorations</p>
  <div class="motif-row">{''.join(img(n, 'Watercolour motif study', 'm') for n in [121, 143, 125, 126, 142])}</div>
  <div class="tex-row">{fig(130, 'Watercolour texture tests on paper', 'Watercolour texture tests', 'l')}{fig(128, 'Watercolour texture tests', 'Colour bleeds', 'l')}</div></section>
<section class="prints invert"><p class="label">Prints — repeats and colourways</p>
  <div class="print-grid">
    {fig(147, 'Repeat print on olive ground', '10" × 10"', 'l', 'p-big')}
    {fig(157, 'Repeat print on navy ground', '6" × 6"', 'm')}{fig(155, 'Repeat print on white ground', '6" × 6"', 'm')}
    {fig(159, 'Repeat print on dusk ground', '6" × 6"', 'm')}{fig(152, 'Repeat print, fruit and leaf motifs', '4" × 4"', 'm')}
  </div></section>
<section class="range"><p class="label">Range plan</p>{img(154, 'Range plan: five illustrated looks', 'xl')}</section>
<section class="process"><p class="label">Making</p>
  <ol class="steps">{''.join(f'<li><span class="label">{i + 1:02d} / {t}</span>{img(n, note, "m")}<p>{note}</p></li>' for i, (n, t, note) in enumerate(steps))}</ol></section>''',
     f'''<section class="lookbook lb-bb"><p class="label">Final shoot</p>
  <div class="lb">{''.join(img(n, 'Bleed & Bloom final look on a rocky landscape', 'l') for n in [182, 177, 103, 181, 178, 180, 175])}</div></section>''']) + proj_nav(('raw.html', 'RAW'), ('contained.html', 'Contained'))
page('bleed-bloom.html', 'Bleed & Bloom — Padmabala S', 'Print & tie-dye brand-based project for Aniclothing, 2025.', bb, '#8A5A12', '#E9BD76')

# ---------- CONTAINED ----------
ct = opener(3, 'Contained', 'Brand-based ready-to-wear', 2025, 185, 'Model in a black jacket over a grey laced corset and pleated skirt, black background',
            'What is held, and what is allowed to fall free.', '50% 22%') + case(
    [('Brief', 'Brand-based ready-to-wear collection for Haderlump, Berlin'),
     ('Audience', 'Women (also unisex), 25–40, high disposable income, urban creative hubs'),
     ('Process', 'Silhouette exploration, pleating, draped corset'),
     ('Outcome', 'Final illustration, studio and location lookbooks')],
    [f'''<section class="concept two">
  <div><p class="label">Concept</p><p class="big">Contained is a study in emotional discipline as the highest form of authority. In an era of radical exposure, it proposes that the most powerful act is choosing what you reveal.</p></div>
  <div><p class="body">There is a strength that does not announce itself — the strength of a woman who carries entire worlds within her. The collection is built on a single tension: what is held, and what is allowed to fall free.</p>
  <p class="label words">Boundaried · Protective · Rebuilt · Quiet · Powerful</p></div>
</section>''',
     f'''<section class="brand invert">
  <div class="brand-txt"><p class="label">Brand study — Haderlump</p>
  <p class="big">“At Haderlump, we see fashion as a timeless force — an extension of the self, a form of armor in an unpredictable world. It protects, empowers, and reveals.”</p></div>
  <div class="brand-txt"><p class="body">Haderlump positions fashion as a shield and extension of identity, prioritising emotional depth over trends. Each garment is a vessel of memory and individuality, crafted with integrity. Produced on-demand in its Berlin atelier, the brand embraces conscious creation and rejects the disposability of fast fashion.</p>
  <p class="label">Client profile</p><p class="body">Age 25–40 · Female (also unisex) · High disposable income · Urban creative hubs. They treat clothing as identity and storytelling, seek experimental silhouettes and concept-driven pieces, and move through fashion weeks, art exhibitions and underground cultural spaces.</p></div>
</section>
<section class="material">
  <div><p class="label">Colour — Pantone</p>{chips([('Dawn Blue', '13-4303 TCX', chip_hex(213)), ('Estate Blue', '19-4027 TCX', chip_hex(37)), ('Espresso', '19-1103 TCX', chip_hex(38))])}
  {swatches(['#0E0F0F', '#364742', '#566E67', '#95AEAC', '#6D727B'], 'Sampled from the finished garments.')}</div>
  <div><p class="label">Fabric board</p><div class="fab">{img(206, 'Dark twill fabric swatch', 's')}{img(207, 'Denim fabric swatch', 's')}</div>{img(208, 'Five fabric samples laid out', 'm')}</div>
</section>''',
     f'''<section class="sil"><p class="label">Silhouette exploration — from line to colour</p>{fig(217, 'Line sketches exploring six silhouettes', 'Explorations', 'xl')}{fig(218, 'Coloured line-up of six looks', 'Developed line-up', 'xl')}</section>
<section class="process cprocess"><p class="label">Design process — pleating, draped corset</p>
  <div class="cp">{fig(222, 'Corset panels pinned on a dress form', 'Draped corset on the form', 'l')}{fig(224, 'Pleated dark fabric', 'Pleating', 'm')}{fig(225, 'Corset and pleated skirt on the form', 'On the form', 'l')}</div></section>
<section class="illus invert"><p class="label">Final illustration</p>{img(226, 'Final illustration of the Contained collection', 'xl')}</section>''',
     f'''<section class="lookbook lb-ct"><p class="label">Lookbook — studio</p>
  <div class="cut">{''.join(img(n, 'Contained look, studio', 'm') for n in [231, 232, 233, 236, 238])}</div></section>
<section class="lookbook lb-loc"><p class="label">Lookbook — location</p>
  <div class="lb">{''.join(img(n, 'Contained look, location shoot', 'l') for n in [241, 235, 242, 243, 244, 229])}</div></section>''']) + proj_nav(('bleed-bloom.html', 'Bleed &amp; Bloom'), ('in-between.html', 'The In Between'))
page('contained.html', 'Contained — Padmabala S', 'Brand-based ready-to-wear collection for Haderlump, Berlin, 2025.', ct, '#364742', '#95AEAC')

# ---------- THE IN BETWEEN ----------
JACKET = [('Bust round', '38”'), ('Collar height', '4”'), ('Full length from HSP', '12.5”'), ('Full sleeve length', '29”'),
          ('HSP to elbow', '15”'), ('Shoulder to style line', '9”'), ('Wrist round', '11”')]
DRESS = [('Bust round', '32”'), ('Full length from HSP', '30”'), ('Waist round', '28”'), ('Hip round', '33”'),
         ('Tuck panel length', '4”'), ('Armhole length', '8”')]


def spec(title, rows, flats, trims, details):
    tr = ''.join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in rows)
    return f'''<article class="spec">
  <div class="spec-flats">{''.join(img(n, a, 'm') for n, a in flats)}</div>
  <div class="spec-txt"><p class="label">Season A/W 26 · Western · Size S · Style #AW26C9G5 · 27/05/25</p><h3>{title}</h3>
  <table><caption class="label">Measurements (size S)</caption>{tr}</table>
  <p class="label">Details — {details}</p><p class="label">Trims &amp; fabric — {trims}</p></div>
</article>'''


ib = opener(4, 'The In <em>Between</em>', 'Denim collection, AW 26/27', 2025, 246, 'Model in a navy denim look holding a web of red yarn',
            'Seeing is never just seeing.', '50% 40%') + case(
    [('Brief', 'Denim collection for AW 26/27'),
     ('Audience', 'Women, 18–30, urban youth, students and creative professionals'),
     ('Process', 'Trend research, form explorations, pin tucks, surface work, tech packs'),
     ('Outcome', 'Denim jacket and panelled dress with full specs, final shoot')],
    [f'''<section class="concept two">
  <div><p class="label">Concept</p><p class="big">There is always a moment in between, a gap between the eye receiving something and the mind making sense of it.</p></div>
  <div><p class="body">By the time it reaches the brain, what began as a simple image has already been quietly shaped into something personal. Something filtered through everything that person has ever felt or lived. The way perception is never neutral, never clean, never fully our own.</p>
  {img(250, 'Handwritten quote: We do not see things as they are, we see things as we are — Anaïs Nin', 's', 'quote-card')}</div>
</section>''',
     f'''<section class="trend">
  <div><p class="label">Client profile</p><p class="big">Trend-conscious and inclined toward experimental design.</p>
  <p class="body">Age 18–30 · Female · Urban cities · Upper-middle class to affluent. Urban youth, students and creative professionals who engage actively with streetwear culture, seek individuality, and are interested in content creation, fashion styling and functional aesthetics.</p>
  <p class="label">Trend research — AW 26/27</p><ul class="body ticks"><li>Details with contrast thread</li><li>Exaggerated sleeves</li><li>Machine embroidery</li><li>High neck collar</li></ul></div>
  <div class="trend-img">{''.join(img(n, 'Trend reference', 'm') for n in [263, 264, 265, 266])}</div>
</section>
<section class="mood invert">
  <div class="poem"><p class="label">Mood</p><p class="big">Tense and intimate. The feeling of being too conscious of your own seeing, aware of the machinery behind the eye, the noise behind the thought. Unsettled, but quietly so.</p>
  <p class="label words">Fragmented vision · The unseen self · Interpreted · Emotional void</p>
  {chips([('Neon Navy', '20-0142 TPM', chip_hex(255)), ('Space Cherry', '20-0075 TPM', chip_hex(256))])}</div>
  <div class="mood-grid">{''.join(fig(n, a, '', 'm') for n, a in [(249, 'Mood reference: portrait drawn over with red and blue thread lines'), (257, 'Mood reference: red thread embroidery sketch'), (254, 'Mood reference: collaged eye'), (258, 'Mood reference: ink burst on a plate')])}</div>
</section>''',
     f'''<section class="sil"><p class="label">Form &amp; silhouette explorations</p>{fig(267, 'Pencil line-up of silhouette explorations', 'Line-up explorations', 'xl')}{fig(268, 'Line studies of collar and sleeve forms', 'Form studies', 'xl')}</section>
<section class="range"><p class="label">Range plan</p><div class="cut">{''.join(img(n, 'Range plan illustration', 'm') for n in [219, 271, 272, 283])}</div></section>
<section class="process"><p class="label">Design process</p>
  <ol class="steps">{''.join(f'<li><span class="label">{i + 1:02d} / {t}</span>{img(n, t, "m")}</li>' for i, (n, t) in enumerate([(277, 'Pin tucks &amp; asymmetrical panel'), (282, 'Surface work'), (280, 'Pointy, structured sleeve'), (278, 'Adjust strap'), (279, 'Final garment')]))}</ol></section>
<section class="specs"><p class="label">Technical flats &amp; specs</p>
  {spec('Denim jacket with raglan sleeve', JACKET, [(294, 'Technical flat, jacket front'), (297, 'Technical flat, jacket back')], 'navy blue denim, metal railroad zipper, sewing thread', 'high neck collar, raglan sleeve, asymmetric panel, pointy and structured style line, cuff strap, separating zipper')}
  {spec('Denim panelled dress with tuck detail', DRESS, [(295, 'Technical flat, dress front'), (296, 'Technical flat, dress back')], 'navy blue denim, metal adjustable slide buckles, separating zipper, sewing thread', 'panels with flat-and-fell seams, tuck detail, zipper')}
  <div class="trims">{''.join(img(n, a, 's') for n, a in [(290, 'Navy denim swatch'), (288, 'Metal railroad zipper'), (289, 'Separating zipper'), (286, 'Metal slide buckle'), (285, 'Navy sewing thread'), (287, 'Red thread')])}</div>
</section>''',
     f'''<section class="lookbook lb-ib"><p class="label">Lookbook</p>
  <div class="lb">{''.join(img(n, 'The In Between look', 'l') for n in [307, 308, 305, 309, 304, 310])}</div>
  <div class="cut">{''.join(img(n, 'The In Between look, studio', 'm') for n in [298, 299, 300, 301])}</div></section>''']) + proj_nav(('contained.html', 'Contained'), None)
page('in-between.html', 'The In Between — Padmabala S', 'Denim collection, AW 26/27, with technical flats and specs.', ib, '#990213', '#E0606A')

total = sum(os.path.getsize(os.path.join(OUT_IMG, f)) for f in os.listdir(OUT_IMG))
print(f'{len(_done)} images, {total / 1e6:.1f} MB')
assert total < 40e6, 'image payload too large'
