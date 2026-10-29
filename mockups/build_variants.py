#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""variants.html — варианты страницы брендов и страницы поставщика (для выбора)."""
import html
import json
import os
import re

import build as home

HERE = os.path.dirname(os.path.abspath(__file__))
CAT = json.load(open(os.path.join(HERE, 'data', 'catalog.json'), encoding='utf-8'))
MANS = json.load(open(os.path.join(HERE, 'data', 'manufacturers.json'), encoding='utf-8'))

LOGO = {
    'nord': 'nord', 'Motovario': 'motovario', 'brevini': 'brevini', 'bondioli_pavesi': 'bondioli',
    'tambov_polimer': 'tambovpolimermash', 'ChelyabinskReduktor': 'chzr',
    'mogilev_electrodvig': 'mze', 'pskovskii_privod': 'pzmp', 'SEW_Eurodrive': 'sew',
}
CAT_NAMES = {c['slug']: c['name'] for c in home.CATS}
CAT_NAMES.update({s: n for s, n, _ in home.OTHER_CATS})


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
    top_cats = sorted(cats.items(), key=lambda kv: -kv[1])[:3]
    raw = clean_desc((m.get('desc') or [''])[0])
    desc = raw
    if len(raw) > 300:
        cut = raw[:300].rsplit(' ', 1)[0]
        desc = cut.rstrip('.,;:') + '…'
    brands.append(dict(
        slug=slug, name=m['name'], logo='assets/img/brands/%s.png' % LOGO.get(slug, 'nord'),
        n=len(prods), cats=[(CAT_NAMES.get(c, c), k) for c, k in top_cats],
        desc=desc, short=desc[:150].rsplit(' ', 1)[0] + '…' if len(desc) > 150 else desc,
        products=prods,
    ))
brands.sort(key=lambda b: -b['n'])
HERO = ['assets/img/hero/slide-1.jpg', 'assets/img/hero/slide-2.jpg', 'assets/img/hero/slide-3.jpg']


def label(letter, title, sub):
    return ('<div class="vlabel"><span class="vletter">%s</span><b>%s</b><span class="vsub">%s</span></div>'
            % (letter, title, sub))


def cats_chips(b):
    return ''.join('<span class="v-chip">%s <i>%d</i></span>' % (esc(n), c) for n, c in b['cats'])


# ---------------------------------------------------------------- A. плитка
def variant_a():
    cards = ''.join(f"""
      <a class="v-brand" href="#">
        <span class="v-brand-logo"><img src="{b['logo']}" alt="{esc(b['name'])}" loading="lazy"></span>
        <b class="v-brand-name">{esc(b['name'])}</b>
        <span class="v-brand-desc">{esc(b['short'] or 'Официальные поставки и подбор под задачу.')}</span>
        <span class="v-chips">{cats_chips(b)}</span>
        <span class="v-brand-foot"><i>{b['n']} моделей</i><em>Смотреть товары <span>→</span></em></span>
      </a>""" for b in brands)
    return label('A', 'Плитка', 'сетка карточек 3 в ряд') + \
        f'<div class="v-wrap v-grid3">{cards}</div>'


# ---------------------------------------------------------------- B. строки
def variant_b():
    rows = ''.join(f"""
      <a class="v-row" href="#">
        <span class="v-row-logo"><img src="{b['logo']}" alt="{esc(b['name'])}" loading="lazy"></span>
        <span class="v-row-main">
          <b>{esc(b['name'])}</b>
          <span class="v-row-desc">{esc(b['short'] or '')}</span>
          <span class="v-chips">{cats_chips(b)}</span>
        </span>
        <span class="v-row-num"><b>{b['n']}</b><i>моделей</i></span>
        <span class="v-row-go">→</span>
      </a>""" for b in brands)
    return label('B', 'Строки', 'плотный список, как в снабжении') + \
        f'<div class="v-wrap v-rows">{rows}</div>'


# ---------------------------------------------------------------- C. витрина
def variant_c():
    cards = ''
    for i, b in enumerate(brands[:6]):
        cards += f"""
      <a class="v-show" href="#">
        <span class="v-show-bg" style="background-image:url('{HERO[i % 3]}')"></span>
        <span class="v-show-inner">
          <span class="v-show-logo"><img src="{b['logo']}" alt="{esc(b['name'])}" loading="lazy"></span>
          <span class="v-show-text">
            <b>{esc(b['name'])}</b>
            <span>{b['n']} моделей · {len(b['cats'])} категории</span>
          </span>
          <span class="v-show-go">→</span>
        </span>
      </a>"""
    return label('C', 'Витрина', 'крупные карточки с фото производства') + \
        f'<div class="v-wrap v-grid2">{cards}</div>'


