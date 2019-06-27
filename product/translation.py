from modeltranslation.translator import translator, TranslationOptions

from product.models import CategoryProducts, Product


class ProductModelTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description'
    )


translator.register(Product, ProductModelTranslationOptions)


class CategoryProductsModelTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


translator.register(CategoryProducts, CategoryProductsModelTranslationOptions)
