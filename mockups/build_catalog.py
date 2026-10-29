#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генератор catalog.html — страница каталога (листинг категорий) в дизайне Bexon /shop."""
import json
import os

import build as home
import tags_data

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = home.SITE
ROWS = json.load(open(os.path.join(HERE, 'data', 'catalog.json'), encoding='utf-8'))

TAG_LABELS = {
    'Редукторы и мотор-редукторы': 'Редукторы и мотор-редукторы',
    'Для сельскохозяйственной техники и оборудования': 'Сельхозтехника',
    'Машиностроение': 'Машиностроение',
    'Для конвейеров, станков, подъемников, мешалок и др....': 'Конвейеры и станки',
    'Для тяжелой, легкой и химической промышленности.': 'Тяжёлая, лёгкая и химическая пром.',
    'Пищевая промышленность': 'Пищевая промышленность',
    'Тяжелая и легкая промышленность': 'Тяжёлая и лёгкая промышленность',
    'Для коммунальной и дорожной техники': 'Коммунальная и дорожная техника',
    'Лесное хозяйство': 'Лесное хозяйство',
    'Добыча полезных ископаемых': 'Добыча полезных ископаемых',
    'Медицинское оборудование': 'Медицинское оборудование',
    'Конвейеры и другие транспортные системы': 'Конвейеры и транспортные системы',
    'Для башенных кранов, строительной техники, подъемников, буровой техники': 'Краны и стройтехника',
    'Для тяжелой, легкой и химической промышленности': 'Тяжёлая, лёгкая и химическая пром.',
    'Для коммунальной и дорожной техники.': 'Коммунальная и дорожная техника',
    'Тяжелая промышленность': 'Тяжёлая промышленность',
}

OWN_BRAND = ('own', 'БелЕвропривод')

# подписи тегов — из единого реестра (tags_data), включая серии и тип продукции
TAG_LABELS.update({t['full']: t['short'] for t in tags_data.TAGS})

# все отраслевые теги + серии/модели: попадают в data-tags карточек и в ссылки карточки товара
INDUSTRY_TAGS = {t['full'] for t in tags_data.INDUSTRY + tags_data.SERIES + tags_data.TYPE}

CAT_ORDER = [c['slug'] for c in home.CATS] + [s for s, _, _ in home.OTHER_CATS]
CAT_NAMES = dict({c['slug']: c['name'] for c in home.CATS})
CAT_NAMES.update({s: n for s, n, _ in home.OTHER_CATS})
CAT_IMAGES = {slug: 'assets/img/cat/%s.png' % slug for slug in CAT_NAMES}


def esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def norm_maker(r):
    slug = r.get('maker_slug') or ''
    name = r.get('maker') or ''
    if not slug:
        return OWN_BRAND
    return (slug, name)


def short_tag(t):
    return TAG_LABELS.get(t, t)


# ---------------------------------------------------------------- подготовка данных
for r in ROWS:
    r['_maker'] = norm_maker(r)
    r['_img'] = 'assets/img/products/%s.jpg' % r.get('slug_safe', r['slug'])
    r['_tags'] = sorted({s for s in (tags_data.short_of(t) for t in (r.get('tags') or [])) if s})

cat_counts = {}
maker_counts = {}
tag_counts = {}
for r in ROWS:
    cat_counts[r['catslug']] = cat_counts.get(r['catslug'], 0) + 1
    maker_counts[r['_maker']] = maker_counts.get(r['_maker'], 0) + 1
    for t in r['_tags']:
        tag_counts[t] = tag_counts.get(t, 0) + 1

maker_list = sorted([(k, v) for k, v in maker_counts.items()], key=lambda kv: -kv[1])
# в сайдбаре — только отрасли и серии (тег «Редукторы и мотор-редукторы» = весь каталог)
SIDEBAR_TAG_SKIP = {t['short'] for t in tags_data.TYPE}
top_tags = sorted([(k, v) for k, v in tag_counts.items() if k not in SIDEBAR_TAG_SKIP],
                  key=lambda kv: -kv[1])[:10]
TOTAL = len(ROWS)


