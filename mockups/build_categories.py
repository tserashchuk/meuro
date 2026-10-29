#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генератор страниц категорий: category/<slug>.html — своя шапка, картинка и описание."""
import html
import json
import os
import re

import build as home
import tags_data
from urllib.parse import quote

SKIP_TAGS = {t['short'] for t in tags_data.TYPE}

HERE = os.path.dirname(os.path.abspath(__file__))
CAT = json.load(open(os.path.join(HERE, 'data', 'catalog.json'), encoding='utf-8'))
CIN = json.load(open(os.path.join(HERE, 'data', 'categories.json'), encoding='utf-8'))
OUT = os.path.join(HERE, 'category')
os.makedirs(OUT, exist_ok=True)

CAT_NAMES = dict({c['slug']: c['name'] for c in home.CATS})
CAT_NAMES.update({s: n for s, n, _ in home.OTHER_CATS})
CAT_ORDER = [c['slug'] for c in home.CATS] + [s for s, _, _ in home.OTHER_CATS]

LOGO = {  # slug производителя → логотип (путь от корня проекта)
    'nord': 'assets/img/brands/nord.png', 'Motovario': 'assets/img/brands/motovario.png',
    'brevini': 'assets/img/brands/brevini.png', 'bondioli_pavesi': 'assets/img/brands/bondioli.png',
    'tambov_polimer': 'assets/img/brands/tambovpolimermash.png',
    'ChelyabinskReduktor': 'assets/img/brands/chzr.png',
    'mogilev_electrodvig': 'assets/img/brands/mze.png', 'pskovskii_privod': 'assets/img/brands/pzmp.png',
    'SEW_Eurodrive': 'assets/img/brands/sew.png', 'own': 'assets/img/logo-mark-orange.png',
}


def esc(s):
    return html.escape(s or '', quote=True)


def fix(t, prefix='../'):
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


# ------------------------------------------------------------------ данные
by_cat = {}
for r in CAT:
    by_cat.setdefault(r['catslug'], []).append(r)

INFO = {}
for slug in CAT_ORDER:
    prods = by_cat.get(slug, [])
    if not prods:
        continue
    names = {r.get('maker_slug') or 'own': (r.get('maker') or 'БелЕвропривод') for r in prods}
    tags = {}
    # применения: только отраслевые теги и серии, по частоте (подписи — из tags_data)
    for r in prods:
        for t in (r.get('tags') or []):
            n = tags_data.short_of(t)
            if n and n not in SKIP_TAGS:
                tags[n] = tags.get(n, 0) + 1
    apps = [t for t, _ in sorted(tags.items(), key=lambda kv: -kv[1])][:6]
    info = CIN.get(slug, {})
    INFO[slug] = dict(
        slug=slug, name=CAT_NAMES.get(slug, prods[0]['cat']), n=len(prods),
        makers=sorted(names.items(), key=lambda kv: -sum(1 for r in prods if (r.get('maker_slug') or 'own') == kv[0])),
        prods=sorted(prods, key=lambda r: r['h1']),
        apps=apps, lead=(info.get('lead') or '').strip(), h1site=(info.get('h1') or '').strip(),
        img='../assets/img/cat/%s.png' % slug,
    )

TOTAL = sum(v['n'] for v in INFO.values())


def shorten(text, limit=44):
    """Обрезает длинное назначение по границе слова, убирая висячие союзы."""
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(' ', 1)[0]
    cut = re.sub(r'[,\s]+$', '', cut)
    hang = ('и', 'или', 'для', 'с', 'в', 'на', 'по', 'от', 'а')
    tail = re.compile(r'(ого|его|ых|их|ому|ым|ой|ая|ий|ый)$', re.I)
    while True:
        words = cut.split(' ')
        if len(words) < 2:
            break
        last = re.sub(r'[,\s]+$', '', words[-1])
        if last.lower() in hang or tail.search(last):
            cut = ' '.join(words[:-1]).rstrip(',')
            continue
        break
    return re.sub(r'[,\s]+$', '', cut)


GEN = {
    'Сельхозтехника': 'сельхозтехники', 'Машиностроение': 'машиностроения',
    'Конвейеры и станки': 'конвейеров и станков', 'Тяжёлая и химическая пром.': 'тяжёлой и химической промышленности',
    'Пищевая промышленность': 'пищевой промышленности', 'Коммунальная техника': 'коммунальной техники',
    'Лесное хозяйство': 'лесного хозяйства', 'Добыча полезных ископаемых': 'добычи полезных ископаемых',
    'Медицинское оборудование': 'медицинского оборудования', 'Конвейеры и транспорт': 'конвейеров и транспорта',
    'Краны и стройтехника': 'кранов и стройтехники', 'Тяжёлая и лёгкая пром.': 'тяжёлой и лёгкой промышленности',
}


