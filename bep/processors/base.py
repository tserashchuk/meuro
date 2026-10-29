from django.db.models import Count
from django.urls import reverse

from privod.models import Category, Manufacturer, Product, Producttag, Punkt

PHONE = '+375 (29) 6-910-510'
PHONE_HREF = 'tel:+375296910510'
PHONE_ALT = ['+375 (29) 6-815-205', '+375 (17) 374-74-54']
EMAIL = 'europrivod@mail.ru'
ADDRESS = '220137, г. Минск, Партизанский проспект 178, офис 311'
UNP = 'УНП 191148828'
BRAND = 'БелЕвропривод'


def _column(category):
    name = category.cat_name.lower()
    if 'гидромотор' in name or 'коническо' in name:
        return 1
    if any(hint in name for hint in (
        'червяч', 'коническ', 'планетар', 'соосн', 'параллель', 'плоск', 'индустриал',
    )):
        return 0
    if any(hint in name for hint in ('вариатор', 'электродвиг', 'цеп')):
        return 1
    return 2


def _is_hot(category):
    name = category.cat_name.lower()
    if 'коническо' in name:
        return False
    return any(hint in name for hint in ('червяч', 'коническ', 'планетар'))


def category_processor(request):
    categories = list(
        Category.objects.annotate(n=Count('product', distinct=True)).order_by('-n', 'cat_name')
    )
    for category in categories:
        category.is_hot = _is_hot(category)

    columns = {'Редукторы': [], 'Приводы и узлы': [], 'Ещё': []}
    order = ('Редукторы', 'Приводы и узлы', 'Ещё')
    for category in categories:
        columns[order[_column(category)]].append(category)
    menu_columns = [{'title': title, 'items': columns[title]} for title in order]

    manufacturers = list(
        Manufacturer.objects.annotate(n=Count('product', distinct=True)).order_by('-n', 'manufacturer_name')
    )
    tags = list(
        Producttag.objects.annotate(n=Count('product', distinct=True)).order_by('-n', 'tag_name')
    )
    punkts = list(Punkt.objects.select_related('region'))
    tag_titles = ('Отрасли', 'Ещё отрасли', 'Подборки')
    tag_size = max(1, (len(tags) + len(tag_titles) - 1) // len(tag_titles)) if tags else 1
    tag_columns = []
    for index, title in enumerate(tag_titles):
        chunk = tags[index * tag_size:(index + 1) * tag_size]
        if chunk:
            tag_columns.append({'title': title, 'items': chunk})

    search_index = []
    for product in Product.objects.prefetch_related('category').order_by('product_name'):
        category = next(iter(product.category.all()), None)
        image = ''
        if product.product_image:
            try:
                image = product.product_image.url
            except ValueError:
                image = ''
        search_index.append({
            'n': product.product_name,
            'c': category.cat_name if category else 'Каталог',
            'u': reverse('product', args=[product.product_slug]),
            'i': image,
        })

    return {
        'catprocessor_base': categories,
        'menu_columns': menu_columns,
        'manufacturers_base': manufacturers,
        'producttags_base': tags,
        'tag_columns': tag_columns,
        'punkts_base': punkts,
        'product_total': Product.objects.count(),
        'own_count': Product.objects.filter(manufacturer=None).count(),
        'search_index': search_index,
        'site_phone': PHONE,
        'site_phone_href': PHONE_HREF,
        'site_phone_alt': PHONE_ALT,
        'site_email': EMAIL,
        'site_address': ADDRESS,
        'site_unp': UNP,
        'site_brand': BRAND,
    }
