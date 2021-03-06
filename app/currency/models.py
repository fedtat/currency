from currency import model_choices as mch

from django.db import models


class ContactUs(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128)
    email_from = models.EmailField()
    subject = models.CharField(max_length=64)
    message = models.CharField(max_length=1000)
    raw_content = models.TextField()


class Source(models.Model):
    name = models.CharField(max_length=64, unique=True)
    code_name = models.PositiveSmallIntegerField(choices=mch.SourceCodeName.choices, unique=True)
    source_url = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    icon = models.FileField(default=None, null=True, blank=True)

    def __str__(self):
        return self.name


class Rate(models.Model):
    type = models.CharField(max_length=5, choices=mch.RateType.choices)  # noqa: A003
    base_type = models.CharField(max_length=5, choices=mch.RateType.choices, default=mch.RateType.UAH)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='rates')
    created = models.DateTimeField(auto_now_add=True)
    buy = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.DecimalField(max_digits=10, decimal_places=2)
