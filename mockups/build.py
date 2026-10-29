#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор index.html: шаблон Bexon home-02, заполненный реальными данными
beleuroprivod.by (каталог собран обходом sitemap: 172 товара, 17 категорий).
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://beleuroprivod.by'
_LOCAL = os.path.join(HERE, 'data', 'products.json')
_SRC = os.path.expanduser('~/.hermes/cache/scratch/bep/products.json')
PRODUCTS = json.load(open(_LOCAL if os.path.exists(_LOCAL) else _SRC))

import tags_data  # единый реестр тегов сайта (отрасли, серии, тип продукции)  # noqa: E402

TAG_INDUSTRY, TAG_SERIES, TAG_TYPE = tags_data.INDUSTRY, tags_data.SERIES, tags_data.TYPE

BRAND = 'БелЕвропривод'
PHONE = '+375 (29) 6-910-510'
PHONE_HREF = 'tel:+375296910510'
PHONE_ALT = ['+375 29 6 815 205', '+375 17 374 74 54']
EMAIL = 'europrivod@mail.ru'
ADDRESS = '220137, г. Минск, Партизанский проспект 178, офис 311'
UNP = 'УНП 191148828'

CATS = [
    dict(slug='konicheskie_reduktori', name='Конические редукторы', n=49,
         desc='Конические редукторы получили своё название из-за формы зубчатых колёс: '
              'понижают частоту вращения и увеличивают крутящий момент. Угловые, одно- и двухступенчатые.',
         top=['BEP-1271', 'S-1000 / S-2000 / S-3000', 'BEP-215, BEP-240']),
    dict(slug='chervyachnie_reduktori', name='Червячные редукторы', n=19,
         desc='Червячные мотор-редукторы применяются в металлургии, горнодобыче, деревообработке, '
              'судостроении и машиностроении. Передаточное число — до 100:1, у сдвоенных до 5000:1.',
         top=['NMRV 025–150', 'NMRV-P 063–110', 'SW, 2Ч-63/80, Ч-100/160']),
    dict(slug='planetarnie_reductori', name='Планетарные редукторы', n=16,
         desc='Надёжные планетарные редукторы и мотор-редукторы 3МП для промышленного оборудования: '
              'высокий момент при компактном корпусе и соосной компоновке.',
         top=['3МП-31,5 / 3МП-40 / 3МП-50', 'MP, MPO, TD', 'BEP-0151.211.02.02']),
    dict(slug='konichesko-cilindricheskie-gidromotor', name='Коническо-цилиндрические под гидромотор', n=15,
         desc='Редукторы в сцепке с гидромотором востребованы в сельском хозяйстве, '
              'а также в дорожной и коммунальной технике.',
         top=['5545 (RT500)', 'BEP-0881 / 0882', 'BEP-1141F / 1142F']),
    dict(slug='reductori_parral_vali', name='Цилиндрические с параллельными валами', n=13,
         desc='Применяются в системах с конвейерами и шнеками, подходят для разных отраслей '
              'промышленности: от станкостроения до пищевого производства.',
         top=['Серия F', 'MGA, GPSH, RM', 'C2, C2N, C3U, CDN']),
    dict(slug='variatori', name='Вариаторы', n=13,
         desc='Вариатор-редуктор передаёт крутящий момент и плавно меняет передаточное отношение '
              'в диапазоне регулирования — без остановки оборудования.',
         top=['TXF и TXF+NMRV', 'VH, вариатор S', 'Гидровариаторы HS-15…HS-17']),
    dict(slug='tsilindr_soosn_reduktori', name='Цилиндрические соосные редукторы', n=9,
         desc='Соосные мотор-редукторы широко применяются в строительной технике, '
              'деревообрабатывающих и металлообрабатывающих станках.',
         top=['Серия R', 'RC, 4МЦ2С-63…125', 'Серия H, HA']),
    dict(slug='electrodvig', name='Электродвигатели', n=4,
         desc='Трёхфазные и однофазные электродвигатели: преобразуют электрическую энергию '
              'в механическую и комплектуются с редукторами любых серий.',
         top=['АИР, АИРЕ', 'Серия S', 'ТСТП']),
]

OTHER_CATS = [
    ('cepi', 'Цепи', 8), ('industrial_reductori', 'Индустриальные редукторы', 5),
    ('konichesko-tsilindricheskie_reductori', 'Коническо-цилиндрические редукторы', 4),
    ('korobki', 'Коробки передач', 4), ('drugoe', 'Другое оборудование', 3),
    ('reducktorni_balki', 'Редукторные балки', 3), ('cepnie_kolesa', 'Цепные колёса', 3),
    ('tsilindr_ploski_reductori', 'Цилиндрические плоские редукторы', 2),
    ('zapchasti', 'Запчасти и аксессуары', 2),
]

CAT_NAMES = {c['slug']: c['name'] for c in CATS}
CAT_NAMES.update({s: n for s, n, _ in OTHER_CATS})

SLIDES = [
    dict(photo='assets/img/hero/slide-1.jpg',
         title='Приводная техника<br>для вашего <span>производства.</span>',
         desc='Редукторы, мотор-редукторы, вариаторы и электродвигатели: 172 модели в каталоге, '
              'склад в Минске и подбор под задачу инженером.',
         cta='Подобрать привод', cta_href='#catalog', cta2='Популярные позиции', cta2_href='#products',
         facts=[('172', 'модели в каталоге'), ('15', 'поставщиков'), ('15 лет', 'на рынке приводов')],
         thumb='assets/img/hero/slide-1.jpg'),
    dict(photo='assets/img/hero/slide-2.jpg',
         title='Червячные мотор-редукторы <span>NMRV.</span>',
         desc='Компактный корпус, КПД до 90 %, самоторможение. Типоразмеры 025–150, '
              'крутящий момент до 1 550 Н·м, любые монтажные положения.',
         cta='Смотреть серию', cta_href='#products', cta2='Все категории', cta2_href='#catalog',
         facts=[('025–150', 'типоразмеры'), ('1 550 Н·м', 'макс. момент'), ('до 90 %', 'КПД')],
         thumb='assets/img/hero/slide-2.jpg'),
    dict(photo='assets/img/hero/slide-3.jpg',
         title='Склад в Минске —<br><span>отгрузка в день заказа.</span>',
         desc='Ходовые позиции держим на складе в Колодищах. Доставка по Беларуси и в Россию, '
              'офисы в Минске, Туле и Смоленске.',
         cta='Запросить наличие', cta_href='#contacts', cta2='Как мы работаем', cta2_href='#process',
         facts=[('4', 'офиса и склада'), ('2 страны', 'Беларусь и Россия'), ('15', 'поставщиков')],
         thumb='assets/img/hero/slide-3.jpg'),
]

