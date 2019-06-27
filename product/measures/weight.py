"""We are using 'weight' instead of a 'mass'.

For those of us who are earth-bound, weight is what we usually experience.
Mass is a theoretical construct.
Unless we are dealing with inertia and momentum, we are encountering
the attractive force between ourselves and the earth,
the isolated effects of mass alone being a little more esoteric.

So even though mass is more fundamental, most people think
in terms of weight.

In the end, it does not really matter unless you travel between
different planets.
"""
from enum import Enum

from django.utils.translation import pgettext_lazy
from measurement.measures import Weight


class WeightUnits:
    KILOGRAM = 'kg'
    GRAM = 'g'

    CHOICES = [
        (KILOGRAM, pgettext_lazy('Kilogram weight unit symbol', 'kg')),
        (GRAM, pgettext_lazy('Gram weight unit symbol', 'g'))]


WeightUnitsEnum = Enum('WeightUnitsEnum',
                       {unit: unit for unit in WeightUnits.CHOICES})


def zero_weight():
    """Function used as a model's default."""
    return Weight(kg=0)


def convert_weight(weight, unit):
    # Weight amount from the Weight instance can be retrieved in several units
    # via its properties. eg. Weight(lb=10).kg
    converted_weight = getattr(weight, unit)
    return Weight(**{unit: converted_weight})


class DefaultWeightUnit(object):
    serializer_field = None

    def call(self):
        return WeightUnits.KILOGRAM

    def set_context(self, serializer_field):
        self.serializer_field = serializer_field