from django.db import models


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=254)
    subject = models.CharField(max_length=64)
    message = models.CharField(max_length=1000)


class Rate(models.Model):
    type = models.CharField(max_length=5)  # noqa: A003
    source = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    buy = models.DecimalField(max_digits=10, decimal_places=2)
    sell = models.DecimalField(max_digits=10, decimal_places=2)


class Source(models.Model):
    name = models.CharField(max_length=64)
    source_url = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