BRANDS = [
    dict(slug='motovario', name='Motovario', file='motovario', n=27),
    dict(slug='ChelyabinskReduktor', name='Челябинский завод «Редуктор»', file='chzr', n=15),
    dict(slug='tambov_polimer', name='Тамбовполимермаш', file='tambovpolimermash', n=8),
    dict(slug='brevini', name='Brevini', file='brevini', n=5),
    dict(slug='bondioli_pavesi', name='Bondioli & Pavesi', file='bondioli', n=4),
    dict(slug='nord', name='NORD DRIVESYSTEMS', file='nord', n=3),
    dict(slug='pskovskii_privod', name='Псковский завод механических приводов', file='pzmp', n=3),
    dict(slug='mogilev_electrodvig', name='Могилёвский завод «Электродвигатель»', file='mze', n=2),
]

PARTNERS = [
    ('1btsk', '1БТСК'), ('maz', 'МАЗ'), ('gomselmash', 'Гомсельмаш'), ('agropromselmash', 'Агропромсельмаш'),
]

PRODUCTS_FEATURED = [
    ('nmrv-chervyachny', 'nmrv_chervyachni', 'Мотор-редуктор NMRV червячный', 'Червячные редукторы'),
    ('planetarnyj-bep-0151', 'bep1602', 'Вертикальный планетарный редуктор BEP-0151.211.02.02', 'Планетарные редукторы'),
    ('s1000', 's1000', 'Редуктор S-1000 конический угловой', 'Конические редукторы'),
    ('rt500', 'rt500', 'Редуктор 5545 (RT500)', 'Коническо-цилиндрические под гидромотор'),
    ('bep-1271', 'bep-1271', 'Конический редуктор BEP-1271', 'Конические редукторы'),
    ('k-seriya', 'koniceski_tsilindricheski_k', 'Коническо-цилиндрический редуктор серии K', 'Коническо-цилиндрические'),
    ('f-seriya', 'tsilindricheski_pv_f', 'Цилиндрический редуктор с параллельными валами серии F', 'Параллельные валы'),
    ('r-seriya', 'tsilindricheski_soosni_r', 'Цилиндрический соосный мотор-редуктор серии R', 'Соосные редукторы'),
    ('industrialnyj-v', 'industrialni_b', 'Индустриальный редуктор В', 'Индустриальные редукторы'),
    ('rc', 'rc', 'Редуктор цилиндрический соосный RC', 'Соосные редукторы'),
    ('korobka-bep00153', 'bep00.153', 'Коробка передач BEP00.153', 'Коробки передач'),
    ('korobka-bep451f', 'bep451f0303', 'Коробка передач BEP451F.03.03', 'Коробки передач'),
]

STEPS = [
    ('Заявка и консультация',
     'Опишите оборудование и задачу: нагрузка, обороты, передаточное число. Ответим в рабочее время '
     'и сразу скажем, есть ли позиция на складе.'),
    ('Подбор и расчёт',
     'Инженер подбирает модель по крутящему моменту, частоте вращения и монтажному исполнению. '
     'Присылаем характеристики и чертежи до оплаты.'),
    ('Договор и поставка',
     'Со склада в Колодищах — отгрузка в день заказа. Под заказ — работаем с 15 поставщиками, '
     'доставка по Беларуси и в Россию.'),
    ('Монтаж и сервис',
     'Помогаем с пуском и обслуживанием, поставляем запчасти для NMRV: валы, фланцы, реактивные тяги. '
     'Берём редукторы в ремонт.'),
]

INDUSTRIES = [
    ('Сельское хозяйство', 'Разбрасыватели РОУМ SF, кормораздатчики, камнеподборщики К-4, мульчеры УРН',
     'rt500', 'assets/img/cat/konichesko-cilindricheskie-gidromotor.png'),
    ('Коммунальная и дорожная техника', 'Приводы щёток, отвалов и разбрасывателей — работа под нагрузкой и на морозе',
     's1000', 'assets/img/cat/konicheskie_reduktori.png'),
    ('Конвейеры, станки, подъёмники', 'Мотор-редукторы NMRV, серии F и R для транспортных систем и станков',
     'nmrv-chervyachni', 'assets/img/cat/reductori_parral_vali.png'),
    ('Тяжёлая и химическая промышленность', 'Индустриальные редукторы серии H и B для больших мощностей',
     'industrialnyj-v', 'assets/img/cat/industrial_reductori.png'),
    ('Пищевая промышленность', 'Исполнения с пищевыми смазками и мойкой корпуса, нержавеющие опции',
     'r-seriya', 'assets/img/cat/cepi.png'),
    ('Лесное хозяйство и добыча', 'Цепные приводы, редукторные балки и приводы для тяжёлых условий',
     'k-seriya', 'assets/img/cat/cepnie_kolesa.png'),
]

OFFICES = [
    ('Офис в Минске', 'Партизанский проспект 178, офис 311', '+375 29 6 815 205', 'Минск'),
    ('Склад в Минске', 'Минский р-н, пос. Колодищи, Триумфальная 8А', '+375 29 6 910 510', 'Колодищи'),
    ('Офис в Туле', 'Тульская обл., пос. Щёкино, ул. Декабристов 45Б', '+7 903 840 06 69', 'Щёкино'),
    ('Офис в Смоленске', 'ул. 2-я Садовая, дом 2', '+7 4812 20-92-92', 'Смоленск'),
]

QUOTE = ('«Мы рады поделиться своим опытом, знаниями и умениями. Главной целью работы ставлю '
         'команду единомышленников и комфортный деловой климат. Вера в то, что мы занимаемся нужным '
         'и полезным делом, — что частичка нашего труда есть в выращенном зерне, в собранном тракторе, '
         'в построенном доме.»')

YANDEX = 'https://yandex.by/maps/?text='


# ---------------------------------------------------------------- helpers
def safe_slug(s):
    """Имя файла/страницы без символов, которые ломают URL (% : + , .)."""
    return re.sub(r'[^A-Za-z0-9_-]+', '-', s).strip('-')


def plural(n, one, few, many):
    n = abs(int(n))
    if n % 100 in (11, 12, 13, 14):
        return many
    if n % 10 == 1:
        return one
    if n % 10 in (2, 3, 4):
        return few
    return many