# ---------------------------------------------------------------- D. страница бренда
def variant_d():
    b = next(x for x in brands if x['slug'] == 'nord')
    prods = b['products'][:4] or CAT[:4]
    cards = ''.join(f"""
        <a class="bep-card bep-pcard" href="#">
          <span class="bep-card-img"><img src="assets/img/products/{p.get('slug_safe', p['slug'])}.jpg" alt="{esc(p['h1'])}" loading="lazy"></span>
          <span class="bep-card-body">
            <span class="bep-card-cat">{esc(CAT_NAMES.get(p['catslug'], ''))}</span>
            <b class="bep-card-name">{esc(p['h1'])}</b>
            <span class="bep-pcard-maker">{esc(b['name'])}</span>
          </span>
        </a>""" for p in prods)
    tabs = ''.join('<button class="v-tab%s">%s <i>%d</i></button>' % (' is-active' if i == 0 else '', esc(n), c)
                   for i, (n, c) in enumerate(b['cats']))
    return label('D', 'Страница поставщика — «классика»', 'тёмная шапка с логотипом, описание + факты, товары') + f"""
    <div class="v-wrap">
      <div class="v-brandhead">
        <span class="v-brandhead-bg" style="background-image:url('{HERO[1]}')"></span>
        <div class="v-brandhead-inner">
          <span class="v-brandhead-logo"><img src="{b['logo']}" alt="{esc(b['name'])}"></span>
          <div>
            <div class="v-crumbs">Главная → Производители → {esc(b['name'])}</div>
            <h2 class="v-brandhead-title">{esc(b['name'])}</h2>
            <div class="v-brandhead-stats">
              <span><b>{b['n']}</b> моделей</span><span><b>{len(b['cats'])}</b> категории</span>
              <span><b>9</b> поставщиков</span><span><b>15</b> лет на рынке</span>
            </div>
          </div>
        </div>
      </div>
      <div class="v-brandbody">
        <div class="v-brandtext">
          <h3>О производителе</h3>
          <p>{esc(b['desc'])}</p>
          <h3>Что поставляем</h3>
          <p>Мотор-редукторы, электродвигатели и приводная электроника NORD: цилиндрические соосные,
             коническо-цилиндрические и с параллельными валами. Подбор по моменту и оборотам, аналоги
             снятых серий, склад в Минске.</p>
        </div>
        <div class="v-facts">
          <div><b>{b['n']}</b><span>моделей в каталоге</span></div>
          <div><b>{len(b['cats'])}</b><span>категории</span></div>
          <div><b>1–3 дня</b><span>срок поставки со склада</span></div>
          <a class="tj-primary-btn" href="#"><span class="btn-text"><span>Запросить прайс</span></span>
            <span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
        </div>
      </div>
      <div class="v-tabs">{tabs}<button class="v-tab">Все товары <i>{b['n']}</i></button></div>
      <div class="v-pgrid">{cards}</div>
    </div>"""


