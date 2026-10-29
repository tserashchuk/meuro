#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Скачивает первый чертёж каждого товара в локальную галерею (720 px, JPEG)."""
import json
import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DET_PATH = os.path.join(HERE, 'data', 'details.json')
RAW = os.path.expanduser('~/.hermes/cache/scratch/drawings')
OUT = os.path.join(HERE, 'assets', 'img', 'drawings')
os.makedirs(RAW, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

det = json.load(open(DET_PATH, encoding='utf-8'))
jobs = [(slug, d['drawings'][0]) for slug, d in det.items() if d.get('drawings')]
print('products with drawings:', len(jobs))


def fetch(item):
    slug, url = item
    raw = os.path.join(RAW, re.sub(r'[^A-Za-z0-9._-]', '_', slug) + '.png')
    if os.path.exists(raw) and os.path.getsize(raw) > 2000:
        return slug, raw
    p = subprocess.run(['curl', '-sSL', '--max-time', '40', '-A', 'Mozilla/5.0 Chrome/120',
                        url, '-o', raw], capture_output=True)
    return (slug, raw if p.returncode == 0 and os.path.exists(raw) else None)


with ThreadPoolExecutor(8) as ex:
    got = dict(ex.map(fetch, jobs))

ok = 0
for slug, raw in got.items():
    if not raw:
        continue
    try:
        im = Image.open(raw).convert('RGBA')
        im.thumbnail((760, 760), Image.LANCZOS)
        canvas = Image.new('RGB', im.size, 'white')
        canvas.paste(im, (0, 0), im)
        canvas.save(os.path.join(OUT, slug + '.jpg'), quality=84, optimize=True, progressive=True)
        det[slug]['drawing_local'] = 'assets/img/drawings/%s.jpg' % slug
        ok += 1
    except Exception as e:
        print('skip', slug, str(e)[:70])

json.dump(det, open(DET_PATH, 'w', encoding='utf-8'), ensure_ascii=False)
total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
print('saved:', ok, 'MB:', round(total / 1e6, 2))
