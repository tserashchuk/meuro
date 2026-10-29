#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерация фотографий для hero-слайдера и карточки отзыва (Gemini image API).
Ключ берётся из ~/.hermes/.env (GOOGLE_API_KEY), в консоль не печатается."""
import base64
import json
import os
import subprocess
import sys

ENV = os.path.expanduser('~/.hermes/.env')
KEY = None
for line in open(ENV, encoding='utf-8', errors='ignore'):
    if line.strip().startswith('GOOGLE_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
        break
if not KEY:
    sys.exit('GOOGLE_API_KEY не найден в ~/.hermes/.env')

MODEL = 'gemini-3.1-flash-image'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'img', 'hero')
os.makedirs(OUT, exist_ok=True)

STYLE = (' фотorealistic editorial photography, cinematic lighting, deep shadows, '
         'warm amber accents, professional B2B industrial mood, no text, no logos, no watermarks, '
         'no readable labels, no people faces in focus, not a product cutout on white')

JOBS = {
    'slide-1': 'Wide view of a modern industrial production hall: long rows of conveyor lines and '
               'stainless machinery receding into the distance, dusk, warm light pools on the floor' + STYLE,
    'slide-2': 'Industrial drive assembly bolted to a machine frame inside a heavy machinery workshop: '
               'electric motor coupled to a gearbox, cables, oiled steel, control cabinet behind, '
               'light dust in the air, dramatic warm side light' + STYLE,
    'slide-3': 'Inside an industrial spare-parts warehouse: tall pallet racking with plain cardboard '
               'boxes and wooden pallets, a forklift standing in the aisle, warm ceiling lamps, '
               'long perspective' + STYLE,
    'testimonial': 'Conveyor line in a modern factory: steel rollers and a blue frame curving away, '
                   'shallow depth of field, warm highlights on metal, dark background' + STYLE,
}


def post(url, payload):
    proc = subprocess.run(['curl', '-sS', '--max-time', '240', '-X', 'POST', url,
                           '-H', 'Content-Type: application/json', '--data-binary', '@-'],
                          input=json.dumps(payload).encode(), capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode()[:300])
    return json.loads(proc.stdout.decode())


def generate(prompt, aspect='1:1', model=MODEL):
    url = ('https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s'
           % (model, KEY))
    payload = {
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {
            'responseModalities': ['IMAGE'],
            'imageConfig': {'aspectRatio': aspect},
        },
    }
    try:
        data = post(url, payload)
    except Exception:
        payload['generationConfig'].pop('imageConfig', None)
        data = post(url, payload)
    if 'error' in data:
        raise RuntimeError(json.dumps(data['error'])[:300])
    for cand in data.get('candidates', []):
        for part in cand.get('content', {}).get('parts', []):
            if 'inlineData' in part:
                return base64.b64decode(part['inlineData']['data'])
    raise RuntimeError('нет изображения в ответе: ' + json.dumps(data)[:300])


for name, prompt in JOBS.items():
    try:
        raw = generate(prompt)
        path = os.path.join(OUT, name + '.png')
        open(path, 'wb').write(raw)
        print('OK', name, len(raw) // 1024, 'KB ->', path)
    except Exception as e:
        print('FAIL', name, str(e)[:220])