def models(n):
    return '%d %s' % (n, plural(n, 'модель', 'модели', 'моделей'))


def cat_img(slug):
    return 'assets/img/cat/%s.png' % slug


def product_url(slug):
    return '%s/product/%s' % (SITE, slug)


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def btn(text, href, cls='tj-primary-btn'):
    return ('<a class="%s" href="%s"><span class="btn-text"><span>%s</span></span>'
            '<span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>' % (cls, href, text))


def btn_submit(text):
    return ('<button type="submit" class="tj-primary-btn"><span class="btn-text"><span>%s</span></span>'
            '<span class="btn-icon"><i class="tji-arrow-right-long"></i></span></button>' % text)


def text_btn(text, href):
    return ('<a class="text-btn" href="%s"><span class="btn-text"><span>%s</span></span>'
            '<span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>' % (href, text))


def heading(sub, title, center=False, cls=''):
    sub_html = '<span class="sub-title">%s</span>' % sub if sub else ''
    return ('<div class="sec-heading style-2%s %s">%s'
            '<h2 class="sec-title">%s</h2></div>' %
            (' text-center' if center else '', cls, sub_html, title))


# ---------------------------------------------------------------- sections
def header():
    all_cats = [(c['slug'], c['name'], c['n']) for c in CATS] + [(s, n, c) for s, n, c in OTHER_CATS]
    total_models = sum(n for _, _, n in all_cats)

    # три колонки мега-меню: редукторы / приводы и узлы / прочее
    COLS = [
        ('Редукторы', ['konicheskie_reduktori', 'chervyachnie_reduktori', 'planetarnie_reductori',
                       'tsilindr_soosn_reduktori', 'reductori_parral_vali', 'tsilindr_ploski_reductori',
                       'industrial_reductori']),
        ('Приводы и узлы', ['konichesko-cilindricheskie-gidromotor', 'konichesko-tsilindricheskie_reductori',
                            'variatori', 'electrodvig', 'cepi', 'cepnie_kolesa']),
        ('Ещё', ['korobki', 'reducktorni_balki', 'zapchasti', 'drugoe']),
    ]
    cat_map = {s: (n, c) for s, n, c in all_cats}
    HOT = {'konicheskie_reduktori', 'chervyachnie_reductori', 'planetarnie_reductori'}

    mega_cols = ''
    for title, slugs in COLS:
        items = ''
        for s in slugs:
            if s not in cat_map:
                continue
            name, cnt = cat_map[s]
            badge = '<span class="bep-mega-badge">Хит</span>' if s in HOT else ''
            items += ('<li><a href="category/%s.html"><span class="bep-mega-name">%s%s</span>'
                      '<span class="bep-mega-count">%d</span></a></li>' % (s, name, badge, cnt))
        if title == 'Ещё':
            items += ('<li class="bep-mega-sep"><a href="catalog.html"><span class="bep-mega-name">'
                      'Все 17 категорий</span><span class="bep-mega-count">%d</span></a></li>' % total_models)
            items += ('<li><a href="brands.html"><span class="bep-mega-name">Производители</span>'
                      '<span class="bep-mega-count">9</span></a></li>')
        mega_cols += ('<div class="bep-mega-col"><h5>%s</h5><ul class="bep-mega-list">%s</ul></div>'
                      % (title, items))

    manu_items = ''.join('<li><a href="catalog.html?maker=%s">%s</a></li>' % (b['slug'], b['name'])
                         for b in BRANDS)

    # панель «Отрасли»: все 20 тегов сайта — 13 отраслей, 6 серий/моделей и тип продукции
    tag_groups = [('Отрасли', TAG_INDUSTRY[:7]), ('Ещё отрасли', TAG_INDUSTRY[7:]),
                  ('Серии и модели', TAG_SERIES)]
    tag_cols = ''
    for title, items in tag_groups:
        rows = ''.join(
            '<li><a href="%s" title="%s"><span class="bep-mega-name">%s</span>'
            '<span class="bep-mega-count">%d</span></a></li>'
            % (tags_data.catalog_href(t), esc(t['full']), esc(t['short']), t['count']) for t in items)
        tag_cols += ('<div class="bep-mega-col"><h5>%s</h5><ul class="bep-mega-list">%s</ul></div>'
                     % (title, rows))
    tag_type = (TAG_TYPE[0] if TAG_TYPE else None)
    tag_type_link = ''
    if tag_type:
        tag_type_link = ('<a class="bep-tags-mega-type" href="%s"><span>%s</span>'
                         '<span class="bep-tags-mega-type-n">%d</span></a>'
                         % (tags_data.catalog_href(tag_type), esc(tag_type['short']), tag_type['count']))

    return f"""
<header class="site-header" id="site-header">
  <div class="container">
    <div class="header-wrapper">
      <a class="bep-logo" href="#top">
        <img src="assets/img/logo-mark-teal.png" alt="БелЕвропривод">
        <span class="bep-logo-text">БелЕвропривод<em>машиностроительное оборудование</em></span>
      </a>

      <div class="menu-area d-none d-lg-inline-flex align-items-center">
        <nav class="mainmenu">
          <ul>
            <li class="has-dropdown mega-parent">
              <a href="catalog.html">Каталог</a>
              <ul class="sub-menu bep-mega">
                <li>
                  <div class="bep-mega-panel">
                    {mega_cols}
                    <aside class="bep-mega-promo">
                      <h3>{total_models}</h3>
                      <p>модели в каталоге · 17 категорий</p>
                      <a class="bep-mega-phone" href="{PHONE_HREF}"><i class="tji-phone"></i>{PHONE}</a>
                      <span class="bep-mega-promo-img"><img src="assets/img/hero/slide-2.jpg" alt=""></span>
                    </aside>
                  </div>
                </li>
              </ul>
            </li>
            <li class="has-dropdown"><a href="brands.html">Производители</a><ul class="sub-menu">{manu_items}</ul></li>
            <li class="has-dropdown mega-parent"><a href="tags.html">Отрасли</a>
              <ul class="sub-menu bep-mega bep-mega--tags">
                <li>
                  <div class="bep-mega-panel bep-mega-panel--tags">
                    {tag_cols}
                    <div class="bep-tags-mega-foot">
                      {tag_type_link}
                      <a class="bep-tags-mega-all" href="tags.html">
                        <span>Все {len(TAG_INDUSTRY) + len(TAG_SERIES) + len(TAG_TYPE)} тегов: отрасли, серии и подборки</span>
                        <i class="tji-arrow-right-long"></i>
                      </a>
                    </div>
                  </div>
                </li>
              </ul>
            </li>
            <li><a href="#process">Как мы работаем</a></li>
            <li><a href="#contacts">Контакты</a></li>
          </ul>
        </nav>
      </div>

      <div class="header-right">
        <button class="bep-icon-btn" data-open-search aria-label="Поиск по каталогу"><i class="tji-search"></i></button>
        <a class="bep-header-phone d-none d-xl-inline-flex" href="{PHONE_HREF}"><i class="tji-phone"></i>{PHONE}</a>
        <a class="tj-primary-btn header-btn d-none d-md-inline-flex" href="#" data-open-modal>
          <span class="btn-text"><span>Заказать звонок</span></span>
          <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
        </a>
        <button class="bep-burger d-lg-none" aria-label="Меню"><span></span><span></span><span></span></button>
      </div>
    </div>
  </div>
</header>
"""


