#!/usr/bin/env python3
"""Prepare Beleuroprivod images for the mockup: trim, pad, resize, rename."""
import os, re, json
from PIL import Image, ImageChops

SRC = os.path.expanduser('~/.hermes/cache/scratch/bep_src')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'img')
os.makedirs(OUT, exist_ok=True)

CATS = {
    'chervyachnie_reduktori': '19051808552_nmrv_1_xWTtnja.jpg',
    'tsilindr_soosn_reduktori': 'h-removebg-preview_s2AWAjd.png',
    'konichesko-tsilindricheskie_reductori': 'b-removebg-preview_1_ErfliCe_oidwLTH.png',
    'tsilindr_ploski_reductori': '477_original-removebg-preview_87pW9Dg.png',
    'planetarnie_reductori': 'Brevini_E.jpg',
    'variatori': 'txf-nmrv_oI93pql-removebg-preview_9FKzKA9.png',
    'industrial_reductori': 'qwqw_MDSJqlu.png',
    'electrodvig': 'dvigatel-s-removebg-preview_Shrai10.png',
    'reductori_parral_vali': 'as.png',
    'konichesko-cilindricheskie-gidromotor': 'ssa.png',
    'konicheskie_reduktori': 'Bandioli-S2000_zvY7lzg_5kJ2AvU.jpg',
    'korobki': 'qwqwqw_LEqmXxj.png',
    'reducktorni_balki': '_D0_BF_D0_BE_D0_BF_D0_BE_D1_80-removebg-preview.png',
    'cepi': 'y-removebg-preview.png',
    'cepnie_kolesa': '_D1_83_D0_B2_D1_83_D0_B2.png',
    'drugoe': 'kekeke_KKC1XbH.jpg',
    'zapchasti': 'hjhjhhjhd_06zer5f.png',
}

BRANDS = {
    'nord': 'Nord_Logo_final.jpg',
    'brevini': 'logo-removebg-preview.png',
    'motovario': '_D1_84-removebg-preview.png',
    'sew': 'SEW_LOGO.svg.png',
    'tambovpolimermash': 'reduce_image-removebg-preview.png',
    'bondioli': 'logo.png',
    'chzr': 'imgonline-com-ua-Resize-wCJ8bxXOKkyvcy-removebg-preview.png',
    'mze': 'imgonline_com_ua_resize_genaouuclxqlf-removebg-preview_1.png',
    'pzmp': 'logo-1056-removebg-preview.png',
}

PARTNERS = {
    '1btsk': '1BTSK.jpg',
    'maz': 'Minsky_automoblie_plant.png',
    'gomselmash': 'table_gomselmash.jpg',
    'agropromselmash': 'agropromselmash.jpg',
}

PRODUCTS = {
    'nmrv-chervyachny': '19051808552_nmrv_1.jpg',
    'planetarnyj-bep-0151': 'bezymyannyj66678_cinQmj8.png',
    'rt500': 'zz_NIndgf0.png',
    's1000': 'Bandioli-S1000_ddfUseD.jpg',
    'k-seriya': 'ud-k-removebg-preview_jMv0wVw.png',
    'f-seriya': 'F_MMRZpGe.png',
    'r-seriya': 'Reduktor-seriya-R.jpg',
    'industrialnyj-v': '_D0_B1.png',
    'bep-1271': '_D1_8F_D1_8F_D1_8F.png',
    'rc': 'rs.png',
    'korobka-bep00153': 'qwqwqw.png',
    'korobka-bep451f': '1212121_eAOykUR.png',
}


