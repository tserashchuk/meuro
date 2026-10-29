#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генератор tags.html — страница тегов («Отрасли и применение») в дизайне Bexon.

Все 20 тегов сайта клиента (/product-tag/*) на одной странице: 13 отраслей карточками,
6 серий/моделей списком и тег «Редукторы и мотор-редукторы» широкой полосой.
Каждая карточка ведёт в каталог с уже включённым фильтром (catalog.html?tag=…).
"""
import html
import os

import build as home
import tags_data as TAGS_MOD

HERE = os.path.dirname(os.path.abspath(__file__))
TAGS = TAGS_MOD.TAGS
INDUSTRY = TAGS_MOD.INDUSTRY
SERIES = TAGS_MOD.SERIES
TYPE = TAGS_MOD.TYPE
TOTAL_TAGGED = 166  # посчитано tags_data.py: товары каталога с хотя бы одним отраслевым тегом


def esc(s):
    return html.escape(s or '', quote=True)


def q(tag):
    """URL-encoded значение фильтра для каталога."""
    from urllib.parse import quote
    return quote(tag['short'])


def n_models(n):
    return '%d %s' % (n, home.plural(n, 'модель', 'модели', 'моделей'))


def card(t):
    chips = ''.join('<span class="bep-chip">%s <i>%d</i></span>' % (esc(name), cnt)
                    for _, name, cnt in t['cats'][:3])
    full = t['full'] if t['full'] != t['short'] else ''
    return f"""
      <a class="bep-tagcard" href="catalog.html?tag={q(t)}"
         data-name="{esc((t['short'] + ' ' + t['full']).lower())}" data-count="{t['count']}">
        <span class="bep-tagcard-media">
          <img src="assets/img/cat/{esc(t['img'])}.png" alt="" loading="lazy">
          <span class="bep-tagcard-count"><b>{t['count']}</b> {home.plural(t['count'], 'модель', 'модели', 'моделей')}</span>
        </span>
        <span class="bep-tagcard-body">
          <span class="bep-tagcard-eyebrow">Отрасль</span>
          <span class="bep-tagcard-name">{esc(t['short'])}</span>
          {f'<span class="bep-tagcard-full">{esc(full)}</span>' if full else ''}
          <span class="bep-tagcard-lead">{esc(t['lead'])}</span>
          <span class="bep-tagcard-chips">{chips}</span>
          <span class="bep-tagcard-foot">
            <span class="bep-tagcard-meta">{len(t['cats'])} {home.plural(len(t['cats']), 'категория', 'категории', 'категорий')} каталога</span>
            <span class="bep-tagcard-go">Подборка <span>→</span></span>
          </span>
        </span>
      </a>"""


def row(i, t):
    return f"""
      <a class="bep-tagrow" href="catalog.html?tag={q(t)}">
        <span class="bep-tagrow-i">{i:02d}</span>
        <span class="bep-tagrow-main">
          <span class="bep-tagrow-name">{esc(t['short'])}</span>
          <span class="bep-tagrow-full">{esc(t['full'])}</span>
        </span>
        <span class="bep-tagrow-n">{n_models(t['count'])}</span>
        <span class="bep-tagrow-go"><i class="tji-arrow-right-long"></i></span>
      </a>"""


def util_cards():
    """Две служебные плитки в конце сетки: весь каталог и заявка на подбор."""
    return f"""
      <a class="bep-tagcard bep-tagcard--total" href="catalog.html">
        <span class="bep-tagcard-media bep-tagcard-media--ink">
          <span class="bep-tagcard-big">172<span>модели в каталоге</span></span>
        </span>
        <span class="bep-tagcard-body">
          <span class="bep-tagcard-eyebrow">Весь каталог</span>
          <span class="bep-tagcard-name">Без фильтра по отрасли</span>
          <span class="bep-tagcard-full">17 категорий и 9 производителей в одном списке</span>
          <span class="bep-tagcard-lead">Если назначение не важно — смотрите все позиции каталога
            с фильтрами по категории, производителю и наличию чертежей.</span>
          <span class="bep-tagcard-chips"><span class="bep-chip">17 категорий</span>
            <span class="bep-chip">9 производителей</span></span>
          <span class="bep-tagcard-foot">
            <span class="bep-tagcard-meta">172 модели</span>
            <span class="bep-tagcard-go">В каталог <span>→</span></span>
          </span>
        </span>
      </a>

      <a class="bep-tagcard bep-tagcard--cta" href="#" data-open-modal>
        <span class="bep-tagcard-body">
          <span class="bep-tagcard-eyebrow">Подбор инженером</span>
          <span class="bep-tagcard-name">Не нашли свою отрасль?</span>
          <span class="bep-tagcard-lead">Пришлите фото шильдика или опишите оборудование: нагрузку,
            обороты, передаточное число. Подберём модель и пришлём характеристики до оплаты.</span>
          <span class="bep-tagcard-chips"><span class="bep-chip">Ответ в рабочее время</span>
            <span class="bep-chip">Чертежи до оплаты</span></span>
          <span class="bep-tagcard-foot">
            <span class="bep-tagcard-meta">{home.PHONE}</span>
            <span class="bep-tagcard-go">Оставить заявку <span>→</span></span>
          </span>
        </span>
      </a>"""


def page():
    header = home.header()
    footer = home.footer()
    cards = ''.join(card(t) for t in INDUSTRY) + util_cards()
    rows = ''.join(row(i + 1, t) for i, t in enumerate(
        sorted(SERIES, key=lambda x: (-x['count'], x['short']))))
    type_banner = ''.join(f"""
      <a class="bep-tagtype-card" href="catalog.html?tag={q(t)}">
        <span class="bep-tagtype-main">
          <span class="bep-tagtype-hint">Тег типа продукции</span>
          <span class="bep-tagtype-name">{esc(t['short'])}</span>
          <span class="bep-tagtype-desc">Самая широкая подборка: вся номенклатура приводов без привязки
            к отрасли — это {t['count']} из 172 позиций каталога.</span>
        </span>
        <span class="bep-tagtype-num">{t['count']}<span>моделей</span></span>
        <span class="bep-tagtype-go"><i class="tji-arrow-right-long"></i></span>
      </a>""" for t in TYPE)
    hero_thumbs = ''.join('<img src="assets/img/cat/%s.png" alt="">' % esc(t['top_cat'])
                          for t in INDUSTRY[:3])
    cats_in_tags = len({c[0] for t in INDUSTRY for c in t['cats']})

    return f"""<!DOCTYPE html>
<html lang="ru" data-accent="teal">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Отрасли и применение редукторов — 13 отраслей, 20 тегов | БелЕвропривод</title>
<meta name="description" content="Подбор редукторов и мотор-редукторов по отрасли: сельхозтехника, машиностроение, конвейеры и станки, пищевая, химическая, коммунальная техника. 13 отраслей и 6 серий техники, 166 моделей каталога с тегами.">
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
<link rel="stylesheet" href="assets/css/tags.css">
</head>
<body class="bep-catalog-page">
{header}
<main>
  <section class="bep-hero1 bep-hero1--tags">
    <div class="container">
      <div class="bep-hero1-inner">
        <div>
          <nav class="bep-hero1-crumbs" aria-label="Хлебные крошки">
            <a href="index.html">Главная</a><i class="tji-arrow-right-long"></i><span>Отрасли</span>
          </nav>
          <span class="bep-kicker"><i class="tji-list"></i> {len(INDUSTRY)} отраслей · {len(TAGS)} тегов · {TOTAL_TAGGED} моделей</span>
          <h1 class="bep-hero1-title">Подбор привода<br><span>по отрасли и технике.</span></h1>
          <div class="bep-hero1-row">
            <a class="bep-hero1-link" href="#bep-tags-grid" aria-label="К отраслям">
              <i class="tji-arrow-down-long"></i>
            </a>
            <span class="bep-hero1-div"></span>
            <p class="bep-hero1-desc">Отраслевые теги с сайта клиента: от сельхозтехники до медицинского
              оборудования. Выбирайте отрасль — откроется подборка моделей, которые ставят на такую технику.</p>
          </div>
        </div>
        <div class="bep-hero1-media">
          <img src="assets/img/hero/slide-1.jpg" alt="Производственные линии: приводы для разных отраслей">
          <div class="bep-hero1-card">
            <div><b>{TOTAL_TAGGED}</b><span>моделей с отраслевыми тегами</span></div>
            <div class="bep-hero1-thumbs">{hero_thumbs}</div>
          </div>
        </div>
      </div>
      <a class="bep-hero1-scroll" href="#bep-tags-grid">Смотреть все отрасли <i class="tji-arrow-down"></i></a>
    </div>
  </section>

  <section class="bep-tags section-gap" id="bep-tags-grid">
    <div class="container">
      <div class="bep-tags-head">
        <div>
          <span class="bep-eyebrow">Отрасли и применение</span>
          <h2 class="bep-tags-title">Где работает наша продукция</h2>
          <p class="bep-tags-sub">{len(INDUSTRY)} отраслей · {TOTAL_TAGGED} моделей · {cats_in_tags} категорий каталога.
            Карточка открывает каталог с уже включённым фильтром по тегу.</p>
        </div>
        <label class="bep-brands-search bep-tags-search">
          <i class="tji-search"></i>
          <input type="search" id="bep-tags-q" placeholder="Найти отрасль: конвейер…" autocomplete="off">
        </label>
      </div>

      <div class="bep-tags-grid" id="bep-tags">{cards}</div>

      <div class="bep-empty" id="bep-tags-empty" hidden>
        <h3>Такой отрасли в списке нет</h3>
        <p>Опишите оборудование — инженер подберёт привод по нагрузке, оборотам и монтажному исполнению.</p>
        <a class="tj-primary-btn" href="#" data-open-modal><span class="btn-text"><span>Отправить запрос</span></span>
          <span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>
      </div>
    </div>
  </section>

  <section class="bep-tagseries">
    <div class="container">
      <div class="bep-tagseries-head">
        <div>
          <span class="bep-eyebrow">Серии и модели техники</span>
          <h2 class="bep-tagseries-title">Теги по конкретным машинам</h2>
        </div>
        <p class="bep-tagseries-note">На сайте клиента такие теги есть, но их не видно в навигации:
          поиск по «Амкодор В-МИКС» или «СРК» идёт из поиска, а не из меню.</p>
      </div>
      <div class="bep-tagrows">{rows}</div>
    </div>
  </section>

  <section class="bep-tagtype">
    <div class="container">
      {type_banner}
    </div>
  </section>

  <section class="bep-tagnote">
    <div class="container">
      <div class="bep-tagnote-grid">
        <div class="bep-tagnote-card">
          <span class="bep-eyebrow">Что стоит починить на сайте</span>
          <h3>Три тега про тяжёлую промышленность, два — про конвейеры</h3>
          <ul>
            <li><b>Тяжёлая, лёгкая и химическая пром.</b> — 32 модели, <b>Тяжёлая и лёгкая промышленность</b> — 21
              и <b>Тяжёлая промышленность</b> — 5: один и тот же спрос, разбитый на три тега.</li>
            <li><b>Конвейеры и станки</b> — 78 моделей и <b>Конвейеры и транспортные системы</b> — 8:
              дубль, который делит один трафик на две страницы.</li>
            <li>6 позиций каталога из 172 не размечены ни одним отраслевым тегом — они не попадут
              ни в одну подборку.</li>
            <li>Ни один отраслевой тег не виден в меню: на сайте попасть в подборку можно только
              из поиска или из футера.</li>
          </ul>
          <p>В макете теги оставлены как на сайте (чтобы ничего не потерять), но сгруппированы:
            отрасли, серии техники и тип продукции, и выведены в меню и футер.</p>
        </div>
        <div class="bep-tagnote-cta">
          <span class="bep-tagnote-label">Что предлагаем</span>
          <h3>Свести теги к 8–9 отраслям</h3>
          <ol class="bep-tagnote-steps">
            <li>Склеить три «тяжёлых» тега и два «конвейерных» в один каждый.</li>
            <li>Дать каждой отрасли страницу с описанием и подборкой — как у категорий.</li>
            <li>Оставить в меню все отрасли и серии: сейчас их видно только из поиска.</li>
          </ol>
          <div class="bep-tagnote-actions">
            <a class="bep-ghost-link" href="{home.PHONE_HREF}"><i class="tji-phone"></i> {home.PHONE}</a>
            <a class="bep-ghost-link" href="https://beleuroprivod.by/product-tag/selskoe_hozyaistvo"
               target="_blank" rel="noopener">Как это сейчас <i class="tji-arrow-right-long"></i></a>
          </div>
        </div>
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
  var q = document.getElementById('bep-tags-q');
  var cards = [].slice.call(document.querySelectorAll('.bep-tagcard'));
  var empty = document.getElementById('bep-tags-empty');
  if (!q) return;
  q.addEventListener('input', function () {{
    var v = q.value.trim().toLowerCase();
    var shown = 0;
    cards.forEach(function (c) {{
      var ok = !v || (c.getAttribute('data-name') || '').indexOf(v) > -1;
      c.hidden = !ok;
      if (ok) shown++;
    }});
    empty.hidden = shown !== 0;
  }});
}})();
</script>
</body>
</html>
"""


if __name__ == '__main__':
    out = os.path.join(HERE, 'tags.html')
    open(out, 'w', encoding='utf-8').write(page())
    print('written', out, os.path.getsize(out), 'bytes')