def hero():
    slides = []
    for i, s in enumerate(SLIDES):
        facts = ''.join('<div><b>%s</b><span>%s</span></div>' % f for f in s['facts'])
        slides.append(f"""
        <div class="swiper-slide tj-slider-item">
          <div class="slider-bg-image bep-hero-bg has-photo" style="background-image:linear-gradient(90deg, rgb(var(--bep-ink-rgb) / .97) 0%, rgb(var(--bep-ink-rgb) / .93) 28%, rgb(var(--bep-ink-rgb) / .66) 56%, rgb(var(--bep-ink-rgb) / .3) 100%), linear-gradient(180deg, rgb(var(--bep-ink-rgb) / .35), rgb(var(--bep-ink-rgb) / .12)), url('{s['photo']}')"></div>
          <div class="container">
            <div class="slider-wrapper">
              <div class="slider-content">
                <h1 class="slider-title">{s['title']}</h1>
                <div class="slider-desc">{s['desc']}</div>
                <div class="bep-hero-actions">
                  {btn(s['cta'], s['cta_href'])}
                  <a class="bep-ghost-btn" href="{s['cta2_href']}">{s['cta2']}</a>
                </div>
                <div class="bep-hero-facts">{facts}</div>
              </div>
            </div>
          </div>
        </div>""")
    thumbs = ''.join('<div class="swiper-slide thumb-item"><img src="%s" alt=""></div>' % s['thumb'] for s in SLIDES)
    return f"""
<section class="tj-slider-section" id="top">
  <div class="swiper hero-slider">
    <div class="swiper-wrapper">{''.join(slides)}</div>
    <div class="hero-navigation d-none d-xl-inline-flex">
      <div class="slider-prev" role="button"><span class="anim-icon"><i class="tji-arrow-left"></i><i class="tji-arrow-left"></i></span></div>
      <div class="slider-next" role="button"><span class="anim-icon"><i class="tji-arrow-right"></i><i class="tji-arrow-right"></i></span></div>
    </div>
  </div>
  <div class="swiper hero-thumb d-none d-lg-block"><div class="swiper-wrapper">{thumbs}</div></div>
  <div class="circle-text-wrap">
    <span class="circle-text" style="background-image:url('assets/img/circle-text.svg')"></span>
    <a class="circle-icon" href="#catalog"><i class="tji-arrow-down-big"></i></a>
  </div>
</section>
"""


def trust():
    tiles = []
    for b in BRANDS:
        tiles.append('<div class="bep-logo-tile"><img src="assets/img/brands/%s.png" alt="%s"></div>' %
                     (b['file'], b['name']))
    for slug, name in PARTNERS:
        tiles.append('<div class="bep-logo-tile"><img src="assets/img/partners/%s.png" alt="%s"></div>' %
                     (slug, name))
    track = ''.join(tiles)
    def card(slug, name):
        return ('<div class="bep-client-card"><img src="assets/img/partners/%s.png" alt="%s"></div>'
                % (slug, name))

    half = (len(PARTNERS) + 1) // 2
    left_cards = ''.join(card(s, n) for s, n in PARTNERS[:half])
    right_cards = ''.join(card(s, n) for s, n in PARTNERS[half:])
    return f"""
<section class="tj-client-section bep-clients">
  <div class="container">
    <div class="bep-clients-row">
      {left_cards}
      <div class="bep-clients-badge">
        <span class="bep-trust-pill"><span>Работаем с <b>9 производителями</b> и более
          <b>15 поставщиками</b> приводной техники</span></span>
      </div>
      {right_cards}
    </div>
  </div>
</section>
"""


def about():
    partner_imgs = ''.join('<li><img src="assets/img/partners/%s.png" alt="%s"></li>' % (s, n) for s, n in PARTNERS)
    return f"""
<section class="tj-about-section section-gap" id="about">
  <div class="container">
    <div class="row row-gap-4">
      <div class="col-lg-4 col-md-6 order-lg-1 order-3" data-count-block>
        <div class="countup-item style-2" data-reveal>
          <span class="count-icon"><i class="tji-box"></i></span>
          <span class="steps">01.</span>
          <div class="count-inner">
            <span class="count-text">Моделей в каталоге</span>
            <div class="inline-content">
              <span class="countup-number" data-count="172">0</span>
            </div>
          </div>
          <div class="bep-about-card-note"><i class="tji-check"></i> Собраны из 17 категорий и 9 брендов</div>
        </div>
      </div>

      <div class="col-lg-8 col-sm-12 order-lg-2 order-1">
        <div class="about-content-area-2">
          <div class="about-content">
            {heading('О компании', 'Приводная техника под задачу: подбор, поставка, ремонт.')}
            <p class="desc" style="max-width:560px;color:var(--tj-color-text-body-3);font-size:16px;line-height:1.65;margin:0 0 22px">
              15 лет поставляем редукторы, мотор-редукторы, вариаторы и электродвигатели на белорусские
              и российские производства. Работаем с 15 поставщиками — поэтому подбираем не «что есть»,
              а то, что нужно оборудованию.
            </p>
            {text_btn('Как мы работаем', '#process')}
          </div>
          <div class="video-img">
            <img class="bep-about-img" src="assets/img/prod/bep-1271.png" alt="Конический редуктор BEP-1271">
          </div>
        </div>
      </div>

      <div class="col-lg-4 col-md-6 order-lg-3 order-2">
        <div class="customers-box style-2" data-reveal>
          <div class="customers-bg" style="background:linear-gradient(150deg,var(--bep-accent),var(--bep-accent-dark))"></div>
          <div class="customers">
            <ul class="bep-customers-logos">{partner_imgs}
              <li class="is-plus"><i class="tji-plus"></i></li>
            </ul>
          </div>
          <h6 class="customers-text">Более 15 поставщиков — подберём аналог под задачу.</h6>
          <div class="star-icon zoomInOut"><img src="assets/img/star.svg" alt=""></div>
        </div>
      </div>

      <div class="col-lg-4 col-md-6 order-lg-4 order-4">
        <div class="countup-item style-2" data-reveal>
          <span class="count-icon"><i class="tji-team"></i></span>
          <span class="steps">02.</span>
          <div class="count-inner">
            <span class="count-text">Производителей</span>
            <div class="inline-content"><span class="countup-number" data-count="9">0</span></div>
          </div>
          <div class="bep-about-card-note"><i class="tji-check"></i> NORD, Motovario, Brevini, ЧЗР и др.</div>
        </div>
      </div>

      <div class="col-lg-4 col-md-6 order-lg-5 order-5">
        <div class="countup-item style-2" data-reveal>
          <span class="count-icon"><i class="tji-growth"></i></span>
          <span class="steps">03.</span>
          <div class="count-inner">
            <span class="count-text">Лет на рынке приводов</span>
            <div class="inline-content"><span class="countup-number" data-count="15">0</span></div>
          </div>
          <div class="bep-about-card-note"><i class="tji-check"></i> 4 офиса и склада: Беларусь и Россия</div>
        </div>
      </div>
    </div>
  </div>
</section>
"""