# ---------------------------------------------------------------- E. компакт
def variant_e():
    b = next(x for x in brands if x['slug'] == 'Motovario')
    prods = b['products'][:6]
    cards = ''.join(f"""
        <a class="bep-card bep-pcard" href="#">
          <span class="bep-card-img"><img src="assets/img/products/{p.get('slug_safe', p['slug'])}.jpg" alt="{esc(p['h1'])}" loading="lazy"></span>
          <span class="bep-card-body">
            <span class="bep-card-cat">{esc(CAT_NAMES.get(p['catslug'], ''))}</span>
            <b class="bep-card-name">{esc(p['h1'])}</b>
            <span class="bep-pcard-maker">{esc(b['name'])}</span>
          </span>
        </a>""" for p in prods)
    side = ''.join('<li%s><span>%s</span><i>%d</i></li>' % (' class="is-active"' if i == 0 else '', esc(n), c)
                   for i, (n, c) in enumerate(b['cats']))
    return label('E', 'Страница поставщика — «компакт»', 'без баннера: шапка-строка, сайдбар, сразу товары') + f"""
    <div class="v-wrap">
      <div class="v-crumbs2">Главная → Производители → {esc(b['name'])}</div>
      <div class="v-compacthead">
        <span class="v-compact-logo"><img src="{b['logo']}" alt="{esc(b['name'])}"></span>
        <div class="v-compact-main">
          <h2>{esc(b['name'])}</h2>
          <p>{esc(b['short'])}</p>
          <div class="v-chips">{cats_chips(b)}</div>
        </div>
        <div class="v-compact-side">
          <b>{b['n']} моделей</b>
          <a class="tj-primary-btn" href="#"><span class="btn-text"><span>Запросить прайс</span></span>
            <span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
        </div>
      </div>
      <div class="v-split">
        <aside class="v-side">
          <h4>Категории бренда</h4>
          <ul>{side}</ul>
          <a class="v-side-link" href="#">Все производители →</a>
        </aside>
        <div class="v-pgrid v-pgrid--3">{cards}</div>
      </div>
    </div>"""


