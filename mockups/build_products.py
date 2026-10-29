#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генератор карточек товаров: product/<slug>.html — по мотивам Bexon /shop/1."""
import html
import json
import os
import re
from urllib.parse import quote

import build as home
import tags_data

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = home.SITE
CAT = json.load(open(os.path.join(HERE, 'data', 'catalog.json'), encoding='utf-8'))
DET = json.load(open(os.path.join(HERE, 'data', 'details.json'), encoding='utf-8'))
OUT = os.path.join(HERE, 'product')
os.makedirs(OUT, exist_ok=True)

CAT_NAMES = dict({c['slug']: c['name'] for c in home.CATS})
CAT_NAMES.update({s: n for s, n, _ in home.OTHER_CATS})

OWN_BRAND = 'БелЕвропривод'


def esc(s):
    return html.escape(s or '', quote=True)


def lead(desc_html, limit=230):
    """Первый абзац описания без тегов, обрезанный по границе слова."""
    m = re.search(r'<p[^>]*>(.*?)</p>', desc_html or '', re.S)
    text = re.sub(r'<[^>]+>', '', m.group(1) if m else (desc_html or ''))
    text = html.unescape(re.sub(r'\s+', ' ', text)).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(' ', 1)[0]
    return cut.rstrip('.,;:') + '…'


def spec_tables(tables):
    out = []
    for t in tables:
        head = t.get('head') or []
        rows = t.get('rows') or []
        if not rows:
            continue
        ths = ''.join('<th>%s</th>' % esc(c) for c in head) if head else ''
        trs = ''
        for r in rows:
            trs += '<tr>%s</tr>' % ''.join('<td>%s</td>' % esc(c) for c in r)
        out.append('<div class="bep-table-wrap"><table class="bep-spec-table">%s<tbody>%s</tbody></table></div>'
                   % (('<thead><tr>%s</tr></thead>' % ths) if ths else '', trs))
    return ''.join(out)


def gallery(r, d):
    imgs = ['../assets/img/products/%s.jpg' % r.get('slug_safe', r['slug'])]
    if d.get('drawing_local'):
        p = d['drawing_local']
        if not os.path.exists(p):
            base = re.sub(r'[^A-Za-z0-9_-]+', '-', os.path.basename(p).rsplit('.', 1)[0]).strip('-') + '.jpg'
            alt = os.path.join(os.path.dirname(p), base)
            if os.path.exists(alt):
                p = alt
        imgs.append('../' + p)
    main = imgs[0]
    thumbs = ''.join(
        '<button type="button" class="bep-gthumb%s" data-src="%s"><img src="%s" alt=""></button>'
        % (' is-active' if i == 0 else '', esc(u), esc(u))
        for i, u in enumerate(imgs))
    return f"""
        <div class="bep-gallery">
          <div class="bep-gallery-main"><img id="bep-gmain" src="{esc(main)}" alt="{esc(r['h1'])}"></div>
          <div class="bep-gallery-thumbs">{thumbs}</div>
        </div>"""