def catalog():
    cards = []
    for c in CATS:
        top = ' · '.join(c['top'])
        cards.append(f"""
        <article class="bep-cat-card">
          <div class="bep-cat-top">
            <span class="bep-cat-icon"><img src="{cat_img(c['slug'])}" alt="{c['name']}" loading="lazy"></span>
            <span class="bep-cat-badge">{models(c['n'])}</span>
          </div>
          <h4 class="bep-cat-name"><a href="{SITE}/category/{c['slug']}" target="_blank" rel="noopener">{c['name']}</a></h4>
          <p class="bep-cat-desc">{c['desc']}</p>
          <p class="bep-cat-models">{top}</p>
        </article>""")
    rest = ', '.join('%s (%d)' % (n, cnt) for _, n, cnt in OTHER_CATS)
    return f"""
<section class="tj-service-section service-2 section-gap" id="catalog">
  <div class="container">
    <div class="row">
      <div class="col-lg-4">
        <div class="content-wrap">
          {heading('Каталог', 'Восемь категорий, которые закрывают 138 из 172 позиций.')}
          <p class="desc" style="color:var(--tj-color-text-body-2);font-size:15px;line-height:1.6;margin:18px 0 26px;max-width:340px">
            Плюс {rest}. Не нашли нужное — инженер подберёт по параметрам оборудования.
          </p>
          <div>{btn('Все 17 категорий', 'catalog.html')}</div>
        </div>
      </div>
      <div class="col-lg-8">
        <div class="bep-cat-grid">{''.join(cards)}</div>
      </div>
    </div>
  </div>
  <div class="bg-shape-1"><img src="assets/img/pattern-2.svg" alt=""></div>
  <div class="bg-shape-2"><img src="assets/img/pattern-3.svg" alt=""></div>
</section>
"""


def products():
    slides = []
    for img, slug, name, cat in PRODUCTS_FEATURED:
        slides.append(f"""
        <div class="swiper-slide">
          <a class="bep-card" href="product/{safe_slug(slug)}.html">
            <div class="bep-card-img"><img src="assets/img/prod/{img}.png" alt="{name}" loading="lazy"></div>
            <div class="bep-card-body">
              <span class="bep-card-cat">{cat}</span>
              <b class="bep-card-name">{name}</b>
              <span class="bep-card-link">Смотреть позицию <i class="tji-arrow-right-long"></i></span>
            </div>
          </a>
        </div>""")
    return f"""
<section class="tj-project-section-2 section-gap" id="products">
  <div class="container">
    <div class="row">
      <div class="col-12">
        {heading('Каталог в наличии', 'Популярные позиции — <span>и ещё 160 моделей.</span>', center=True)}
      </div>
    </div>
  </div>
  <div class="container-fluid">
    <div class="row"><div class="col-12">
      <div class="project-wrapper">
        <div class="swiper project-slider"><div class="swiper-wrapper">{''.join(slides)}</div></div>
      </div>
    </div></div>
  </div>
</section>
"""


def process():
    items = ''.join(f"""
      <div class="process-item" data-reveal>
        <div class="process-step"><span>{i:02d}</span></div>
        <div class="process-content">
          <h4 class="title">{t}</h4>
          <p class="desc">{d}</p>
        </div>
      </div>""" for i, (t, d) in enumerate(STEPS, 1))
    return f"""
<section class="tj-working-process section-gap section-gap-x" id="process">
  <div class="container">
    <div class="row"><div class="col-12">
      <div class="sec-heading-wrap">
        <span class="sub-title">Как мы работаем</span>
        <div class="heading-wrap-content">
          {heading('', 'От заявки до пуска — <span>четыре шага.</span>')}
          <p class="desc">Подбор по параметрам оборудования, поставка со склада или под заказ, помощь с пуском и ремонтом.</p>
          <div class="btn-wrap">{btn('Запросить подбор', '#contacts')}</div>
        </div>
      </div>
    </div></div>
    <div class="row"><div class="col-12">
      <div class="working-process-area">{items}</div>
    </div></div>
  </div>
  <div class="bg-shape-1"><img src="assets/img/pattern-2.svg" alt=""></div>
</section>
"""


