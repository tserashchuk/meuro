#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Разбор карточек товаров: описание, характеристики, документация, чертежи."""
import glob
import html
from html.parser import HTMLParser
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = glob.glob(os.path.expanduser('~/.hermes/cache/scratch/bep/prods/*.html'))
SITE = 'https://beleuroprivod.by'
OUT = os.path.join(HERE, 'data', 'details.json')

ALLOWED = {'p', 'b', 'strong', 'em', 'i', 'u', 'ul', 'ol', 'li', 'br', 'h3', 'h4', 'h5',
           'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'figure', 'figcaption', 'span'}


def clean(s):
    return html.unescape(re.sub(r'\s+', ' ', re.sub('<[^>]+>', '', s or ''))).strip()


class _Sanitizer(HTMLParser):
    """Пропускает только безопасные теги, чистит атрибуты, делает ссылки абсолютными."""

    ALLOWED = {'p', 'b', 'strong', 'em', 'i', 'u', 'ul', 'ol', 'li', 'br', 'h3', 'h4', 'h5',
               'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'figure', 'figcaption'}
    VOID = {'br', 'img'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'iframe', 'form', 'input', 'button', 'select', 'textarea'):
            self.skip += 1
            return
        if self.skip or tag not in self.ALLOWED:
            return
        d = dict(attrs)
        keep = []
        if tag == 'a' and d.get('href'):
            href = d['href']
            if href.startswith('/'):
                href = SITE + href
            keep.append('href="%s"' % html.escape(href))
            keep.append('target="_blank" rel="noopener"')
        if tag == 'img':
            src = d.get('src') or ''
            if not src:
                return
            if src.startswith('/'):
                src = SITE + src
            keep.append('src="%s"' % html.escape(src))
            keep.append('alt="%s"' % html.escape(d.get('alt', '')))
            keep.append('loading="lazy"')
        if tag in ('td', 'th') and d.get('colspan'):
            keep.append('colspan="%s"' % html.escape(d['colspan']))
        self.out.append('<%s%s>' % (tag, (' ' + ' '.join(keep)) if keep else ''))
        if tag in self.VOID:
            pass

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'iframe', 'form', 'input', 'button', 'select', 'textarea'):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip or tag not in self.ALLOWED or tag in self.VOID:
            return
        self.out.append('</%s>' % tag)

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def sanitize(fragment):
    from html.parser import HTMLParser  # noqa: F401  (импорт для ясности)
    p = _Sanitizer()
    p.feed(fragment or '')
    p.close()
    out = ''.join(p.out)
    out = re.sub(r'\n{3,}', '\n\n', out)
    out = re.sub(r'[ \t]{2,}', ' ', out)
    return out.strip()


def pane(h, start_id, next_id=None):
    i = h.find('id="%s"' % start_id)
    if i < 0:
        return ''
    i = h.find('>', i) + 1
    j = h.find('id="%s"' % next_id) if next_id else -1
    if j > 0:
        j = h.rfind('<div', 0, j)
    else:
        j = h.find('<!-- End Tab', i)
        if j < 0:
            j = len(h)
    return h[i:j]


def tables_from(fragment):
    out = []
    for t in re.findall(r'(?is)<table[^>]*>(.*?)</table>', fragment):
        rows = []
        head = []
        th = re.search(r'(?is)<thead[^>]*>(.*?)</thead>', t)
        if th:
            head = [clean(c) for c in re.findall(r'(?is)<th[^>]*>(.*?)</th>', th.group(1))]
            body = t[th.end():]
        else:
            body = t
        for r in re.findall(r'(?is)<tr[^>]*>(.*?)</tr>', body):
            cells = [clean(c) for c in re.findall(r'(?is)<t[hd][^>]*>(.*?)</t[hd]>', r)]
            if not cells:
                continue
            if not head and not rows and all(c and not re.search(r'\d', c) for c in cells):
                head = cells
                continue
            rows.append(cells)
        if head or rows:
            out.append({'head': head, 'rows': rows})
    return out


def images_in(fragment):
    urls = re.findall(r'src="([^"]+)"', fragment)
    res = []
    for u in urls:
        if u.startswith('/'):
            u = SITE + u
        if u not in res:
            res.append(u)
    return res


details = {}
for f in SRC:
    h = open(f, encoding='utf-8', errors='replace').read()
    slug = os.path.basename(f)[:-5]
    desc = pane(h, 'featuresOne', 'featuresTwo')
    specs = pane(h, 'featuresTwo', 'featuresThree')
    docs = pane(h, 'featuresThree', None)

    doc_links = []
    for m in re.finditer(r'(?is)<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', docs):
        url, label = m.group(1), clean(m.group(2))
        if not label:
            continue
        url = url.replace('http://127.0.0.1:8000', SITE)
        url = re.sub(r'^https?://static/', SITE + '/static/', url)
        if url.startswith('/'):
            url = SITE + url
        doc_links.append({'url': url, 'label': label})

    desc_tables = tables_from(desc)
    spec_tables = tables_from(specs)
    # чертежи из описания — в галерею и в текст
    drawing_urls = [u for u in images_in(desc) + images_in(specs) if '/uploads/' in u]
    seen = set()
    drawing_urls = [u for u in drawing_urls if not (u in seen or seen.add(u))]

    details[slug] = {
        'desc_html': sanitize(desc),
        'tables': desc_tables + spec_tables,
        'docs': doc_links,
        'drawings': drawing_urls[:4],
        'has_desc': bool(clean(desc)),
    }

# сохраняем ранее скачанные локальные чертежи, если файл уже был
if os.path.exists(OUT):
    try:
        old = json.load(open(OUT, encoding='utf-8'))
        for slug, d in details.items():
            if slug in old and old[slug].get('drawing_local'):
                d['drawing_local'] = old[slug]['drawing_local']
    except Exception:
        pass

json.dump(details, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print('products:', len(details))
print('with description:', sum(1 for d in details.values() if d['has_desc']))
print('with specs:', sum(1 for d in details.values() if d['tables']))
print('with docs:', sum(1 for d in details.values() if d['docs']))
print('with drawings:', sum(1 for d in details.values() if d['drawings']))
print('size MB:', round(os.path.getsize(OUT) / 1e6, 2))
print(json.dumps({k: v for k, v in list(details.items())[:1]}, ensure_ascii=False)[:600])
