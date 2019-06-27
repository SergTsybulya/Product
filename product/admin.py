from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from product.models import Product, CategoryProducts, Ingredient, Stock, Filling


class ProductAdmin(TranslationAdmin):
    pass


admin.site.register(Product, ProductAdmin)


class CategoryProductsAdmin(TranslationAdmin):
    pass


admin.site.register(CategoryProducts, CategoryProductsAdmin)

admin.site.register(Ingredient)
admin.site.register(Stock)
admin.site.register(Filling)