def testimonial():
    return f"""
<section class="tj-testimonial-section-2 section-gap">
  <div class="container">
    <div class="row row-gap-3">
      <div class="col-lg-6">
        <div class="testimonial-img-area">
          <div class="bep-testi-visual">
            <div class="bep-testi-art-wrap" role="img" aria-label="Конвейерная линия на производстве"></div>
            {heading('Руководитель о работе', 'Слово <span>руководителя.</span>')}
          </div>
          <div class="box-area">
            <div class="rating-box bep-rating-box">
              <h2 class="title">15</h2>
              <div class="rating-area"><span class="rating-text" style="font-size:15px">лет на рынке приводной техники</span></div>
              <span class="rating-text">4 офиса · 172 модели · 15 поставщиков</span>
            </div>
          </div>
        </div>
      </div>
      <div class="col-lg-6">
        <div class="testimonial-wrapper">
          <div class="swiper testimonial-slider-2">
            <div class="swiper-wrapper">
              <div class="swiper-slide">
                <div class="testimonial-item">
                  <span class="quote-icon"><i class="tji-quote"></i></span>
                  <div class="desc"><p>{QUOTE}</p></div>
                  <div class="testimonial-author">
                    <div class="author-inner">
                      <div class="author-img"><img src="assets/img/logo-mark-orange.png" alt="" style="padding:10px;object-fit:contain"></div>
                      <div class="author-header">
                        <h4 class="title">Сергей Николаевич</h4>
                        <span class="designation">руководитель компании «БелЕвропривод»</span>
                      </div>
                    </div>
                  </div>
                  <div class="bep-quote-facts">
                    <div><b>15 лет</b><span>на рынке приводов</span></div>
                    <div><b>172</b><span>модели в каталоге</span></div>
                    <div><b>4</b><span>офиса и склада</span></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
"""


def brands():
    cards = ''.join(f"""
      <div class="col-lg-3 col-sm-6">
        <div class="team-item bep-brand-card">
          <div class="team-img">
            <div class="team-img-inner"><img src="assets/img/brands/{b['file']}.png" alt="{b['name']}"></div>
          </div>
          <div class="team-content">
            <div>
              <h4 class="title"><a href="catalog.html?maker={b['slug']}">{b['name']}</a></h4>
              <span class="designation">{models(b['n'])} в каталоге</span>
            </div>
            <a class="mail-at" href="catalog.html?maker={b['slug']}"><i class="tji-arrow-right-long"></i></a>
          </div>
        </div>
      </div>""" for b in BRANDS)
    return f"""
<section class="tj-team-section section-separator" id="brands">
  <div class="container">
    <div class="row"><div class="col-12">
      {heading('Производители', 'Восемь брендов <span>в наличии и под заказ.</span>', center=True)}
    </div></div>
    <div class="row row-gap-4">{cards}</div>
    <p class="bep-brands-note">Девятый производитель в списке сайта — SEW Eurodrive: в каталоге пока нет
      ни одной позиции, поставляем под заказ по запросу.</p>
  </div>
</section>
"""


def terms():
    plans = [
        dict(name='Со склада', desc='Ходовые позиции в Колодищах', num='1', period='/ день — отгрузка',
             cta='Запросить наличие',
             items=['Наличие на складе в Минском районе',
                    'Самовывоз или доставка по Минску',
                    'Отгрузка в день заказа',
                    'Полный пакет документов: ТТН, счёт, сертификаты']),
        dict(name='Под заказ', desc='15 поставщиков и 9 производителей', num='15', period='/ поставщиков', active=True,
             cta='Отправить заявку',
             items=['Подбор по моменту, оборотам и монтажу',
                    'Чертежи и характеристики до оплаты',
                    'Поставка по Беларуси и в Россию',
                    'Аналоги снятых с производства серий']),
        dict(name='Ремонт и сервис', desc='Редукторы и мотор-редукторы', num='4', period='/ офиса и склада',
             cta='Обсудить ремонт',
             items=['Диагностика и дефектовка редуктора',
                    'Запчасти NMRV: валы, фланцы, тяги',
                    'Помощь с пуском и обслуживанием',
                    'Сопровождение на объекте в Минске']),
    ]
    cards = ''.join(f"""
      <div class="col-xl-4 col-md-6">
        <div class="pricing-box{' active' if p.get('active') else ''}" data-reveal>
          <div class="pricing-header">
            <h4 class="package-name">{p['name']}</h4>
            <div class="package-desc"><p>{p['desc']}</p></div>
            <div class="package-price">
              <span class="price-number">{p['num']}</span>
              <span class="package-period">{p['period']}</span>
            </div>
            <div class="pricing-btn">{text_btn(p['cta'], '#contacts')}</div>
          </div>
          <div class="list-items"><ul>{''.join('<li><i class="tji-list"></i>%s</li>' % i for i in p['items'])}</ul></div>
        </div>
      </div>""" for p in plans)
    return f"""
<section class="tj-pricing-section section-gap">
  <div class="container">
    <div class="row"><div class="col-12">
      {heading('Условия работы', 'Три сценария <span>поставки.</span>', center=True)}
    </div></div>
    <div class="row row-gap-4">{cards}</div>
    <p class="bep-brands-note">Девятый производитель в списке сайта — SEW Eurodrive: в каталоге пока нет
      ни одной позиции, поставляем под заказ по запросу.</p>
  </div>
</section>
"""


def industries():
    from urllib.parse import quote
    label = {'Сельское хозяйство': 'Сельхозтехника',
             'Коммунальная и дорожная техника': 'Коммунальная и дорожная техника',
             'Конвейеры, станки, подъёмники': 'Конвейеры и станки',
             'Тяжёлая и химическая промышленность': 'Тяжёлая, лёгкая и химическая пром.',
             'Пищевая промышленность': 'Пищевая промышленность',
             'Лесное хозяйство и добыча': 'Лесное хозяйство'}
    cards = ''.join(f"""
      <div class="swiper-slide">
        <a class="blog-item style-2 bep-industry-card" href="catalog.html?tag={quote(label.get(name, name))}">
          <div class="blog-thumb"><img src="{img}" alt="{name}"></div>
          <div class="blog-content">
            <div class="title-area">
              <div class="blog-meta"><span class="categories"><span>Отрасль</span></span></div>
              <h4 class="title">{name}</h4>
              <p style="font-size:13.5px;line-height:1.5;color:var(--tj-color-text-body-3);margin:8px 0 0">{desc}</p>
            </div>
            <span class="text-btn"><span class="btn-text"><span>Смотреть подборку</span></span>
              <span class="btn-icon"><i class="tji-arrow-right-long"></i></span></span>
          </div>
        </a>
      </div>""" for name, desc, _, img in INDUSTRIES)
    return f"""
<section class="tj-blog-section-2 section-gap" id="industries">
  <div class="container">
    <div class="row"><div class="col-12">
      <div class="sec-heading-wrap">
        <span class="sub-title">Отрасли</span>
        <div class="heading-wrap-content">
          {heading('', 'Где работают <span>наши приводы.</span>')}
          <div><p class="desc">Подборки по назначению: от сельхозтехники до пищевого производства.</p></div>
          <div class="slider-navigation d-none d-md-inline-flex" id="blog-nav">
            <div class="slider-prev" role="button"><span class="anim-icon"><i class="tji-arrow-left"></i><i class="tji-arrow-left"></i></span></div>
            <div class="slider-next" role="button"><span class="anim-icon"><i class="tji-arrow-right"></i><i class="tji-arrow-right"></i></span></div>
          </div>
        </div>
      </div>
    </div></div>
    <div class="row"><div class="col-12">
      <div class="blog-wrapper">
        <div class="swiper blog-slider"><div class="swiper-wrapper">{cards}</div></div>
      </div>
      <div class="bep-industries-more">
        <a href="tags.html">Все {len(TAG_INDUSTRY)} отраслей и {len(TAG_INDUSTRY) + len(TAG_SERIES) + len(TAG_TYPE)} тегов — с описаниями и подборками
          <i class="tji-arrow-right-long"></i></a>
      </div>
    </div></div>
  </div>
</section>
"""