def trim(im, clean=True):
    """Trim borders and (optionally) knock out flat light studio backgrounds."""
    import numpy as np
    from collections import deque

    im = im.convert('RGBA')
    arr = np.array(im)
    h, w = arr.shape[:2]
    rgb = arr[:, :, :3].astype(int)
    alpha = arr[:, :, 3]
    bright = rgb.mean(axis=2)
    sat = rgb.max(axis=2) - rgb.min(axis=2)
    is_light = (bright > 196) & (sat < 34)

    if not clean:
        # logos: keep white areas, just crop
        if alpha.min() == 255:
            bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
            diff = ImageChops.difference(im, bg).convert('L')
            bbox = diff.point(lambda v: 255 if v > 10 else 0).getbbox()
        else:
            bbox = im.getchannel('A').getbbox()
        return im.crop(bbox) if bbox else im

    # seeds: transparent pixels, plus light pixels touching the outer border
    mask = alpha == 0
    border_pts = []
    for x in range(w):
        border_pts.append((0, x)); border_pts.append((h - 1, x))
    for y in range(h):
        border_pts.append((y, 0)); border_pts.append((y, w - 1))
    for (y, x) in border_pts:
        if is_light[y, x] or alpha[y, x] == 0:
            mask[y, x] = True
    q = deque(map(tuple, np.argwhere(mask)))

    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not mask[ny, nx] and is_light[ny, nx]:
                mask[ny, nx] = True
                q.append((ny, nx))

    if mask.any():
        arr[:, :, 3] = np.where(mask, 0, arr[:, :, 3])
        im = Image.fromarray(arr)

    bbox = im.getchannel('A').getbbox()
    if bbox:
        im = im.crop(bbox)
    return im


def save(im, path, max_side, white_bg=False, clean=True):
    im = trim(im, clean=clean)
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    # pad to square with transparent margin
    side = max(im.size)
    canvas = Image.new('RGBA', (int(side * 1.06), int(side * 1.06)), (0, 0, 0, 0))
    canvas.alpha_composite(im, ((canvas.width - im.width) // 2, (canvas.height - im.height) // 2))
    if white_bg:
        flat = Image.new('RGB', canvas.size, 'white')
        flat.paste(canvas, (0, 0), canvas)
        flat.save(path, quality=88, optimize=True)
    else:
        canvas.save(path, optimize=True)


def main():
    os.makedirs(os.path.join(OUT, 'cat'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'prod'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'brands'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'partners'), exist_ok=True)

    for slug, f in CATS.items():
        p = os.path.join(SRC, re.sub(r'[^A-Za-z0-9._-]', '_', f))
        im = Image.open(p)
        save(im, os.path.join(OUT, 'cat', slug + '.png'), 420)

    for slug, f in PRODUCTS.items():
        p = os.path.join(SRC, re.sub(r'[^A-Za-z0-9._-]', '_', f))
        im = Image.open(p)
        save(im, os.path.join(OUT, 'prod', slug + '.png'), 760)

    for slug, f in BRANDS.items():
        p = os.path.join(SRC, re.sub(r'[^A-Za-z0-9._-]', '_', f))
        im = Image.open(p)
        save(im, os.path.join(OUT, 'brands', slug + '.png'), 300, clean=False)

    for slug, f in PARTNERS.items():
        p = os.path.join(SRC, re.sub(r'[^A-Za-z0-9._-]', '_', f))
        im = Image.open(p)
        save(im, os.path.join(OUT, 'partners', slug + '.png'), 300, clean=False)

    # brand mark: orange, transparent cuts
    logo = Image.open(os.path.expanduser('~/.hermes/cache/scratch/sh_assets/img/logo.png')).convert('RGBA')
    logo = logo.crop(logo.getbbox())
    px = logo.load()
    for y in range(logo.height):
        for x in range(logo.width):
            r, g, b, a = px[x, y]
            if r > 235 and g > 235 and b > 235:
                px[x, y] = (255, 255, 255, 0)
    logo.thumbnail((256, 256), Image.LANCZOS)
    logo.save(os.path.join(OUT, 'logo-mark-orange.png'), optimize=True)

    white = logo.copy()
    px = white.load()
    for y in range(white.height):
        for x in range(white.width):
            r, g, b, a = px[x, y]
            if a > 40:
                px[x, y] = (255, 255, 255, a)
    white.save(os.path.join(OUT, 'logo-mark-white.png'), optimize=True)

    total = 0
    for root, _, files in os.walk(OUT):
        for f in files:
            total += os.path.getsize(os.path.join(root, f))
    print('images ready, total MB', round(total / 1e6, 2))


if __name__ == '__main__':
    main()