def purpose(info):
    """Серая вторая строка заголовка: назначение категории из её же h1 на сайте."""
    s = info['h1site']
    s = re.sub(r'\s+с доставкой.*$', '', s, flags=re.I)
    s = re.sub(r'^.*?\bдля\b', 'для', s, flags=re.I | re.S)
    s = re.sub(r'^купить.*$', '', s, flags=re.I)
    s = re.sub(r'\s+в Минске.*$', '', s, flags=re.I)
    s = s.strip(' .,;')
    bad = ('ваш', 'по низк', 'минск', 'под заказ')
    if 10 <= len(s) <= 68 and s.lower().startswith('для') and not any(b in s.lower() for b in bad):
        short = shorten(s)
        if len(short) >= 12:
            return short
    # запасной вариант — из отраслевых тегов этой же категории
    gen = [GEN[a] for a in info['apps'] if a in GEN]
    if gen:
        return 'для %s' % gen[0]
    return ''


def lead_of(info, limit=190):
    """Короткая версия описания для шапки: первое предложение."""
    t = info['lead'] or ''
    m = re.match(r'(.{60,}?[.!?])(?:\s|$)', t)
    if m:
        t = m.group(1)
    if len(t) > limit:
        t = t[:limit].rsplit(' ', 1)[0].rstrip('.,;:') + '…'
    return t


def card(r):
    maker = r.get('maker') or 'БелЕвропривод'
    return f"""
        <article class="bep-card bep-pcard" data-maker="{esc(r.get('maker_slug') or 'own')}">
          <a class="bep-card-img" href="../product/{r.get('slug_safe', r['slug'])}.html">
            <img src="../assets/img/products/{r.get('slug_safe', r['slug'])}.jpg" alt="{esc(r['h1'])}" loading="lazy">
          </a>
          <div class="bep-card-body">
            <span class="bep-card-cat">{esc(make(r))}</span>
            <b class="bep-card-name"><a href="../product/{r.get('slug_safe', r['slug'])}.html">{esc(r['h1'])}</a></b>
            <span class="bep-pcard-maker">{esc(maker)}</span>
          </div>
        </article>"""


def make(r):
    return CAT_NAMES.get(r['catslug'], r['cat'])


def related(info, k=4):
    others = [v for s, v in INFO.items() if s != info['slug']]
    others.sort(key=lambda v: -v['n'])
    return others[:k]