def footer():
    offices = ''.join(
        '<li><b><a href="%s%s" target="_blank" rel="noopener" style="color:#fff;text-decoration:none">%s</a></b>'
        '<span>%s</span><span>%s</span></li>' % (YANDEX, o[3], o[0], o[1], o[2]) for o in OFFICES)
    cat_links = ''.join('<li><a href="category/%s.html">%s</a></li>' %
                        (c['slug'], c['name']) for c in CATS[:6])
    tag_chips = ''.join('<a href="%s">%s <i>%d</i></a>' %
                        (tags_data.catalog_href(t), esc(t['short']), t['count'])
                        for t in TAG_INDUSTRY)
    marquee_words = ['Редукторы', 'Мотор-редукторы', 'Вариаторы', 'Электродвигатели',
                     'Коробки передач', 'Цепи', 'Запчасти NMRV']
    marquee = ''.join(
        '<div class="swiper-slide marquee-item"><h4 class="marquee-text">%s</h4>'
        '<div class="marquee-img"><img src="assets/img/prod/%s.png" alt=""></div></div>' %
        (w, ['nmrv-chervyachny', 'k-seriya', 'rt500', 'rc', 'korobka-bep00153', 'f-seriya', 'r-seriya'][i % 7])
        for i, w in enumerate(marquee_words * 2))
    return f"""
<footer class="tj-footer-section footer-2 section-gap-x" id="contacts">
  <div class="footer-top">
    <div class="container">
      <div class="row"><div class="col-12">
        <div class="footer-subscribe">
          <div class="subscribe-logo">
            <img src="assets/img/logo-mark-white.png" alt="БелЕвропривод" style="width:56px;height:56px">
          </div>
          <div style="max-width:420px">
            <h4 style="color:#fff;font-size:22px;margin:0 0 6px">Подберём привод под вашу задачу</h4>
            <p style="color:rgba(255,255,255,.55);font-size:13.5px;margin:0">Инженер перезвонит и уточнит параметры оборудования.</p>
          </div>
          <div class="subscribe-form" style="flex:1;min-width:320px">
            <form data-bep-form>
              <div class="bep-form-row" style="grid-template-columns:1fr 1fr;display:grid;gap:10px">
                <input type="text" name="name" placeholder="Ваше имя" autocomplete="name">
                <input type="tel" name="phone" placeholder="+375 (__) ___-__-__" autocomplete="tel" inputmode="tel">
              </div>
              <div class="bep-form-error" style="margin:6px 0 8px"></div>
              <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">
                {btn_submit('Отправить заявку')}
                <span style="font-size:12px;color:rgba(255,255,255,.45)">Нажимая кнопку, вы соглашаетесь на обработку данных</span>
              </div>
              <div class="bep-form-ok">Спасибо! Заявка отправлена — свяжемся в рабочее время.</div>
            </form>
          </div>
        </div>
      </div></div>
    </div>
  </div>

  <div class="footer-main-area">
    <div class="container">
      <div class="row justify-content-between">
        <div class="col-xl-3 col-md-6">
          <div class="footer-widget footer-col-1">
            <div class="footer-logo">
              <a href="#top" style="display:flex;align-items:center;gap:10px;text-decoration:none">
                <img src="assets/img/logo-mark-white.png" alt="БелЕвропривод" style="width:34px;height:34px">
                <span style="color:#fff;font-weight:700;font-size:18px">БелЕвропривод</span>
              </a>
            </div>
            <div class="footer-text">
              <p>Машиностроительное оборудование: редукторы, мотор-редукторы, вариаторы,
                 электродвигатели. 15 лет на рынке, 172 модели в каталоге.</p>
            </div>
            <div class="footer-text">
              <p style="margin:0 0 18px">{ADDRESS}<br>{UNP}</p>
            </div>
          </div>
        </div>
        <div class="col-xl-3 col-md-6">
          <div class="footer-widget footer-col-2 widget-nav-menu">
            <h5 class="title">Каталог</h5>
            <ul>{cat_links}<li><a href="catalog.html">Все 17 категорий</a></li></ul>
          </div>
        </div>
        <div class="col-xl-3 col-md-6">
          <div class="footer-widget footer-col-2 widget-nav-menu">
            <h5 class="title">Офисы и склады</h5>
            <ul class="bep-office-list">{offices}</ul>
          </div>
        </div>
        <div class="col-xl-3 col-md-6">
          <div class="footer-widget widget-contact">
            <h5 class="title">Связаться</h5>
            <div class="footer-contact-info">
              <div class="contact-item">
                <a href="{PHONE_HREF}">P: {PHONE}</a>
                <a href="tel:+375296815205">P: {PHONE_ALT[0]}</a>
                <a href="tel:+375173747454">P: {PHONE_ALT[1]}</a>
                <a href="mailto:{EMAIL}">M: {EMAIL}</a>
              </div>
              <div class="contact-item"><span><i class="tji-clock"></i> Пн–Пт, 9:00–18:00</span></div>
              <div class="contact-item"><span>Самовывоз со склада в Колодищах</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="footer-tags">
    <div class="container">
      <div class="footer-tags-head">
        <h5 class="footer-tags-title">Продукты по назначению</h5>
        <a class="footer-tags-all" href="tags.html">Все отрасли и теги <i class="tji-arrow-right-long"></i></a>
      </div>
      <div class="footer-tags-list">{tag_chips}</div>
    </div>
  </div>

  <div class="footer-marquee">
    <div class="swiper marquee-slider"><div class="swiper-wrapper">{marquee}</div></div>
  </div>

  <div class="tj-copyright-area-2">
    <div class="container">
      <div class="row">
        <div class="col-md-6">
          <div class="copyright-text"><p>© БелЕвропривод, 2026 — машиностроительное оборудование</p></div>
        </div>
        <div class="col-md-6">
          <div class="copyright-text text-md-end">
            <p>{ADDRESS} · {UNP}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</footer>
"""