def card(r):
    maker_slug, maker_name = r['_maker']
    tags = ','.join(r['_tags'])
    return f"""
      <article class="bep-card bep-pcard" data-cat="{r['catslug']}" data-maker="{maker_slug}"
               data-tags="{esc(tags)}" data-name="{esc(r['h1'].lower())}">
        <a class="bep-card-img" href="product/{r['slug_safe']}.html">
          <img src="{r['_img']}" alt="{esc(r['h1'])}" loading="lazy">
        </a>
        <div class="bep-card-body">
          <a class="bep-card-cat" href="category/{r['catslug']}.html">{esc(CAT_NAMES.get(r['catslug'], r['cat']))}</a>
          <b class="bep-card-name"><a href="product/{r['slug_safe']}.html">{esc(r['h1'])}</a></b>
          <span class="bep-pcard-maker">{esc(maker_name)}</span>
        </div>
      </article>"""


def sidebar():
    n_tags = len(tags_data.INDUSTRY)
    cats = []
    for slug in CAT_ORDER:
        n = cat_counts.get(slug, 0)
        if not n:
            continue
        cats.append(f"""
        <li>
          <label class="bep-filter">
            <input type="radio" name="bep-cat" value="{slug}">
            <span class="bep-filter-name">{esc(CAT_NAMES[slug])}</span>
            <i class="bep-filter-count">{n}</i>
            <a class="bep-filter-go" href="category/{slug}.html" title="О категории и применении"
               aria-label="Открыть страницу категории">→</a>
          </label>
        </li>""")
    makers = []
    for (slug, name), n in maker_list:
        makers.append(f"""
        <li>
          <label class="bep-filter">
            <input type="checkbox" name="bep-maker" value="{slug}">
            <span class="bep-filter-name">{esc(name)}</span>
            <i class="bep-filter-count">{n}</i>
          </label>
        </li>""")
    tags = ''.join(
        f'<button type="button" class="bep-chip" data-tag="{esc(t)}">{esc(t)}</button>' for t, _ in top_tags)
    return f"""
    <aside class="bep-sidebar" id="bep-sidebar">
      <div class="bep-widget">
        <h3 class="bep-widget-title">Поиск по названию</h3>
        <div class="bep-search-field bep-sidebar-search">
          <i class="tji-search"></i>
          <input type="search" id="bep-q" placeholder="NMRV, RT500, планетарный…" autocomplete="off">
        </div>
      </div>

      <div class="bep-widget">
        <h3 class="bep-widget-title">Категории</h3>
        <ul class="bep-filter-list">
          <li>
            <label class="bep-filter">
              <input type="radio" name="bep-cat" value="all" checked>
              <span class="bep-filter-name">Все категории</span>
              <i class="bep-filter-count">{TOTAL}</i>
            </label>
          </li>{''.join(cats)}
        </ul>
      </div>

      <div class="bep-widget">
        <h3 class="bep-widget-title">Производитель</h3>
        <ul class="bep-filter-list">{''.join(makers)}</ul>
        <a class="bep-widget-link" href="brands.html">Все бренды и описания <i class="tji-arrow-right-long"></i></a>
      </div>

      <div class="bep-widget">
        <h3 class="bep-widget-title">Назначение</h3>
        <div class="bep-chips">{tags}</div>
        <a class="bep-widget-link" href="tags.html">Все {n_tags} отраслей и тегов <i class="tji-arrow-right-long"></i></a>
      </div>

      <div class="bep-widget bep-widget-cta">
        <h3 class="bep-widget-title">Не нашли нужное?</h3>
        <p>Инженер подберёт модель по крутящему моменту, оборотам и монтажному исполнению.</p>
        <a class="tj-primary-btn" href="index.html#contacts"><span class="btn-text"><span>Запросить подбор</span></span>
          <span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
        <a class="bep-widget-phone" href="{home.PHONE_HREF}"><i class="tji-phone"></i>{home.PHONE}</a>
      </div>
    </aside>"""