def page(r):
    d = DET.get(r['slug'], {})
    cat = CAT_NAMES.get(r['catslug'], r.get('cat') or '')
    maker = r.get('maker') or OWN_BRAND
    tags = []
    for t in (r.get('tags') or []):
        lab = tags_data.short_of(t)
        if lab and lab not in tags:
            tags.append(lab)
    tags = tags[:4]

    desc_html = d.get('desc_html') or ''
    tables_html = spec_tables(d.get('tables') or [])
    docs = d.get('docs') or []
    docs_html = ''.join(
        '<a class="bep-doc" href="%s" target="_blank" rel="noopener">'
        '<i class="tji-envelop"></i><span>%s</span><i class="tji-arrow-right-long"></i></a>'
        % (esc(x['url']), esc(x['label'])) for x in docs)

    tabs = []
    panes = []
    if desc_html:
        tabs.append(('desc', 'Описание', True))
        panes.append(('desc', desc_html, True))
    if tables_html:
        tabs.append(('specs', 'Характеристики', not tabs))
        panes.append(('specs', tables_html, not panes))
    if docs_html:
        tabs.append(('docs', 'Документация', not tabs))
        panes.append(('docs', docs_html, not panes))

    tabs_html = ''.join(
        '<button type="button" class="bep-tab%s" data-tab="%s">%s</button>'
        % (' is-active' if active else '', key, label) for key, label, active in tabs)
    panes_html = ''.join(
        '<div class="bep-tabpane%s" id="pane-%s">%s</div>'
        % (' is-active' if active else '', key, body) for key, body, active in panes)

    # связанные товары из той же категории
    same = [x for x in CAT if x['catslug'] == r['catslug'] and x['slug'] != r['slug']][:4]
    related = ''.join(f"""
          <div class="bep-rel-col">
            <a class="bep-card bep-pcard" href="{x.get('slug_safe', x['slug'])}.html">
              <span class="bep-card-img"><img src="../assets/img/products/{x.get('slug_safe', x['slug'])}.jpg" alt="{esc(x['h1'])}" loading="lazy"></span>
              <span class="bep-card-body">
                <span class="bep-card-cat">{esc(CAT_NAMES.get(x['catslug'], ''))}</span>
                <b class="bep-card-name">{esc(x['h1'])}</b>
                <span class="bep-pcard-maker">{esc(x.get('maker') or OWN_BRAND)}</span>
              </span>
            </a>
          </div>""" for x in same)

    tags_html = ''.join('<a class="bep-tag" href="../catalog.html?tag=%s">%s</a>'
                        % (quote(t), esc(t)) for t in tags)

    return f"""<!DOCTYPE html>
<html lang="ru" data-accent="teal">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(r['h1'])} — купить в Минске | БелЕвропривод</title>
<meta name="description" content="{esc(lead(desc_html, 160) or r['h1'])}">
<link rel="stylesheet" href="../assets/css/00-swiper-bundle.css">
<link rel="stylesheet" href="../assets/css/01-fonts.css">
<link rel="stylesheet" href="../assets/css/02-bootstrap.css">
<link rel="stylesheet" href="../assets/css/03-fontawesome.css">
<link rel="stylesheet" href="../assets/css/05-swiper-icons.css">
<link rel="stylesheet" href="../assets/css/06-theme.css">
<link rel="stylesheet" href="../assets/css/bep.css">
<link rel="stylesheet" href="../assets/css/header.css">
<link rel="stylesheet" href="../assets/css/mega.css">
</head>
<body class="bep-catalog-page">
{HEADER}
<main>
  <section class="bep-pagehead bep-pagehead--slim">
    <div class="bep-pagehead-bg" style="background-image:url('../assets/img/hero/slide-2.jpg')"></div>
    <div class="container">
      <nav class="bep-crumbs" aria-label="Хлебные крошки">
        <a href="../index.html">Главная</a><i class="tji-arrow-right-long"></i>
        <a href="../catalog.html">Каталог</a><i class="tji-arrow-right-long"></i>
        <a href="../category/{r['catslug']}.html">{esc(cat)}</a><i class="tji-arrow-right-long"></i>
        <span>{esc(r['h1'])}</span>
      </nav>
    </div>
  </section>

  <section class="bep-product section-gap">
    <div class="container">
      <div class="row row-gap-4 align-items-start">
        <div class="col-lg-7">{gallery(r, d)}</div>
        <div class="col-lg-5">
          <div class="bep-product-info">
            <a class="bep-product-cat" href="../category/{r['catslug']}.html">{esc(cat)}</a>
            <h1 class="bep-product-title">{esc(r['h1'])}</h1>
            <p class="bep-product-lead">{esc(lead(desc_html))}</p>

            <div class="bep-product-price">
              <b>Цена по запросу</b>
              <span>Уточним наличие, сроки поставки и цену под объём</span>
            </div>

            <div class="bep-product-actions">
              <button type="button" class="tj-primary-btn" data-open-modal>
                <span class="btn-text"><span>Запросить цену</span></span>
                <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
              </button>
              <a class="bep-ghost-btn bep-ghost-btn--dark" href="{home.PHONE_HREF}">
                <i class="tji-phone"></i>{home.PHONE}
              </a>
            </div>

            <dl class="bep-product-meta">
              <div><dt>Артикул</dt><dd>{esc(r['slug'])}</dd></div>
              <div><dt>Производитель</dt><dd>{esc(maker)}</dd></div>
              <div><dt>Категория</dt><dd><a href="../category/{r['catslug']}.html">{esc(cat)}</a></dd></div>
              <div><dt>Наличие</dt><dd>Склад в Минске / под заказ</dd></div>
            </dl>
            {'<div class="bep-product-tags">' + tags_html + '</div>' if tags_html else ''}
          </div>
        </div>
      </div>

      <div class="bep-tabs-wrap">
        <div class="bep-tabs">{tabs_html}</div>
        <div class="bep-tabpanes">{panes_html}</div>
      </div>

      {f'''
      <div class="bep-related">
        <div class="bep-related-head">
          <h2 class="bep-related-title">Смотрите также</h2>
          <a class="bep-inline-link" href="../category/{r['catslug']}.html">Вся категория</a>
        </div>
        <div class="bep-related-grid">{related}</div>
      </div>''' if related else ''}
    </div>
  </section>

  <section class="bep-cta">
    <div class="container">
      <div class="bep-cta-inner">
        <div>
          <h2>Не уверены, что модель подойдёт?</h2>
          <p>Инженер подберёт редуктор по крутящему моменту, оборотам и монтажному исполнению — пришлите параметры оборудования.</p>
        </div>
        <div class="bep-cta-actions">
          <button type="button" class="tj-primary-btn" data-open-modal>
            <span class="btn-text"><span>Получить подбор</span></span>
            <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
          </button>
          <a class="bep-ghost-btn" href="mailto:{home.EMAIL}">{home.EMAIL}</a>
        </div>
      </div>
    </div>
  </section>
</main>
{FOOTER}
{OVERLAYS}
<script>window.BEP_PRODUCTS = {home.search_index('../')};</script>
<script src="../assets/js/swiper-bundle.min.js"></script>
<script src="../assets/js/main.js"></script>
<script src="../assets/js/product.js"></script>
</body>
</html>
"""