def overlays():
    mega = []
    for c in CATS:
        mega.append('<li><a href="category/%s.html">%s <span style="opacity:.5">· %d</span></a></li>'
                    % (c['slug'], c['name'], c['n']))
    for s, n, cnt in OTHER_CATS:
        mega.append('<li><a href="category/%s.html">%s <span style="opacity:.5">· %d</span></a></li>'
                    % (s, n, cnt))
    mobile_tags = ''.join('<li><a href="%s">%s <span style="opacity:.5">· %d</span></a></li>'
                          % (tags_data.catalog_href(t), esc(t['short']), t['count'])
                          for t in TAG_INDUSTRY + TAG_SERIES)
    return f"""
<div class="bep-search" id="bep-search" role="dialog" aria-label="Поиск по каталогу">
  <div class="bep-search-inner">
    <div class="bep-search-field">
      <i class="tji-search"></i>
      <input id="bep-search-input" type="search" placeholder="Название модели или категория: NMRV, RT500, планетарный…" autocomplete="off">
      <button class="bep-icon-btn bep-search-close" style="color:var(--bep-text);border-color:var(--bep-line)" aria-label="Закрыть"><i class="tji-plus" style="transform:rotate(45deg)"></i></button>
    </div>
    <div class="bep-search-hint" id="bep-search-hint"></div>
    <div class="bep-search-results" id="bep-search-results"></div>
  </div>
</div>

<div class="bep-modal" id="bep-modal" role="dialog" aria-label="Заказать звонок">
  <div class="bep-modal-card">
    <button class="bep-modal-close" aria-label="Закрыть"><i class="tji-plus" style="transform:rotate(45deg)"></i></button>
    <h3>Заказать звонок</h3>
    <p class="bep-modal-sub">Инженер перезвонит в рабочее время и подберёт привод под задачу.</p>
    <form data-bep-form>
      <div class="bep-form-row">
        <input type="text" name="name" placeholder="Ваше имя" autocomplete="name">
        <input type="tel" name="phone" placeholder="+375 (__) ___-__-__" autocomplete="tel" inputmode="tel">
        <textarea name="comment" placeholder="Что нужно подобрать? Например: мотор-редуктор для конвейера, 1,5 кВт"></textarea>
      </div>
      <div class="bep-form-error"></div>
      {btn_submit('Отправить заявку')}
      <div class="bep-form-ok">Спасибо! Заявка отправлена — свяжемся в рабочее время.</div>
    </form>
  </div>
</div>

<div class="bep-mobile-panel" id="bep-mobile">
  <div class="bep-mobile-head">
    <a class="bep-logo" href="#top">
      <img src="assets/img/logo-mark-teal.png" alt="БелЕвропривод">
      <span class="bep-logo-text">БелЕвропривод</span>
    </a>
    <button class="bep-mobile-close" aria-label="Закрыть"><i class="tji-plus" style="transform:rotate(45deg)"></i></button>
  </div>
  <ul>
    <li><a href="catalog.html">Каталог</a>
      <ul class="bep-mobile-sub">{''.join(mega[:10])}</ul>
    </li>
    <li><a href="brands.html">Производители</a></li>
    <li><a href="#products">Популярные позиции</a></li>
    <li><a href="#process">Как мы работаем</a></li>
    <li><a href="tags.html">Отрасли</a>
      <ul class="bep-mobile-sub">{mobile_tags}</ul>
    </li>
    <li><a href="#contacts">Контакты</a></li>
  </ul>
  <div class="bep-mobile-contacts">
    <a href="{PHONE_HREF}"><i class="tji-phone"></i> {PHONE}</a>
    <a href="mailto:{EMAIL}"><i class="tji-envelop"></i> {EMAIL}</a>
    <span style="color:rgba(255,255,255,.55);font-size:13px">{ADDRESS}</span>
    <button class="tj-primary-btn" data-open-modal style="margin-top:8px">
      <span class="btn-text"><span>Заказать звонок</span></span>
      <span class="btn-icon"><i class="tji-arrow-right-long"></i></span>
    </button>
  </div>
</div>

<button class="bep-progress" aria-label="Наверх">
  <svg viewBox="0 0 64 64"><circle class="track" cx="32" cy="32" r="28"></circle>
    <circle class="bar" cx="32" cy="32" r="28"></circle></svg>
  <span class="bep-progress-label">0%</span>
</button>
"""


def search_index(prefix=''):
    idx = []
    for p in PRODUCTS:
        cat = p.get('cat') or 'Каталог'
        slug = p.get('catslug') or ''
        img = cat_img(slug) if os.path.exists(os.path.join(HERE, cat_img(slug))) else cat_img('drugoe')
        idx.append({'n': p['h1'] or p['title'].split(' - ')[0], 'c': cat,
                    'u': '%sproduct/%s.html' % (prefix, safe_slug(p['slug'])), 'i': prefix + img})
    idx.sort(key=lambda x: x['n'])
    return json.dumps(idx, ensure_ascii=False, separators=(',', ':'))


def page():
    return f"""<!DOCTYPE html>
<html lang="ru" data-accent="teal">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>БелЕвропривод — редукторы, мотор-редукторы и электродвигатели в Беларуси</title>
<meta name="description" content="Продажа и ремонт редукторов, мотор-редукторов, вариаторов и электродвигателей. 172 модели, 17 категорий, 9 производителей. Склад в Минске, офисы в Туле и Смоленске.">
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
<body>
{header()}
<main>
{hero()}
{trust()}
{about()}
{catalog()}
{products()}
{process()}
{testimonial()}
{brands()}
{terms()}
{industries()}
</main>
{footer()}
{overlays()}
<script>window.BEP_PRODUCTS = {search_index()};</script>
<script src="assets/js/swiper-bundle.min.js"></script>
<script src="assets/js/main.js"></script>
</body>
</html>
"""


if __name__ == '__main__':
    html = page()
    out = os.path.join(HERE, 'index.html')
    open(out, 'w', encoding='utf-8').write(html)
    print('written', out, len(html), 'bytes')
