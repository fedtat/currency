from api.v2.filters import RateFilter
from api.v2.pagination import RatesPagination
from api.v2.serializers import ContactUsSerializer, RateSerializer, SourceSerializer
from api.v2.throttles import AnonCurrencyThrottle

from currency.models import ContactUs, Rate, Source

from django.conf import settings
from django.core.mail import send_mail

from django_filters import rest_framework as filters

from rest_framework import filters as rest_framework_filters, generics, viewsets
from rest_framework.renderers import JSONRenderer

from rest_framework_csv.renderers import CSVRenderer

from rest_framework_xml.renderers import XMLRenderer


class SourceView(generics.ListAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        subject = request.data.get('subject')
        email = request.data.get('email_from')
        message = request.data.get('message')
        subject = f"Contact us: {subject}"
        body = f'''
                From: {email}
                Message: {message}
                '''
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False
        )
        return response


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    renderer_classes = (JSONRenderer, XMLRenderer, CSVRenderer)
    pagination_class = RatesPagination
    filterset_class = RateFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    ordering_fields = ('id', 'sale', 'buy')
    throttle_classes = [AnonCurrencyThrottle]