def fix(html_text, prefix='../'):
    """Превращает ссылки шапки/футера главной в относительные для /product/."""
    t = html_text
    t = t.replace('href="catalog.html', 'href="%scatalog.html' % prefix)
    t = t.replace('href="brands.html', 'href="%sbrands.html' % prefix)
    t = t.replace('href="tags.html', 'href="%stags.html' % prefix)
    t = t.replace('href="category/', 'href="%scategory/' % prefix)
    t = t.replace('href="product/', 'href="%sproduct/' % prefix)
    t = t.replace('href="#', 'href="%sindex.html#' % prefix)
    t = t.replace('href="%sindex.html#"' % prefix, 'href="#"')
    t = t.replace('src="assets/', 'src="%sassets/' % prefix)
    t = t.replace("url('assets/", "url('%sassets/" % prefix)
    t = t.replace('url(assets/', 'url(%sassets/' % prefix)
    return t


if __name__ == '__main__':
    globals().update(HEADER=fix(home.header()), FOOTER=fix(home.footer()), OVERLAYS=fix(home.overlays()))
    n = 0
    for r in CAT:
        open(os.path.join(OUT, r.get('slug_safe', r['slug']) + '.html'), 'w', encoding='utf-8').write(page(r))
        n += 1
    print('written', n, 'product pages')
