#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Единый реестр тегов («Продукты по назначению») для меню, страницы тегов и каталога.

Источник: data/catalog.json (обход каталога клиента, 172 товара) + data/tags.json
(снимок страниц /product-tag/<slug> с сайта: H1 и лид).

Все значения фильтра в каталоге — короткие подписи (`short`), поэтому один и тот же
реестр используется и в ссылках меню, и в data-tags карточек каталога.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = json.load(open(os.path.join(HERE, 'data', 'catalog.json'), encoding='utf-8'))
try:
    SITE_TAGS = {t['slug']: t for t in
                 json.load(open(os.path.join(HERE, 'data', 'tags.json'), encoding='utf-8'))}
except FileNotFoundError:
    SITE_TAGS = {}

SITE = 'https://beleuroprivod.by'

# ---------------------------------------------------------------- метаданные
# short — подпись в фильтрах/меню (ключ фильтра), full — название тега на сайте
META = [
    # отрасль / назначение
    ('selskoe_hozyaistvo', 'industry', 'Сельхозтехника'),
    ('mashinostroenie', 'industry', 'Машиностроение'),
    ('conveyor_stanki', 'industry', 'Конвейеры и станки'),
    ('pishevaya_prom', 'industry', 'Пищевая промышленность'),
    ('tyashelaya_legkaya_him_prom', 'industry', 'Тяжёлая, лёгкая и химическая пром.'),
    ('tyashelaya_legkaya_prom', 'industry', 'Тяжёлая и лёгкая промышленность'),
    ('kom_tech', 'industry', 'Коммунальная и дорожная техника'),
    ('conveyor', 'industry', 'Конвейеры и транспортные системы'),
    ('tyashelaya_prom', 'industry', 'Тяжёлая промышленность'),
    ('spec_tech', 'industry', 'Краны и стройтехника'),
    ('poleznie_iskopaemie', 'industry', 'Добыча полезных ископаемых'),
    ('medicine', 'industry', 'Медицинское оборудование'),
    ('les', 'industry', 'Лесное хозяйство'),
    # серии и модели техники
    ('srk_mv', 'series', 'СРК серии MV'),
    ('urn', 'series', 'Мульчер УРН-450'),
    ('vmix', 'series', 'Амкодор В-МИКС'),
    ('k4', 'series', 'Камнеподборщик К-4'),
    ('roum-sf', 'series', 'РОУМ серии SF'),
    ('rvs1500', 'series', 'РВС-1500 «Хозяин»'),
    # тип продукции (не отрасль)
    ('reduktory-motor-reduktory', 'type', 'Редукторы и мотор-редукторы'),
]

KIND_TITLES = {
    'industry': 'Отрасли и применение',
    'series': 'Серии и модели техники',
    'type': 'Тип продукции',
}


def clean(text):
    """Убираем хвосты вида «др....», двойные пробелы, точку в конце."""
    t = (text or '').replace('&quot;', '"').strip()
    t = t.replace('и др....', 'и др.').replace('....', '…')
    while t.endswith('..'):
        t = t[:-1]
    return ' '.join(t.split())


# канонические полные названия тегов с сайта (по одному на slug)
FULL = {}
LEAD = {}
for p in CATALOG:
    for name, slug in zip(p.get('tags') or [], p.get('tag_slugs') or []):
        FULL.setdefault(slug, name)
        if not LEAD.get(slug):
            LEAD[slug] = clean((SITE_TAGS.get(slug) or {}).get('lead'))

CAT_NAMES = {}
for p in CATALOG:
    CAT_NAMES.setdefault(p['catslug'], p['cat'])

IMG = {p['slug_safe']: 'assets/img/products/%s.jpg' % p['slug_safe'] for p in CATALOG}

TAGS = []
for slug, kind, short in META:
    prods = [p for p in CATALOG if slug in (p.get('tag_slugs') or [])]
    counts = {}
    for p in prods:
        counts[p['catslug']] = counts.get(p['catslug'], 0) + 1
    cats = sorted(counts.items(), key=lambda kv: (-kv[1], CAT_NAMES.get(kv[0], '')))
    # примеры: сначала позиции с фото; 3 штуки
    samples = sorted(prods, key=lambda p: (0 if IMG.get(p['slug_safe']) else 1, p['h1']))[:3]
    TAGS.append(dict(
        slug=slug, kind=kind, short=short,
        full=clean(FULL.get(slug, short)),
        count=len(prods),
        lead=LEAD.get(slug, ''),
        cats=[(s, CAT_NAMES.get(s, s), n) for s, n in cats],
        top_cat=cats[0][0] if cats else 'drugoe',
        samples=[(p['slug_safe'], p['h1'], IMG.get(p['slug_safe'], '')) for p in samples],
        site_url='%s/product-tag/%s' % (SITE, slug),
    ))

TAGS.sort(key=lambda t: (-t['count'], t['short']))
BY_SLUG = {t['slug']: t for t in TAGS}
INDUSTRY = [t for t in TAGS if t['kind'] == 'industry']
SERIES = [t for t in TAGS if t['kind'] == 'series']
TYPE = [t for t in TAGS if t['kind'] == 'type']

# картинка карточки: самая частая категория тега, но без повторов между карточками
_used = set()
for _t in TAGS:
    _pic = next((s for s, _, _ in _t['cats'] if s not in _used), _t['top_cat'])
    _used.add(_pic)
    _t['img'] = _pic

# полное название с сайта → короткая подпись (для чипов в карточках товаров)
_FULL2SHORT = {}
for t in TAGS:
    _FULL2SHORT[t['full'].rstrip('.').lower()] = t['short']
    _FULL2SHORT[t['short'].lower()] = t['short']


def short_of(name):
    """Короткая подпись тега по названию с сайта (None, если тег не отраслевой)."""
    return _FULL2SHORT.get(clean(name).rstrip('.').lower())


def label(slug):
    return BY_SLUG[slug]['short'] if slug in BY_SLUG else slug


def catalog_href(tag):
    """Ссылка на каталог с включённым фильтром по тегу."""
    from urllib.parse import quote
    slug = tag['slug'] if isinstance(tag, dict) else tag
    return 'catalog.html?tag=%s' % quote(label(slug))


if __name__ == '__main__':
    for t in TAGS:
        print('%-11s %-3d %-32s %-46s %s' % (t['kind'], t['count'], t['short'], t['full'][:44],
                                             ','.join('%s:%d' % (c[1][:18], c[2]) for c in t['cats'][:3])))
    print('итого тегов:', len(TAGS), '| товаров в отраслях:',
          len({p['slug_safe'] for p in CATALOG if set(p.get('tag_slugs') or []) & {t['slug'] for t in INDUSTRY}}))
