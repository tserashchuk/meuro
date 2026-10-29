from django.contrib import admin
from privod.models import *



class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'article_name')


admin.site.register(Category, admin.ModelAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Region, admin.ModelAdmin)
admin.site.register(Punkt, admin.ModelAdmin)
admin.site.register(Product, admin.ModelAdmin)
admin.site.register(Manufacturer, admin.ModelAdmin)
admin.site.register(Producttag, admin.ModelAdmin)





