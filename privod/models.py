import datetime
from django.urls import reverse
from django.db import models
from django_editorjs_fields import EditorJsJSONField

class Category(models.Model):
    cat_name = models.CharField('Название категории продукта', max_length=200)
    cat_title = models.CharField('Заголовок для Open Graph (og:title)', max_length=200, blank=True)
    cat_metadesc = models.CharField('Описание для Open Graph (og:description)', max_length=300, blank=True)
    cat_slug = models.CharField('URL', max_length=200, default='slug' + str(datetime.datetime.now()))
    cat_short_desc = models.TextField('Короткое описание', blank=True)
    pin_main_first = models.BooleanField('Закрепить на главной странице в первом блоке', default=False)
    pin_main_sec = models.BooleanField('Закрепить на главной странице во втором блоке', default=False)
    cat_desccript = EditorJsJSONField(default=dict)
    cat_image = models.ImageField('Изображение категории', default='placeholder.jpg')
    preview_image = models.ImageField('Изображение категории', default='placeholder.jpg')
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    cat_question_1 = models.TextField('Вопрос 1', blank=True, default='')
    cat_question_2 = models.TextField('Вопорос 2', blank=True, default='')
    cat_answer_1 = models.TextField('Ответ 1', blank=True, default='')
    cat_answer_2 = models.TextField('Ответ 2', blank=True, default='')

    def __str__(self):
        return self.cat_name

    def get_absolute_url(self):
        return reverse('products', args=[self.cat_slug])

class Manufacturer(models.Model):
    manufacturer_name = models.CharField('Название производителя', max_length=200)
    manufacturer_title = models.CharField('Заголовок для Open Graph (og:title)', max_length=200)
    manufacturer_metadesc = models.CharField('Описание для Open Graph (og:description)', max_length=300)
    manufacturer_image = models.ImageField('Логотип производителя', default='placeholder.jpg')
    manufacturer_big_image = models.ImageField('Фон производителя', default='placeholder.jpg')
    manufacturer_desc = models.TextField('Описание производителя', blank=True)
    body_editorjs = EditorJsJSONField()
    manufacturer_slug = models.CharField('URL', max_length=200, default='manufacturer' + str(datetime.datetime.now()))

    def __str__(self):
        return self.manufacturer_name

    def get_absolute_url(self):
        return reverse('manufacturer', args=[self.manufacturer_slug])

class Producttag(models.Model):
    tag_name = models.CharField('Название тега', max_length=200)
    tag_title = models.CharField('Заголовок для Open Graph (og:title)', max_length=200)
    tag_metadesc = models.CharField('Описание для Open Graph (og:description)', max_length=300)
    tag_short_desc = models.TextField('Короткое описание', blank=True)
    tag_slug = models.CharField('URL', max_length=200, default='tag' + str(datetime.datetime.now()))

    def __str__(self):
        return self.tag_name

class Product(models.Model):
    product_name = models.CharField('Название продукта', max_length=200)
    product_title = models.CharField('Заголовок для Open Graph (og:title)', max_length=200)
    product_metadesc = models.CharField('Описание для Open Graph (og:description)', max_length=300)
    product_short_desc = models.TextField('Короткое описание', blank=True)
    product_desc = models.TextField('Артикул', blank=True)
    product_image = models.ImageField('Изображение продукта', default='placeholder.jpg')
    pin_main = models.BooleanField('Закрепить на главной странице', default=False)
    category = models.ManyToManyField(Category,blank=True)
    manufacturer = models.ManyToManyField(Manufacturer, blank=True)
    product_tag = models.ManyToManyField(Producttag,blank=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    characteristics = EditorJsJSONField(default=dict)
    longdescription = EditorJsJSONField(default=dict)
    documentationfield = EditorJsJSONField(default=dict)
    product_slug = models.CharField('URL', max_length=200, default='product' + str(datetime.datetime.now()))

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('product', args=[self.product_slug])

class Article(models.Model):
    article_name = models.CharField('Заголовок H1', max_length=200)
    article_title = models.CharField('Заголовок для Open Graph (og:title)', max_length=200)
    article_metadesc = models.CharField('Описание для Open Graph (og:description)', max_length=300)
    article_slug = models.CharField('URL', max_length=200, default='article' + str(datetime.datetime.now()))
    article_short_desc = models.TextField('Короткое описание для Schema', blank=True)
    article_image = models.ImageField('Изображение статьи')
    isStock = models.BooleanField(default=False)
    body_editorjs = EditorJsJSONField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.article_name

    def get_absolute_url(self):
        return reverse('article', args=[self.article_slug])



class Region(models.Model):
    region_name = models.CharField('Название региона', max_length=200)
    region_title = models.CharField('Заголовок для Open Graph (og:title)', max_length=200)
    region_metadesc = models.CharField('Описание для Open Graph (og:description)', max_length=300)
    region_slug = models.CharField('URL', max_length=200, default='region' + str(datetime.datetime.now()))
    region_short_desc = models.TextField('Короткое описание', blank=True)
    body_editorjs = EditorJsJSONField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.region_name

    def get_absolute_url(self):
        return reverse('region', args=[self.region_slug])


class Punkt(models.Model):
    punkt_name = models.CharField('Название офиса', max_length=200)
    punkt_title = models.CharField('Заголовок для Open Graph (og:title)', max_length=200)
    punkt_metadesc = models.CharField('Описание для Open Graph (og:description)', max_length=300)
    punkt_short_desc = models.TextField('Короткое описание', blank=True)
    punkt_geo = models.CharField('Описание description', max_length=300, default="55.659173,37.762848")
    punkt_image = models.ImageField('Изображение пункта')
    body_editorjs = EditorJsJSONField()
    punkt_map_key = models.CharField('Ключ карты Яндекс', max_length=200, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    
    def __str__(self):
        return self.punkt_name

