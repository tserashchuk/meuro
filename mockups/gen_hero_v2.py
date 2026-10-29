#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hero-фото для БелЕвропривода: чистые производства + реальный продукт в кадре.
Продукт передаётся в модель как референс (image-to-image), ключ — из ~/.hermes/.env."""
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
    sys.exit('нет GOOGLE_API_KEY')

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = 'gemini-3.1-flash-image'
OUT = os.path.join(HERE, 'assets', 'img', 'hero')
os.makedirs(OUT, exist_ok=True)

BASE = ('Photorealistic wide interior photograph of a CLEAN, TIDY, well-lit modern production facility: '
        'smooth floors, organised equipment, no clutter, no dirt. Place the industrial gearmotor from the '
        'reference image into the scene as a real mounted machine element in the foreground — keep its exact '
        'shape, colour and proportions, add realistic perspective, contact shadows and mounting frame. '
        'Cool neutral daylight with a subtle teal accent, professional B2B editorial photography, '
        'shallow depth of field. No text, no logos, no watermarks, no readable labels, no cutout on white.')

JOBS = {
    'slide-1': ('assets/img/prod/k-seriya.png',
                BASE + ' Scene: a spacious assembly hall with a conveyor line running into the distance; '
                        'the gearmotor is mounted at the drive end of the conveyor.'),
    'slide-2': ('assets/img/prod/nmrv-chervyachny.png',
                BASE + ' Scene: a clean machine shop with stainless frames and a workbench; '
                        'the worm gearmotor sits bolted to a steel frame in the foreground, close-up.'),
    'slide-3': ('assets/img/prod/rt500.png',
                BASE + ' Scene: a bright modern spare-parts warehouse with racking and pallets; '
                        'the gear unit stands on a wooden pallet in the aisle, labels blurred.'),
    'testimonial': ('assets/img/prod/f-seriya.png',
                    BASE + ' Scene: close-up of a workshop bench; the gear unit rests on the bench with '
                            'tools slightly out of focus behind it, dark moody background.'),
}


def post(url, payload):
    proc = subprocess.run(['curl', '-sS', '--max-time', '240', '-X', 'POST', url,
                           '-H', 'Content-Type: application/json', '--data-binary', '@-'],
                          input=json.dumps(payload).encode(), capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode()[:300])
    return json.loads(proc.stdout.decode())


def generate(prompt, ref_path, aspect='16:9'):
    ref = base64.b64encode(open(ref_path, 'rb').read()).decode()
    payload = {
        'contents': [{'parts': [
            {'inlineData': {'mimeType': 'image/png', 'data': ref}},
            {'text': prompt},
        ]}],
        'generationConfig': {
            'responseModalities': ['IMAGE'],
            'imageConfig': {'aspectRatio': aspect},
        },
    }
    url = ('https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s'
           % (MODEL, KEY))
    data = post(url, payload)
    if 'error' in data:
        raise RuntimeError(json.dumps(data['error'])[:300])
    for cand in data.get('candidates', []):
        for part in cand.get('content', {}).get('parts', []):
            if 'inlineData' in part:
                return base64.b64decode(part['inlineData']['data'])
    raise RuntimeError('нет картинки в ответе: ' + json.dumps(data)[:300])


for name, (ref, prompt) in JOBS.items():
    try:
        raw = generate(prompt, os.path.join(HERE, ref))
        path = os.path.join(OUT, name + '-v2.png')
        open(path, 'wb').write(raw)
        print('OK', name, len(raw) // 1024, 'KB')
    except Exception as e:
        print('FAIL', name, str(e)[:200])
