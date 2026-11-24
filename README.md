# Padmabala S — Fashion Design Portfolio

Interactive portfolio website for Padmabala S, B.Des Fashion Design (Heritage & Couture), NIFT Jodhpur, 2023–2027.

Static HTML/CSS/JS — no framework, no build step needed to view. Open `index.html` or serve the folder:

```
python -m http.server 8765
```

## Pages

- `index.html` — home: hero, statement, four collections, recognition
- `info.html` — about, education, achievements, skills, software, languages
- `raw.html`, `bleed-bloom.html`, `contained.html`, `in-between.html` — case studies, each in four chapters:
  01 Brief · 02 Audience & research · 03 Ideation & process · 04 Execution & impact

## Interactions

Slide-down menu, scroll-lit statements, collection image swatches, sticky chapter navigation with scrollspy,
keyboard-accessible lightbox (arrow keys, Esc), reduced-motion support.

## Rebuilding

All images come from the original portfolio PDF. `tools/build.py` converts the extracted images to WebP
(`img/`) and writes every page:

```
python tools/build.py path/to/extracted/assets
```

The extracted source images are not in this repository.
