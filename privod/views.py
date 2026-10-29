import json

from django.conf import settings
from django.contrib.staticfiles.finders import find as find_static
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.views import View

from privod.models import Category, Manufacturer, Product, Producttag, Region

INDUSTRY_PHOTOS = (
    'assets/img/hero/slide-1.jpg',
    'assets/img/hero/slide-2.jpg',
    'assets/img/photo/testimonial-factory.jpg',
    'assets/img/hero/slide-3.jpg',
    'assets/img/hero/testimonial.jpg',
)


class Home(View):
    def get(self, request):
        featured = list(
            Product.objects.filter(pin_main=True).prefetch_related('category', 'manufacturer')
        )
        if not featured:
            featured = list(
                Product.objects.prefetch_related('category', 'manufacturer')[:12]
            )
        home_categories = list(
            Category.objects.annotate(n=Count('product', distinct=True))
            .prefetch_related('product_set')
            .order_by('-n')
        )
        for category in home_categories:
            category.hero_src = category_hero_image(category)
        home_industries = list(
            Producttag.objects.annotate(n=Count('product', distinct=True)).order_by('-n')[:5]
        )
        for tag, photo in zip(home_industries, INDUSTRY_PHOTOS):
            tag.photo = photo
        return render(request, 'index.html', {
            'featured': featured,
            'home_categories': home_categories,
            'home_industries': home_industries,
        })


class Categorys(View):
    def get(self, request):
        products = (
            Product.objects.prefetch_related('category', 'manufacturer', 'product_tag')
            .order_by('product_name')
        )
        return render(request, 'categorys.html', {'products': products})


# Слаги в базе не совпадают с файлами рендеров в static/assets/img/cat/.
_HERO_FILE = {
    'сhervyachnie_reduktori': 'chervyachnie_reduktori',
    'slug2024-07-31 09:17:57.417897': 'drugoe',
    'slug2024-08-16 10:34:16.849814': 'konichesko-cilindricheskie-gidromotor',
}


def category_hero_image(category):
    """Прозрачный рендер из макета, иначе фото категории из базы."""
    slug = _HERO_FILE.get(category.cat_slug, category.cat_slug)
    rel = f'assets/img/cat/{slug}.png'
    if find_static(rel):
        return static(rel)
    for field in (category.cat_image, category.preview_image):
        name = getattr(field, 'name', '') or ''
        if not name or name == 'placeholder.jpg':
            continue
        try:
            if field.storage.exists(name):
                return field.url
        except Exception:
            continue
    return ''


class Products(View):
    def get(self, request, cat_slug):
        category = get_object_or_404(Category, cat_slug=cat_slug)
        products = (
            category.product_set.prefetch_related('manufacturer', 'category', 'product_tag')
            .order_by('product_name')
        )
        makers = (
            Manufacturer.objects.filter(product__category=category)
            .annotate(n=Count('product', filter=Q(product__category=category), distinct=True))
            .distinct()
            .order_by('manufacturer_name')
        )
        category_tags = Producttag.objects.filter(product__category=category).distinct().order_by('tag_name')
        others = (
            Category.objects.exclude(pk=category.pk)
            .annotate(n=Count('product', distinct=True))
            .order_by('-n')[:4]
        )
        return render(request, 'products.html', {
            'category': category,
            'products': products,
            'makers': makers,
            'category_tags': category_tags,
            'other_categories': others,
            'hero_image': category_hero_image(category),
        })


class ProductTags(View):
    def get(self, request, tag_slug):
        producttag = get_object_or_404(Producttag, tag_slug=tag_slug)
        products = (
            Product.objects.filter(product_tag=producttag)
            .prefetch_related('category', 'manufacturer', 'product_tag')
            .order_by('product_name')
        )
        return render(request, 'tags.html', {
            'producttags': producttag,
            'products': products,
        })


class SingleProduct(View):
    def get(self, request, product_slug):
        product = get_object_or_404(
            Product.objects.prefetch_related('category', 'manufacturer', 'product_tag'),
            product_slug=product_slug,
        )
        category = product.category.first()
        related = []
        if category:
            related = list(
                Product.objects.filter(category=category)
                .exclude(pk=product.pk)
                .prefetch_related('category', 'manufacturer')[:4]
            )
        return render(request, 'product.html', {
            'product': product,
            'category': category,
            'related': related,
        })


class Contacts(View):
    def get(self, request):
        regions = Region.objects.prefetch_related('punkt_set')
        return render(request, 'contact.html', {'regions': regions})


class Manufacturers(View):
    def get(self, request, manufacturer_slug):
        manufacturer = get_object_or_404(Manufacturer, manufacturer_slug=manufacturer_slug)
        products = (
            Product.objects.filter(manufacturer=manufacturer)
            .prefetch_related('category', 'manufacturer', 'product_tag')
            .order_by('product_name')
        )
        return render(request, 'manufacturer.html', {
            'manufacturer': manufacturer,
            'products': products,
        })


class Search(View):
    def post(self, request):
        try:
            payload = json.loads(request.body or '{}')
        except json.JSONDecodeError:
            payload = {}
        query = str(payload.get('searchquery') or request.POST.get('q') or '').strip()
        return self._results(query)

    def get(self, request):
        return self._results(request.GET.get('q', '').strip())

    def _results(self, query):
        found = []
        if query:
            products = (
                Product.objects.filter(product_name__icontains=query)
                .prefetch_related('category')[:24]
            )
            for product in products:
                found.append([product.product_name, product.product_slug])
        return HttpResponse(json.dumps(found), content_type='application/json')


def sendmail(request):
    if request.method != 'POST':
        return redirect('/')
    name = (request.POST.get('name') or '').strip()
    phone = (request.POST.get('phone') or '').strip()
    comment = (request.POST.get('comment') or request.POST.get('message') or '').strip()
    ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    body = '\n'.join(part for part in (name, phone, comment) if part)
    try:
        send_mail(
            'Заказ звонка с сайта',
            body,
            'info@beleuroprivod.by',
            ['tserashchuk.kirill@gmail.com'],
            fail_silently=False,
        )
    except Exception:
        if settings.DEBUG and ajax:
            return JsonResponse({'ok': True, 'stored': False})
        if ajax:
            return JsonResponse(
                {'ok': False, 'error': 'Не удалось отправить заявку. Позвоните нам.'},
                status=502,
            )
        raise
    if ajax:
        return JsonResponse({'ok': True})
    return redirect('/')
