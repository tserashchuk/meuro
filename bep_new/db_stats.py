import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bep.settings')
django.setup()

from privod.models import Category, Manufacturer, Producttag, Product, Article, Region, Punkt

stats = {
    'categories_count': Category.objects.count(),
    'manufacturers_count': Manufacturer.objects.count(),
    'tags_count': Producttag.objects.count(),
    'products_count': Product.objects.count(),
    'articles_count': Article.objects.count(),
    'regions_count': Region.objects.count(),
    'punkts_count': Punkt.objects.count(),
}

# Products per category
products_per_category = []
for cat in Category.objects.all():
    products_per_category.append({
        'name': cat.cat_name,
        'count': cat.product_set.count()
    })
stats['products_per_category'] = sorted(products_per_category, key=lambda x: x['count'], reverse=True)

# Products per manufacturer
products_per_manufacturer = []
for man in Manufacturer.objects.all():
    products_per_manufacturer.append({
        'name': man.manufacturer_name,
        'count': man.product_set.count()
    })
stats['products_per_manufacturer'] = sorted(products_per_manufacturer, key=lambda x: x['count'], reverse=True)

print(json.dumps(stats, ensure_ascii=False, indent=2))
