from currency.models import ContactUs, Rate, Source

from django.conf import settings
from django.urls import reverse


def test_contactus_get_contact(api_client):
    response = api_client.get(reverse('v1:contactus-list'))
    assert response.status_code == 200
    assert response.json()


def test_contactus_post_empty_data(api_client):
    response = api_client.post(reverse('v1:contactus-list'), data={})
    assert response.status_code == 400
    assert response.json() == {
        'name': ['This field is required.'],
        'email_from': ['This field is required.'],
        'subject': ['This field is required.'],
        'message': ['This field is required.']
    }


def test_contactus_post_valid_data(api_client, mailoutbox):
    initial_count = ContactUs.objects.count()
    payload = {
        'name': 'Example Name',
        'email_from': 'emailcontactus@example.com',
        'subject': 'Subject Example',
        'message': 'Example Text\n' * 10
    }
    response = api_client.post(reverse('v1:contactus-list'), data=payload)
    assert response.status_code == 201
    assert response.json()

    assert len(mailoutbox) == 1
    assert ContactUs.objects.count() == initial_count + 1
    assert mailoutbox[0].to == [settings.DEFAULT_FROM_EMAIL]
    assert mailoutbox[0].subject == 'Contact us: Subject Example'


def test_contactus_patch(api_client):
    contact = ContactUs.objects.create(name=23, email_from=settings.DEFAULT_FROM_EMAIL, subject='Subject Example',
                                       message='Example Text\n' * 10)
    payload = {
        'name': 'New Name',
    }
    response = api_client.patch(reverse('v1:contactus-detail', args=[contact.id]), data=payload)
    assert response.status_code == 200
    assert response.json()


def test_contactus_delete(api_client):
    contact = ContactUs.objects.create(name=23, email_from=settings.DEFAULT_FROM_EMAIL, subject='Subject Example',
                                       message='Example Text\n' * 10)
    response = api_client.delete(reverse('v1:contactus-detail', args=[contact.id]))
    assert response.status_code == 204
    assert response.content == b''


def test_rates_get_list(api_client):
    response = api_client.get(reverse('v1:rate-list'))
    assert response.status_code == 200
    assert response.json()


def test_rates_post_empty_data(api_client):
    response = api_client.post(reverse('v1:rate-list'), data={})
    assert response.status_code == 400
    assert response.json() == {
        'sale': ['This field is required.'],
        'buy': ['This field is required.'],
        'source': ['This field is required.'],
    }


def test_rates_post_valid_data(api_client):
    source = Source.objects.last()
    payload = {
        'sale': 23,
        'buy': 24,
        'source': source.id,
    }
    response = api_client.post(reverse('v1:rate-list'), data=payload)
    assert response.status_code == 201
    assert response.json()


def test_rates_patch_valid_data(api_client):
    rate = Rate.objects.last()

    payload = {
        'sale': 9999,
    }
    response = api_client.patch(reverse('v1:rate-detail', args=[rate.id]), data=payload)
    assert response.status_code == 200
    assert response.json()['sale'] == '9999.00'


def test_rates_delete(api_client):
    rate = Rate.objects.last()

    response = api_client.delete(reverse('v1:rate-detail', args=[rate.id]))
    assert response.status_code == 204
    assert response.content == b''
