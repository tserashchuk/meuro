#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Скачивает и оптимизирует фото всех 172 товаров для страницы каталога."""
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data', 'catalog.json')
RAW = os.path.expanduser('~/.hermes/cache/scratch/prodimg')
OUT = os.path.join(HERE, 'assets', 'img', 'products')
SITE = 'https://beleuroprivod.by'

os.makedirs(RAW, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

rows = json.load(open(DATA, encoding='utf-8'))
jobs = [(r['slug'], SITE + r['img']) for r in rows if r.get('img')]
print('products:', len(jobs))


def fetch(item):
    slug, url = item
    raw = os.path.join(RAW, re.sub(r'[^A-Za-z0-9._-]', '_', slug) + '.img')
    if os.path.exists(raw) and os.path.getsize(raw) > 2000:
        return slug, raw
    p = subprocess.run(['curl', '-sSL', '--max-time', '40', '-A', 'Mozilla/5.0 Chrome/120',
                        url, '-o', raw], capture_output=True)
    if p.returncode != 0:
        return slug, None
    return slug, raw


with ThreadPoolExecutor(8) as ex:
    got = dict(ex.map(fetch, jobs))
print('downloaded:', sum(1 for v in got.values() if v))

ok = 0
for slug, raw in got.items():
    if not raw or not os.path.exists(raw):
        continue
    try:
        im = Image.open(raw)
        im = im.convert('RGBA')
        # обрезаем однотонные поля
        if im.getchannel('A').getextrema()[0] == 255:
            bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
            diff = ImageChops.difference(im, bg).convert('L')
            bbox = diff.point(lambda v: 255 if v > 10 else 0).getbbox()
        else:
            bbox = im.getchannel('A').getbbox()
        if bbox:
            im = im.crop(bbox)
        im.thumbnail((360, 360), Image.LANCZOS)
        canvas = Image.new('RGB', im.size, 'white')
        canvas.paste(im, (0, 0), im)
        canvas.save(os.path.join(OUT, slug + '.jpg'), quality=82, optimize=True, progressive=True)
        ok += 1
    except Exception as e:
        print('skip', slug, str(e)[:80])

print('processed:', ok)
total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
print('total MB:', round(total / 1e6, 2))
