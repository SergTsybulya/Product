from enum import Enum

from django.utils.translation import pgettext_lazy
from measurement.measures import Volume


class VolumeUnits:
    LITER = 'l'
    MILLILITER = 'ml'

    CHOICES = [
        (LITER, pgettext_lazy('Liter volume unit symbol', 'l')),
        (MILLILITER, pgettext_lazy('Milliliter volume unit symbol', 'ml'))]


VolumeUnitsEnum = Enum('VolumeUnitsEnum',
                       {unit: unit for unit in VolumeUnits.CHOICES})


def zero_volume():
    """Function used as a model's default."""
    return Volume(kg=0)


def convert_volume(volume, unit):
    converted_volume = getattr(volume, unit)
    return Volume(**{unit: converted_volume})


class DefaultVolumeUnit(object):
    serializer_field = None

    def call(self):
        return VolumeUnits.LITER

    def set_context(self, serializer_field):
        self.serializer_field = serializer_field