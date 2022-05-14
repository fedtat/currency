from currency.models import ContactUs, Rate, Source

import django_filters


class RateFilter(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = {
            'buy': ('gte', 'lte'),
            'sale': ('gte', 'lte'),
            'created': ('gte', 'lte'),
            'type': ('exact', ),
        }


class SourceFilter(django_filters.FilterSet):
    class Meta:
        model = Source
        fields = {
            'id': ('exact', ),
            'name': ('exact',),
        }


class ContactUsFilter(django_filters.FilterSet):
    class Meta:
        model = ContactUs
        fields = {
            'created': ('gte', 'lte'),
            'name': ('exact',),
            'email_from': ('exact',),
        }
