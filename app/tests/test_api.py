from currency.models import ContactUs, Rate, Source

from django.conf import settings
from django.urls import reverse

from rest_framework.test import APIClient


def test_contactus_get_contact():
    client = APIClient()
    response = client.get(reverse('v1:contactus-list'))
    assert response.status_code == 200
    assert response.json()


def test_contactus_post_empty_data():
    client = APIClient()
    response = client.post(reverse('v1:contactus-list'), data={})
    assert response.status_code == 400
    assert response.json() == {
        'name': ['This field is required.'],
        'email_from': ['This field is required.'],
        'subject': ['This field is required.'],
        'message': ['This field is required.']
    }


def test_contactus_post_valid_data(mailoutbox):
    initial_count = ContactUs.objects.count()
    client = APIClient()
    payload = {
        'name': 'Example Name',
        'email_from': 'emailcontactus@example.com',
        'subject': 'Subject Example',
        'message': 'Example Text\n' * 10
    }
    response = client.post(reverse('v1:contactus-list'), data=payload)
    assert response.status_code == 201
    assert response.json()

    assert len(mailoutbox) == 1
    assert ContactUs.objects.count() == initial_count + 1
    assert mailoutbox[0].to == [settings.DEFAULT_FROM_EMAIL]
    assert mailoutbox[0].subject == 'Contact us: Subject Example'


def test_contactus_patch():
    client = APIClient()
    contact = ContactUs.objects.create(name=23, email_from=settings.DEFAULT_FROM_EMAIL, subject='Subject Example',
                                       message='Example Text\n' * 10)
    payload = {
        'name': 'New Name',
    }
    response = client.patch(reverse('v1:contactus-detail', args=[contact.id]), data=payload)
    assert response.status_code == 200
    assert response.json()


def test_contactus_delete():
    client = APIClient()
    contact = ContactUs.objects.create(name=23, email_from=settings.DEFAULT_FROM_EMAIL, subject='Subject Example',
                                       message='Example Text\n' * 10)
    response = client.delete(reverse('v1:contactus-detail', args=[contact.id]))
    assert response.status_code == 204
    assert response.content == b''


def test_rates_get_list():
    client = APIClient()
    response = client.get(reverse('v1:rate-list'))
    assert response.status_code == 200
    assert response.json()


def test_rates_post_empty_data():
    client = APIClient()
    response = client.post(reverse('v1:rate-list'), data={})
    assert response.status_code == 400
    assert response.json() == {
        'sale': ['This field is required.'],
        'buy': ['This field is required.'],
        'source': ['This field is required.'],
    }


def test_rates_post_valid_data():
    client = APIClient()
    source = Source.objects.last()
    payload = {
        'sale': 23,
        'buy': 24,
        'source': source.id,
    }
    response = client.post(reverse('v1:rate-list'), data=payload)
    assert response.status_code == 201
    assert response.json()


def test_rates_patch_valid_data():
    client = APIClient()
    rate = Rate.objects.last()

    payload = {
        'sale': 9999,
    }
    response = client.patch(reverse('v1:rate-detail', args=[rate.id]), data=payload)
    assert response.status_code == 200
    assert response.json()['sale'] == '9999.00'


def test_rates_delete():
    client = APIClient()
    rate = Rate.objects.last()

    response = client.delete(reverse('v1:rate-detail', args=[rate.id]))
    assert response.status_code == 204
    assert response.content == b''
