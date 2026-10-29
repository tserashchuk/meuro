#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Собирает интро-тексты категорий с beleuroprivod.by → data/categories.json."""
import json
import os
import re

SRC = os.path.expanduser('~/.hermes/cache/scratch/bep/cats')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'categories.json')


def clean(t):
    t = re.sub(r'<[^>]+>', '', t)
    t = t.replace('&nbsp;', ' ').replace('&laquo;', '«').replace('&raquo;', '»')
    t = t.replace('&mdash;', '—').replace('&ndash;', '–').replace('&amp;', '&')
    t = t.replace('&quot;', '"').replace('&#39;', "'")
    return re.sub(r'\s+', ' ', t).strip()


data = {}
for f in sorted(os.listdir(SRC)):
    if not f.endswith('.html'):
        continue
    slug = f[:-5]
    h = open(os.path.join(SRC, f), encoding='utf-8', errors='ignore').read()
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    lead = re.search(r'<p class="lead"[^>]*>(.*?)</p>', h, re.S)
    data[slug] = {
        'h1': clean(h1.group(1)) if h1 else '',
        'lead': clean(lead.group(1)) if lead else '',
    }
    print(slug, '|', data[slug]['h1'][:60], '|', len(data[slug]['lead']))

json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', OUT, len(data))
