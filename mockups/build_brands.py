#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""brands.html — страница производителей (вариант A, плитка)."""
import html
import json
import os
import re

import build as home

HERE = os.path.dirname(os.path.abspath(__file__))
CAT = json.load(open(os.path.join(HERE, 'data', 'catalog.json'), encoding='utf-8'))
MANS = json.load(open(os.path.join(HERE, 'data', 'manufacturers.json'), encoding='utf-8'))

CAT_NAMES = {c['slug']: c['name'] for c in home.CATS}
CAT_NAMES.update({s: n for s, n, _ in home.OTHER_CATS})

LOGO = {
    'nord': 'nord', 'Motovario': 'motovario', 'brevini': 'brevini', 'bondioli_pavesi': 'bondioli',
    'tambov_polimer': 'tambovpolimermash', 'ChelyabinskReduktor': 'chzr',
    'mogilev_electrodvig': 'mze', 'pskovskii_privod': 'pzmp', 'SEW_Eurodrive': 'sew',
}


def esc(s):
    return html.escape(s or '', quote=True)


def clean_desc(text):
    text = re.sub(r'^Подробнее о производителе\s*', '', text or '')
    text = re.sub(r'\.(?=[А-ЯЁA-Z])', '. ', text)   # «времени.С 1931» → «времени. С 1931»
    return re.sub(r'\s+', ' ', text).strip()


brands = []
for slug, m in MANS.items():
    prods = [r for r in CAT if r.get('maker_slug') == slug]
    cats = {}
    for p in prods:
        cats[p['catslug']] = cats.get(p['catslug'], 0) + 1
    top = sorted(cats.items(), key=lambda kv: -kv[1])[:3]
    raw = clean_desc((m.get('desc') or [''])[0])
    short = raw
    if len(raw) > 170:
        short = raw[:170].rsplit(' ', 1)[0].rstrip('.,;:') + '…'
    brands.append(dict(slug=slug, name=m['name'], logo='assets/img/brands/%s.png' % LOGO.get(slug, 'nord'),
                       n=len(prods), cats=[(CAT_NAMES.get(c, c), k) for c, k in top], short=short))
brands.sort(key=lambda b: -b['n'])
TOTAL = sum(b['n'] for b in brands)


def card(b):
    chips = ''.join('<span class="bep-chip">%s <i>%d</i></span>' % (esc(n), c) for n, c in b['cats'])
    if b['n'] == 0:
        return f"""
      <a class="bep-brandcard bep-brandcard--empty" href="catalog.html?maker={esc(b['slug'])}"
         data-name="{esc(b['name'].lower())}">
        <span class="bep-brandcard-logo"><img src="{b['logo']}" alt="{esc(b['name'])}" loading="lazy"></span>
        <h3 class="bep-brandcard-name">{esc(b['name'])}</h3>
        <p class="bep-brandcard-desc">{esc(b['short'] or 'Поставка под заказ по запросу.')}</p>
        <span class="bep-brandcard-chips"><span class="bep-chip">под заказ</span></span>
        <span class="bep-brandcard-foot"><span>нет позиций в каталоге</span>
          <span class="bep-brandcard-go">Запросить <span>→</span></span></span>
      </a>"""
    return f"""
      <a class="bep-brandcard" href="catalog.html?maker={esc(b['slug'])}" data-name="{esc(b['name'].lower())}">
        <span class="bep-brandcard-logo"><img src="{b['logo']}" alt="{esc(b['name'])}" loading="lazy"></span>
        <h3 class="bep-brandcard-name">{esc(b['name'])}</h3>
        <p class="bep-brandcard-desc">{esc(b['short'] or 'Официальные поставки и подбор под задачу.')}</p>
        <span class="bep-brandcard-chips">{chips}</span>
        <span class="bep-brandcard-foot"><span><b>{b['n']}</b> {home.plural(b['n'], 'модель', 'модели', 'моделей')}</span>
          <span class="bep-brandcard-go">Смотреть товары <span>→</span></span></span>
      </a>"""