def page(info):
    chips = '<button class="bep-catchip is-active" data-maker="all">Все <i>%d</i></button>' % info['n']
    for slug, name in info['makers']:
        cnt = sum(1 for r in info['prods'] if (r.get('maker_slug') or 'own') == slug)
        chips += '<button class="bep-catchip" data-maker="%s">%s <i>%d</i></button>' % (esc(slug), esc(name), cnt)
    cards = ''.join(card(r) for r in info['prods'])
    top = ''.join('<li><a href="../product/%s.html">%s</a></li>'
                  % (r.get('slug_safe', r['slug']), esc(r['h1'])) for r in info['prods'][:3])
    rel = ''.join(f"""
        <a class="bep-relcard" href="{r['slug']}.html">
          <span class="bep-relcard-img"><img src="{r['img']}" alt="{esc(r['name'])}" loading="lazy"></span>
          <b>{esc(r['name'])}</b>
          <span class="bep-relcard-n">{r['n']} {home.plural(r['n'], 'модель', 'модели', 'моделей')}</span>
        </a>""" for r in related(info))
    brand_thumbs = ''
    for slug, name in info['makers'][:4]:
        logo = LOGO.get(slug)
        if logo:
            brand_thumbs += '<img src="../%s" alt="%s" title="%s">' % (logo, esc(name), esc(name))
        else:
            brand_thumbs += '<i>%s</i>' % esc((name or '?')[0])
    names = [n for _, n in info['makers']]
    brand_names = ' · '.join(names[:2])
    if len(names) > 2:
        brand_names += ' +%d' % (len(names) - 2)
    p = purpose(info)
    title_line = (' <span>%s.</span>' % esc(p)) if p else ''
    lead = lead_of(info)
    apps = ''.join('<a class="bep-chip" href="../catalog.html?tag=%s">%s</a>' % (quote(a), esc(a))
                   for a in info['apps'])
    apps_sentence = ''
    ind = [a for a in info['apps'] if a != 'Редукторы и мотор-редукторы']
    if ind:
        apps_sentence = ('<p>Основные применения: %s. Под такие задачи подбираем исполнение '
                         'по моменту, оборотам и условиям среды.</p>'
                         % ', '.join(a.lower() for a in ind[:4]))

    header = fix(home.header()).replace('href="../catalog.html#', 'href="../index.html#')
    footer = fix(home.footer()).replace('href="../catalog.html#', 'href="../index.html#')
    overlays = fix(home.overlays())
    prod_pages = len(info['prods'])

    return f"""<!DOCTYPE html>
<html lang="ru" data-accent="teal">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(info['name'])} — {info['n']} моделей с доставкой по Беларуси | БелЕвропривод</title>
<meta name="description" content="{esc(lead or info['name'])}">
<link rel="preload" href="../assets/media/manrope/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../assets/css/00-swiper-bundle.css">
<link rel="stylesheet" href="../assets/css/01-fonts.css">
<link rel="stylesheet" href="../assets/css/02-bootstrap.css">
<link rel="stylesheet" href="../assets/css/03-fontawesome.css">
<link rel="stylesheet" href="../assets/css/05-swiper-icons.css">
<link rel="stylesheet" href="../assets/css/06-theme.css">
<link rel="stylesheet" href="../assets/css/bep.css">
<link rel="stylesheet" href="../assets/css/cat-hero.css">
<link rel="stylesheet" href="../assets/css/header.css">
<link rel="stylesheet" href="../assets/css/mega.css">
</head>
<body class="bep-catalog-page">
{header}
<main>
  <section class="bep-ch">
    <div class="bep-ch-grid">
      <div class="bep-ch-left">
        <div class="bep-ch-body">
          <nav class="bep-ch-crumbs" aria-label="Хлебные крошки">
            <a href="../index.html">Главная</a><i class="tji-arrow-right-long"></i>
            <a href="../catalog.html">Каталог</a><i class="tji-arrow-right-long"></i>
            <span>{esc(info['name'])}</span>
          </nav>
          <span class="bep-ch-kicker"><i class="tji-service-1"></i> {info['n']}&nbsp;{home.plural(info['n'], 'модель', 'модели', 'моделей')} ·
            {len(info['makers'])}&nbsp;{home.plural(len(info['makers']), 'производитель', 'производителя', 'производителей')}</span>
          <h1 class="bep-ch-title">{esc(info['name'])}{title_line}</h1>
          <div class="bep-ch-row">
            <a class="bep-ch-arrow" href="#bep-cat-products" aria-label="К товарам">
              <svg viewBox="0 0 78 78" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">
                <path d="M7 71 L71 7"/><path d="M27 7 H71 V51"/>
              </svg>
            </a>
            <span class="bep-ch-div"></span>
            <p class="bep-ch-desc">{esc(lead)}</p>
          </div>
        </div>
        <a class="bep-ch-scroll" href="#bep-cat-about"><span>Scroll&nbsp;Down</span><i class="tji-arrow-down"></i></a>
      </div>
      <div class="bep-ch-right">
        <img class="bep-ch-img" src="{info['img']}" alt="{esc(info['name'])}">
        <div class="bep-ch-notch">
          <div class="bep-ch-card">
            <div class="bep-ch-thumbs">{brand_thumbs}
              <a class="bep-ch-plus" href="../brands.html" aria-label="Все производители">+</a></div>
            <b>{info['n']}</b>
            <span>{home.plural(info['n'], 'модель', 'модели', 'моделей')} от
              {len(info['makers'])} {home.plural(len(info['makers']), 'производителя', 'производителей', 'производителей')}</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="bep-cat-about section-gap" id="bep-cat-about">
    <div class="container">
      <div class="bep-cat-grid2">
        <div class="bep-cat-text">
          <span class="bep-eyebrow">О категории</span>
          <h2 class="bep-cat-title">{esc(info['name'])}: что это и где применяется</h2>
          <p class="bep-cat-lead">{esc(info['lead'] or info['name'])}</p>
          {apps_sentence}
          <p>В каталоге {info['n']} {home.plural(info['n'], 'модель', 'модели', 'моделей')} от
             {len(info['makers'])} производителей:
             подбираем по крутящему моменту, передаточному числу и монтажному исполнению,
             считаем аналог снятой модели и держим ходовые позиции на складе в Минске.</p>
          <div class="bep-cat-apps">
            <span class="bep-cat-apps-label">Применение</span>
            <div class="bep-cat-apps-list">{apps or '<span class="bep-chip">Под задачу заказчика</span>'}</div>
          </div>
        </div>
        <aside class="bep-cat-facts">
          <div class="bep-cat-facts-row">
            <div><b>{info['n']}</b><span>{home.plural(info['n'], 'модель', 'модели', 'моделей')}</span></div>
            <div><b>{len(info['makers'])}</b><span>{home.plural(len(info['makers']), 'производитель', 'производителя', 'производителей')}</span></div>
          </div>
          <div class="bep-cat-facts-row">
            <div><b>1–3 дня</b><span>поставка со склада</span></div>
            <div><b>15 лет</b><span>на рынке приводов</span></div>
          </div>
          <div class="bep-cat-top">
            <h4>Часто запрашивают</h4>
            <ul>{top}</ul>
          </div>
          <a class="tj-primary-btn" href="../index.html#contacts"><span class="btn-text"><span>Подобрать модель</span></span>
            <span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
          <a class="bep-cat-phone" href="{home.PHONE_HREF}"><i class="tji-phone"></i>{home.PHONE}</a>
        </aside>
      </div>
    </div>
  </section>

  <section class="bep-cat-products section-gap" id="bep-cat-products">
    <div class="container">
      <div class="bep-brands-head">
        <div>
          <h2 class="bep-brands-title">{esc(info['name'])}: все модели</h2>
          <p class="bep-brands-sub">{prod_pages} {home.plural(prod_pages, 'позиция', 'позиции', 'позиций')} от
            {len(info['makers'])} производителей</p>
        </div>
        <a class="bep-ghost-link" href="../catalog.html?category={info['slug']}">Открыть в каталоге с фильтрами
          <i class="tji-arrow-right-long"></i></a>
      </div>
      <div class="bep-catchips" id="bep-cat-chips">{chips}</div>
      <div class="bep-cat-cards" id="bep-cat-cards">{cards}</div>
      <div class="bep-empty" id="bep-cat-empty" hidden>
        <h3>У этого производителя нет позиций в категории</h3>
        <p>Привезём под заказ — уточните модель и количество.</p>
        <a class="tj-primary-btn" href="../index.html#contacts"><span class="btn-text"><span>Отправить запрос</span></span>
          <span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
      </div>
    </div>
  </section>

  <section class="bep-cat-related section-gap">
    <div class="container">
      <div class="bep-brands-head">
        <div>
          <h2 class="bep-brands-title">Другие категории</h2>
          <p class="bep-brands-sub">Всего {TOTAL} моделей в {len(INFO)} категориях</p>
        </div>
        <a class="bep-ghost-link" href="../catalog.html">Весь каталог <i class="tji-arrow-right-long"></i></a>
      </div>
      <div class="bep-relgrid">{rel}</div>
    </div>
  </section>
</main>
{footer}
{overlays}
<script>window.BEP_PRODUCTS = {home.search_index('../')};</script>
<script src="../assets/js/swiper-bundle.min.js"></script>
<script src="../assets/js/main.js"></script>
<script>
(function () {{
  var wrap = document.getElementById('bep-cat-cards');
  var chips = [].slice.call(document.querySelectorAll('.bep-catchip'));
  var empty = document.getElementById('bep-cat-empty');
  if (!wrap || !chips.length) return;
  var cards = [].slice.call(wrap.querySelectorAll('.bep-card'));
  chips.forEach(function (b) {{
    b.addEventListener('click', function () {{
      var m = b.getAttribute('data-maker');
      chips.forEach(function (x) {{ x.classList.toggle('is-active', x === b); }});
      var shown = 0;
      cards.forEach(function (c) {{
        var ok = m === 'all' || c.getAttribute('data-maker') === m;
        c.hidden = !ok;
        if (ok) shown++;
      }});
      if (empty) empty.hidden = shown !== 0;
    }});
  }});
}})();
</script>
</body>
</html>
"""


if __name__ == '__main__':
    for slug, info in INFO.items():
        open(os.path.join(OUT, slug + '.html'), 'w', encoding='utf-8').write(page(info))
        print('%-40s %3d моделей | %-14s | %s' % (slug, info['n'], len(info['makers']),
                                                 purpose(info) or '—'))
    print('written', len(INFO), 'category pages')
