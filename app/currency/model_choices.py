from django.db import models


# class SourceName(models.TextChoices):
#     PB = 'PB', 'PrivatBank'
#     MB = 'MB', 'MonoBank'
#     OB = 'OB', 'OschadBank'


class RateType(models.TextChoices):
    UAH = 'UAH', 'Hryvna'
    USD = 'USD', 'Dollar'
    EUR = 'EUR', 'Euro'
    BTC = 'BTC', 'Bitcoin'


class SourceCodeName(models.IntegerChoices):
    PRIVATBANK = 1, 'PrivatBank'
    MONOBANK = 2, 'MonoBank'
    VKURSE = 3, 'Vkurse'
    GETGEOAPI = 4, 'GetGeoApi'
    FIXER = 5, 'Fixer'
    FREECURRCONV = 6, 'FreeCurrencyConverter'


# SOURCE_NAME_PB = 'PB'
# SOURCE_NAME_MB = 'MB'
# SOURCE_NAME_OB = 'OB'
#
# SOURCE_NAMES = (
#     (SOURCE_NAME_PB, 'PrivatBank'),
#     (SOURCE_NAME_MB, 'MonoBank'),
#     (SOURCE_NAME_OB, 'OschadBank'),
# )