def page():
    def fix(html):
        html = html.replace('href="brands.html"', 'href="brands.html"')
        html = html.replace('href="#', 'href="index.html#')
        html = html.replace('href="index.html#"', 'href="#"')
        return html.replace('href="index.html#catalog"', 'href="catalog.html"')

    header = fix(home.header())
    footer = fix(home.footer())
    overlays = home.overlays()
    cards = ''.join(card(r) for r in ROWS)
    cat_total = len([x for x in CAT_ORDER if cat_counts.get(x)])
    brand_total = len(maker_list)
    return f"""<!DOCTYPE html>
<html lang="ru" data-accent="teal">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Каталог приводной техники — 172 модели | БелЕвропривод</title>
<meta name="description" content="Каталог БелЕвропривода: 172 модели редукторов, мотор-редукторов, вариаторов и электродвигателей в 17 категориях. Склад в Минске, подбор под задачу.">
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
            <a href="index.html">Главная</a><i class="tji-arrow-right-long"></i><span>Каталог</span>
          </nav>
          <span class="bep-kicker"><i class="tji-service-1"></i> {TOTAL}&nbsp;модели · {cat_total}&nbsp;категорий</span>
          <h1 class="bep-hero1-title">Редукторы и приводы<br><span>под задачу производства.</span></h1>
          <div class="bep-hero1-row">
            <a class="bep-hero1-link" href="#bep-grid" aria-label="К товарам">
              <i class="tji-arrow-down-long"></i>
            </a>
            <span class="bep-hero1-div"></span>
            <p class="bep-hero1-desc">Подбираем по крутящему моменту, оборотам и монтажному исполнению.
              Склад в Минске, {brand_total}&nbsp;производителей и 15&nbsp;поставщиков, доставка по Беларуси и в&nbsp;Россию.</p>
          </div>
        </div>
        <div class="bep-hero1-media">
          <img src="assets/img/hero/slide-1.jpg" alt="Производство приводной техники">
          <div class="bep-hero1-card">
            <div><b>{TOTAL}</b><span>модели в каталоге</span></div>
            <div class="bep-hero1-thumbs">
              <img src="assets/img/products/nmrv_chervyachni.jpg" alt="">
              <img src="assets/img/products/s1000.jpg" alt="">
              <img src="assets/img/products/rt500.jpg" alt="">
            </div>
          </div>
        </div>
      </div>
      <a class="bep-hero1-scroll" href="#bep-grid">Листать каталог <i class="tji-arrow-down"></i></a>
    </div>
  </section>

  <section class="bep-catalog section-gap">
    <div class="container">
      <div class="row row-gap-4">
        <div class="col-xl-3 col-lg-4">
          <button class="bep-filters-toggle" id="bep-filters-toggle">
            <i class="tji-list"></i> Фильтры <span id="bep-filters-count"></span>
          </button>
          {sidebar()}
        </div>
        <div class="col-xl-9 col-lg-8">
          <div class="bep-toolbar">
            <p class="bep-toolbar-count" id="bep-count">Показано 1–16 из {TOTAL}</p>
            <div class="bep-toolbar-right">
              <label class="bep-select-wrap">
                <select id="bep-sort" aria-label="Сортировка">
                  <option value="name">По названию А–Я</option>
                  <option value="name-desc">По названию Я–А</option>
                  <option value="cat">По категории</option>
                  <option value="maker">По производителю</option>
                </select>
              </label>
              <label class="bep-select-wrap">
                <select id="bep-perpage" aria-label="Позиций на странице">
                  <option value="12">12 на странице</option>
                  <option value="16" selected>16 на странице</option>
                  <option value="24">24 на странице</option>
                  <option value="48">48 на странице</option>
                </select>
              </label>
            </div>
          </div>

          <div class="bep-active-filters" id="bep-active" hidden></div>

          <div class="bep-pgrid" id="bep-grid">{cards}
          </div>

          <div class="bep-empty" id="bep-empty" hidden>
            <h3>Ничего не нашлось</h3>
            <p>Сбросьте фильтры или напишите нам — подберём аналог под задачу.</p>
            <button type="button" class="tj-primary-btn" id="bep-reset-empty">
              <span class="btn-text"><span>Сбросить фильтры</span></span>
              <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
            </button>
          </div>

          <nav class="bep-pager" id="bep-pager" aria-label="Постраничная навигация"></nav>
        </div>
      </div>
    </div>
  </section>
</main>
{footer}
{overlays}
<script>window.BEP_PRODUCTS = {home.search_index()};</script>
<script src="assets/js/swiper-bundle.min.js"></script>
<script src="assets/js/main.js"></script>
<script src="assets/js/catalog.js"></script>
</body>
</html>
"""


if __name__ == '__main__':
    out = os.path.join(HERE, 'catalog.html')
    open(out, 'w', encoding='utf-8').write(page())
    print('written', out)
