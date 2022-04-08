from django.db import models


class SourceName(models.TextChoices):
    PB = 'PB', 'PrivatBank'
    MB = 'MB', 'MonoBank'
    OB = 'OB', 'OschadBank'


# SOURCE_NAME_PB = 'PB'
# SOURCE_NAME_MB = 'MB'
# SOURCE_NAME_OB = 'OB'
#
# SOURCE_NAMES = (
#     (SOURCE_NAME_PB, 'PrivatBank'),
#     (SOURCE_NAME_MB, 'MonoBank'),
#     (SOURCE_NAME_OB, 'OschadBank'),
# )
