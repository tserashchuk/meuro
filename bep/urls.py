"""bep URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from privod import views

urlpatterns = [
                  path('', views.Home.as_view(), name='home'),
                  path('category/', views.Categorys.as_view(), name='categorys'),
                  path('category/<str:cat_slug>', views.Products.as_view(), name='products'),
                  path('product/<str:product_slug>', views.SingleProduct.as_view(), name='product'),
                  path('product-tag/<str:tag_slug>', views.ProductTags.as_view(), name='producttag'),
                  path('manufacturer/<str:manufacturer_slug>', views.Manufacturers.as_view(), name='manufacturer'),
                  path('contact/', views.Contacts.as_view(), name='contact'),
                  path('admin/', admin.site.urls),
                  path('editorjs/', include('django_editorjs_fields.urls')),
                  path('search', views.Search.as_view(), name='search'),
                  path("sendmail/", views.sendmail, name='sendmail'),
                  

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