def page():
    def fix(t):
        t = t.replace('href="catalog.html', 'href="catalog.html')
        t = t.replace('href="#brands"', 'href="brands.html"')
        return t

    header = fix(home.header()).replace('href="#', 'href="index.html#')
    header = header.replace('href="index.html#brands"', 'href="brands.html"')
    footer = fix(home.footer()).replace('href="#', 'href="index.html#')
    cards = ''.join(card(b) for b in brands)

    return f"""<!DOCTYPE html>
<html lang="ru" data-accent="teal">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Производители редукторов и приводов — 9 брендов | БелЕвропривод</title>
<meta name="description" content="Производители приводной техники, с которыми работает БелЕвропривод: NORD, Motovario, Brevini, Bondioli & Pavesi, ЧЗР, Тамбовполимермаш и другие. 172 модели в каталоге.">
<link rel="preload" href="assets/media/manrope/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/00-swiper-bundle.css">
<link rel="stylesheet" href="assets/css/01-fonts.css">
<link rel="stylesheet" href="assets/css/02-bootstrap.css">
<link rel="stylesheet" href="assets/css/03-fontawesome.css">
<link rel="stylesheet" href="assets/css/05-swiper-icons.css">
<link rel="stylesheet" href="assets/css/06-theme.css">
<link rel="stylesheet" href="assets/css/bep.css">
<link rel="stylesheet" href="assets/css/header.css">
<link rel="stylesheet" href="assets/css/mega.css">
</head>
<body class="bep-catalog-page">
{header}
<main>
  <section class="bep-hero1">
    <div class="container">
      <div class="bep-hero1-inner">
        <div>
          <nav class="bep-hero1-crumbs" aria-label="Хлебные крошки">
            <a href="index.html">Главная</a><i class="tji-arrow-right-long"></i><span>Производители</span>
          </nav>
          <span class="bep-kicker"><i class="tji-team"></i> {len(brands)} {home.plural(len(brands), 'бренд', 'бренда', 'брендов')} · {TOTAL} {home.plural(TOTAL, 'модель', 'модели', 'моделей')}</span>
          <h1 class="bep-hero1-title">Бренды, с которыми<br><span>мы работаем.</span></h1>
          <div class="bep-hero1-row">
            <a class="bep-hero1-link" href="#bep-brands-grid" aria-label="К брендам">
              <i class="tji-arrow-down-long"></i>
            </a>
            <span class="bep-hero1-div"></span>
            <p class="bep-hero1-desc">Европейские и белорусско-российские заводы: мотор-редукторы, приводы
              для сельхозтехники, электродвигатели. Подбираем аналог, если модели нет в наличии.</p>
          </div>
        </div>
        <div class="bep-hero1-media">
          <img src="assets/img/hero/slide-2.jpg" alt="Производство приводной техники">
          <div class="bep-hero1-card">
            <div><b>{TOTAL}</b><span>{home.plural(TOTAL, 'модель', 'модели', 'моделей')} у {len(brands)} брендов</span></div>
            <div class="bep-hero1-thumbs">
              <img src="assets/img/brands/nord.png" alt="">
              <img src="assets/img/brands/motovario.png" alt="">
              <img src="assets/img/brands/chzr.png" alt="">
            </div>
          </div>
        </div>
      </div>
      <a class="bep-hero1-scroll" href="#bep-brands-grid">Смотреть бренды <i class="tji-arrow-down"></i></a>
    </div>
  </section>

  <section class="bep-brands section-gap" id="bep-brands-grid">
    <div class="container">
      <div class="bep-brands-head">
        <div>
          <h2 class="bep-brands-title">Производители</h2>
          <p class="bep-brands-sub" id="bep-brands-count">Показано {len(brands)} из {len(brands)} брендов</p>
        </div>
        <label class="bep-brands-search">
          <i class="tji-search"></i>
          <input type="search" id="bep-brands-q" placeholder="Найти бренд: NORD, Motovario…" autocomplete="off">
        </label>
      </div>

      <div class="bep-brands-grid" id="bep-brands">{cards}</div>

      <div class="bep-empty" id="bep-brands-empty" hidden>
        <h3>Такого бренда нет в списке</h3>
        <p>Мы работаем с 15 поставщиками — напишите, подберём аналог или привезём под заказ.</p>
        <a class="tj-primary-btn" href="index.html#contacts"><span class="btn-text"><span>Отправить запрос</span></span>
          <span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
      </div>
    </div>
  </section>
</main>
{footer}
{home.overlays()}
<script>window.BEP_PRODUCTS = {home.search_index()};</script>
<script src="assets/js/swiper-bundle.min.js"></script>
<script src="assets/js/main.js"></script>
<script>
(function () {{
  var q = document.getElementById('bep-brands-q');
  var cards = [].slice.call(document.querySelectorAll('.bep-brandcard'));
  var count = document.getElementById('bep-brands-count');
  var empty = document.getElementById('bep-brands-empty');
  var total = cards.length;
  if (!q) return;
  q.addEventListener('input', function () {{
    var v = q.value.trim().toLowerCase();
    var shown = 0;
    cards.forEach(function (c) {{
      var ok = !v || (c.getAttribute('data-name') || '').indexOf(v) > -1;
      c.hidden = !ok;
      if (ok) shown++;
    }});
    count.textContent = 'Показано ' + shown + ' из ' + total + ' брендов';
    empty.hidden = shown !== 0;
  }});
}})();
</script>
</body>
</html>
"""


if __name__ == '__main__':
    out = os.path.join(HERE, 'brands.html')
    open(out, 'w', encoding='utf-8').write(page())
    print('written', out)