STYLE = """
<style>
  body.bep-variants { background: #f3f4f4; }
  .vhead { padding: 90px 0 26px; }
  .vhead h1 { font-size: 34px; margin: 0 0 8px; }
  .vhead p { color: var(--bep-muted); font-size: 15px; margin: 0; }
  .vsection { padding: 22px 0 40px; }
  .vlabel { display: flex; align-items: center; gap: 12px; margin: 0 0 14px; }
  .vletter { width: 34px; height: 34px; border-radius: 10px; background: var(--bep-ink); color: #fff;
    display: inline-flex; align-items: center; justify-content: center; font-weight: 700; font-size: 15px; }
  .vlabel b { font-size: 19px; }
  .vsub { font-size: 13px; color: var(--bep-muted); }
  .v-wrap { background: var(--tj-color-theme-bg); border-radius: 18px; padding: 24px; }

  /* A — плитка */
  .v-grid3 { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 16px; }
  .v-brand { display: flex; flex-direction: column; gap: 10px; background: #fff; border: 1px solid var(--bep-line);
    border-radius: 14px; padding: 18px; text-decoration: none; transition: .25s ease; }
  .v-brand:hover { border-color: var(--bep-accent); transform: translateY(-2px); box-shadow: 0 16px 32px rgb(12 30 33 / .08); }
  .v-brand-logo { height: 84px; display: flex; align-items: center; justify-content: flex-start; }
  .v-brand-logo img { max-width: 62%; max-height: 100%; object-fit: contain; }
  .v-brand-name { font-size: 17px; color: var(--bep-text); }
  .v-brand-desc { font-size: 13px; line-height: 1.5; color: var(--bep-muted); min-height: 58px; }
  .v-chips { display: flex; flex-wrap: wrap; gap: 6px; }
  .v-chip { font-size: 11.5px; padding: 5px 10px; border-radius: 20px; background: var(--bep-sand); color: var(--tj-color-text-body); }
  .v-chip i { font-style: normal; opacity: .55; }
  .v-brand-foot { display: flex; align-items: center; justify-content: space-between; margin-top: auto; padding-top: 10px;
    border-top: 1px solid var(--bep-line); font-size: 12.5px; }
  .v-brand-foot i { font-style: normal; color: var(--bep-muted); }
  .v-brand-foot em { font-style: normal; font-weight: 700; color: var(--bep-accent-dark); }

  /* B — строки */
  .v-rows { display: flex; flex-direction: column; gap: 8px; }
  .v-row { display: grid; grid-template-columns: 132px 1fr 108px 28px; align-items: center; gap: 18px;
    background: #fff; border: 1px solid var(--bep-line); border-radius: 12px; padding: 14px 18px; text-decoration: none; transition: .2s; }
  .v-row:hover { border-color: var(--bep-accent); }
  .v-row-logo { height: 56px; display: flex; align-items: center; }
  .v-row-logo img { max-width: 100%; max-height: 100%; object-fit: contain; }
  .v-row-main { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
  .v-row-main b { font-size: 15.5px; color: var(--bep-text); }
  .v-row-desc { font-size: 12.5px; color: var(--bep-muted); overflow: hidden; display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; }
  .v-row-num { text-align: right; }
  .v-row-num b { display: block; font-size: 22px; line-height: 1; color: var(--bep-text); }
  .v-row-num i { font-style: normal; font-size: 11px; color: var(--bep-muted); }
  .v-row-go { font-size: 18px; color: var(--bep-accent); text-align: right; }

  /* C — витрина */
  .v-grid2 { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 16px; }
  .v-show { position: relative; display: block; height: 190px; border-radius: 16px; overflow: hidden; text-decoration: none; }
  .v-show-bg { position: absolute; inset: 0; background-size: cover; background-position: 50% 45%; }
  .v-show-bg:after { content: ''; position: absolute; inset: 0; background: linear-gradient(180deg, rgb(var(--bep-ink-rgb)/.25), rgb(var(--bep-ink-rgb)/.85)); }
  .v-show-inner { position: absolute; inset: auto 0 0 0; padding: 18px 20px; display: flex; align-items: center; gap: 14px; }
  .v-show-logo { width: 62px; height: 62px; border-radius: 12px; background: #fff; display: flex; align-items: center; justify-content: center; padding: 10px; flex: none; }
  .v-show-logo img { max-width: 100%; max-height: 100%; object-fit: contain; }
  .v-show-text { display: flex; flex-direction: column; gap: 3px; }
  .v-show-text b { color: #fff; font-size: 17px; }
  .v-show-text span { color: rgba(255,255,255,.72); font-size: 12.5px; }
  .v-show-go { margin-left: auto; color: #fff; font-size: 20px; }

  /* D — бренд «классика» */
  .v-brandhead { position: relative; border-radius: 16px; overflow: hidden; min-height: 210px; display: flex; align-items: center; }
  .v-brandhead-bg { position: absolute; inset: 0; background-size: cover; background-position: 50% 50%; }
  .v-brandhead-bg:after { content: ''; position: absolute; inset: 0; background: linear-gradient(90deg, rgb(var(--bep-ink-rgb)/.94), rgb(var(--bep-ink-rgb)/.62)); }
  .v-brandhead-inner { position: relative; z-index: 2; display: flex; align-items: center; gap: 24px; padding: 32px; }
  .v-brandhead-logo { width: 120px; height: 120px; border-radius: 16px; background: #fff; display: flex; align-items: center; justify-content: center; padding: 16px; flex: none; }
  .v-brandhead-logo img { max-width: 100%; max-height: 100%; object-fit: contain; }
  .v-crumbs { font-size: 12px; color: rgba(255,255,255,.6); margin-bottom: 8px; }
  .v-brandhead-title { color: #fff; font-size: 34px; margin: 0 0 12px; }
  .v-brandhead-stats { display: flex; gap: 26px; flex-wrap: wrap; }
  .v-brandhead-stats span { color: rgba(255,255,255,.7); font-size: 12.5px; }
  .v-brandhead-stats b { display: block; color: #fff; font-size: 22px; line-height: 1.1; }
  .v-brandbody { display: grid; grid-template-columns: 1fr 300px; gap: 24px; padding: 24px 0 8px; }
  .v-brandtext h3 { font-size: 17px; margin: 0 0 8px; }
  .v-brandtext p { font-size: 14px; line-height: 1.65; color: var(--tj-color-text-body); margin: 0 0 18px; }
  .v-facts { background: #fff; border: 1px solid var(--bep-line); border-radius: 14px; padding: 20px; display: grid; gap: 14px; align-content: start; }
  .v-facts div b { display: block; font-size: 22px; color: var(--bep-text); }
  .v-facts div span { font-size: 12.5px; color: var(--bep-muted); }
  .v-facts .tj-primary-btn { justify-content: center; margin-top: 4px; }
  .v-tabs { display: flex; gap: 10px; flex-wrap: wrap; margin: 10px 0 16px; }
  .v-tab { border: 1px solid var(--bep-line); background: #fff; border-radius: 40px; padding: 9px 16px; font-size: 13px;
    color: var(--tj-color-text-body); cursor: pointer; font-family: var(--tj-ff-body); }
  .v-tab.is-active { background: var(--bep-accent); border-color: var(--bep-accent); color: #fff; }
  .v-tab i { font-style: normal; opacity: .6; }
  .v-pgrid { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 14px; }
  .v-pgrid--3 { grid-template-columns: repeat(3, minmax(0,1fr)); }

  /* E — компакт */
  .v-crumbs2 { font-size: 12.5px; color: var(--bep-muted); margin-bottom: 12px; }
  .v-compacthead { display: flex; align-items: center; gap: 20px; background: #fff; border: 1px solid var(--bep-line);
    border-radius: 16px; padding: 20px 22px; margin-bottom: 18px; }
  .v-compact-logo { width: 96px; height: 72px; display: flex; align-items: center; justify-content: center; flex: none; }
  .v-compact-logo img { max-width: 100%; max-height: 100%; object-fit: contain; }
  .v-compact-main h2 { font-size: 24px; margin: 0 0 6px; }
  .v-compact-main p { font-size: 13px; line-height: 1.5; color: var(--bep-muted); margin: 0 0 8px; max-width: 560px; }
  .v-compact-side { margin-left: auto; display: flex; flex-direction: column; align-items: flex-end; gap: 8px; }
  .v-compact-side b { font-size: 15px; color: var(--bep-text); }
  .v-split { display: grid; grid-template-columns: 240px 1fr; gap: 18px; }
  .v-side { background: #fff; border: 1px solid var(--bep-line); border-radius: 14px; padding: 18px; align-self: start; }
  .v-side h4 { font-size: 14px; margin: 0 0 12px; }
  .v-side ul { list-style: none; margin: 0 0 12px; padding: 0; display: grid; gap: 4px; }
  .v-side li { display: flex; justify-content: space-between; gap: 10px; padding: 7px 8px; border-radius: 8px; font-size: 13px; color: var(--tj-color-text-body); }
  .v-side li.is-active, .v-side li:hover { background: var(--bep-sand); color: var(--bep-accent-dark); }
  .v-side li i { font-style: normal; color: var(--bep-muted); font-size: 12px; }
  .v-side-link { font-size: 12.5px; color: var(--bep-accent-dark); font-weight: 700; text-decoration: none; }

  @media (max-width: 1199px) {
    .v-grid3 { grid-template-columns: repeat(2, minmax(0,1fr)); }
    .v-brandbody { grid-template-columns: 1fr; }
    .v-pgrid, .v-pgrid--3 { grid-template-columns: repeat(2, minmax(0,1fr)); }
    .v-split { grid-template-columns: 1fr; }
  }
  @media (max-width: 767px) {
    .v-grid3, .v-grid2, .v-row { grid-template-columns: 1fr; }
    .v-row { grid-template-columns: 90px 1fr; }
    .v-row-num, .v-row-go { display: none; }
    .v-brandhead-inner { flex-direction: column; align-items: flex-start; }
    .v-compacthead { flex-direction: column; align-items: flex-start; }
    .v-compact-side { align-items: flex-start; }
  }
</style>
"""

