import os

from django.db import models
from django.db.models import SmallIntegerField
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django_measurement.models import MeasurementField
from measurement.measures import Weight, Volume
from stdimage import StdImageField

from product.measures import VolumeUnits
from product.measures.weight import WeightUnits


class ProductManager(models.Manager):

    def active_product(self):
        return self.filter(is_published=True)


def check_and_delete(path_f):
    if os.path.isfile(path_f):
        os.remove(path_f)


def make_upload_path(instance, filename):
    path_f = f'static/products/{instance.category.name}/{instance.name}.jpg'
    check_and_delete(path_f)
    return path_f


def make_upload_path_filling(instance, filename):
    path_f = f'static/products/{instance.filling}/{instance.filling.name}.jpg'
    check_and_delete(path_f)
    return path_f


class Product(models.Model):
    name = models.CharField(max_length=55, verbose_name=_('Название'))
    category = models.ForeignKey('CategoryProducts', blank=True,
                                 null=True, verbose_name=_('Категория'))
    weight = models.CharField(max_length=55, verbose_name=_('Вес'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Описание'))
    price = models.CharField(max_length=10, verbose_name=_('Цена'))
    is_published = models.BooleanField(default=False,
                                       verbose_name=_("Опубликовать"))
    date_published = models.DateTimeField(auto_now=True, null=True, blank=True,
                                          verbose_name=_('Дата публикации'))
    ingradient = models.ManyToManyField('Ingredient', blank=True)
    photo = StdImageField(upload_to=make_upload_path, null=True,
                          max_length=255, verbose_name=_('Фото'),
                          variations={'small': (250, 250),
                                      'medium': (350, 350),
                                      'large': (500, 500)})
    filling = models.ForeignKey('Filling', on_delete=models.SET_NULL, null=True,
                                blank=True, verbose_name=_('Начинка'))

    objects = ProductManager()

    def __str__(self):
        return f'{self.name} - {self.price} грн.'

    def delete(self, *args, **kwargs):
        check_and_delete(self.photo.path)
        super(Product, self).delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = _('Продукты')
        verbose_name = _('Продукт')


class Filling(models.Model):
    name = models.CharField(max_length=55, verbose_name=_('Название начинки'))
    description = models.CharField(max_length=250,
                                   verbose_name=_('Описание начинки'))
    ingradient = models.ManyToManyField('Ingredient', blank=True)
    photo = StdImageField(upload_to=make_upload_path_filling, null=True,
                          max_length=255, verbose_name=_('Фото начинки'),
                          variations={'small': (250, 250),
                                      'medium': (350, 350),
                                      'large': (500, 500)})

    class Meta:
        verbose_name_plural = _('Начинки')
        verbose_name = _('Начинка')


class CategoryProducts(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name=_('Категория сладостей'))
    slug = models.CharField(max_length=50, blank=True, null=True, verbose_name="Slug")

    class Meta:
        verbose_name_plural = _('Категории')
        verbose_name = _('Категория')

    def __str__(self):
        return self.name

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)


class Ingredient(models.Model):
    name = models.CharField(max_length=55,
                            verbose_name=_('Название ингредиента'))

    class Meta:
        verbose_name_plural = _('Ингредиенты')
        verbose_name = _('Ингредиент')

    def __str__(self):
        return self.name


class Stock(models.Model):
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE,
                                   blank=True, null=True,
                                   verbose_name=_('Название ингредиента'))
    weight = MeasurementField(blank=True, null=True,
                              measurement=Weight,
                              unit_choices=WeightUnits.CHOICES,
                              verbose_name=_('Вес'))
    volume = MeasurementField(blank=True, null=True,
                              measurement=Volume,
                              unit_choices=VolumeUnits.CHOICES,
                              verbose_name=_('Обьем'))
    quantity = SmallIntegerField(blank=True, null=True,
                                 verbose_name=_('Количество'))

    class Meta:
        verbose_name_plural = _('Склад')
        verbose_name = _('Ингредиент')

    def __str__(self):
        value = 0
        unit = ''
        if self.volume and self.volume.value:
            value, unit = self.volume.value, self.volume.unit
        if self.weight and self.weight.value:
            value, unit = self.weight.value, self.weight.unit
        if self.quantity:
            value, unit = self.quantity, 'шт'
        return f'{self.ingredient.name} - {value} {unit}'

    def save(self, *args, **kwargs):
        qs = Stock.objects.filter(ingredient=self.ingredient)
        if not qs:
            super().save(*args, **kwargs)
        ##TODO изменить сообщение о сохранении объекта
