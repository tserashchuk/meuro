#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Снимок страниц /product-tag/<slug> с сайта клиента → data/tags.json."""
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://beleuroprivod.by'
CAT = json.load(open(os.path.join(HERE, 'data', 'catalog.json'), encoding='utf-8'))

SLUGS = []
for p in CAT:
    for n, s in zip(p.get('tags') or [], p.get('tag_slugs') or []):
        if s not in SLUGS:
            SLUGS.append(s)


def fetch(url):
    out = subprocess.run(['curl', '-sS', '-m', '40', url], capture_output=True)
    return out.stdout.decode('utf-8', 'replace')


def strip(t):
    t = re.sub(r'<script.*?</script>', '', t, flags=re.S)
    t = re.sub(r'<style.*?</style>', '', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = t.replace('&quot;', '"').replace('&nbsp;', ' ').replace('&amp;', '&')
    return re.sub(r'\s+', ' ', t).strip()


tags = []
for slug in SLUGS:
    html = fetch('%s/product-tag/%s' % (SITE, slug))
    if 'Not Found' in html[:400]:
        print('404', slug)
        continue
    title = re.search(r'<title>(.*?)</title>', html, re.S)
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    lead = ''
    if h1:
        after = html[h1.end():]
        m = re.search(r'<p[^>]*>(.*?)</p>', after, re.S)
        if m:
            lead = strip(m.group(1))
    labels = {s: n for p in CAT for n, s in zip(p.get('tags') or [], p.get('tag_slugs') or [])}
    mine = sum(1 for p in CAT if slug in (p.get('tag_slugs') or []))
    tags.append(dict(slug=slug, name=labels.get(slug, slug),
                     title=title.group(1).strip() if title else '',
                     h1=strip(h1.group(1)) if h1 else '',
                     lead=lead[:400],
                     catalog_count=mine,
                     url='%s/product-tag/%s' % (SITE, slug)))
    print(slug, mine, '|', (tags[-1]['lead'] or '')[:70])

out = os.path.join(HERE, 'data', 'tags.json')
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w', encoding='utf-8') as f:
    json.dump(tags, f, ensure_ascii=False, indent=1)
print('saved', len(tags), '→', out, os.path.getsize(out), 'bytes')