page = f"""<!DOCTYPE html>
<html lang="ru" data-accent="teal">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Варианты: страница брендов и страница поставщика | БелЕвропривод</title>
<link rel="stylesheet" href="assets/css/00-swiper-bundle.css">
<link rel="stylesheet" href="assets/css/01-fonts.css">
<link rel="stylesheet" href="assets/css/02-bootstrap.css">
<link rel="stylesheet" href="assets/css/03-fontawesome.css">
<link rel="stylesheet" href="assets/css/05-swiper-icons.css">
<link rel="stylesheet" href="assets/css/06-theme.css">
<link rel="stylesheet" href="assets/css/bep.css">
<link rel="stylesheet" href="assets/css/header.css">
<link rel="stylesheet" href="assets/css/mega.css">
{STYLE}
</head>
<body class="bep-catalog-page bep-variants">
<main>
  <div class="container vhead">
    <h1>Страница брендов и страница поставщика — варианты</h1>
    <p>Три варианта списка производителей (A, B, C) и два варианта страницы бренда (D, E). Данные настоящие:
       9 производителей, привязанные товары, описания с сайта.</p>
  </div>
  <div class="container vsection">{variant_a()}</div>
  <div class="container vsection">{variant_b()}</div>
  <div class="container vsection">{variant_c()}</div>
  <div class="container vsection">{variant_d()}</div>
  <div class="container vsection">{variant_e()}</div>
</main>
</body>
</html>
"""

if __name__ == '__main__':
    out = os.path.join(HERE, 'variants.html')
    open(out, 'w', encoding='utf-8').write(page)
    print('written', out, len(page))
