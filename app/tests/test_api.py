from currency.models import ContactUs

from django.conf import settings
from django.urls import reverse

from rest_framework.test import APIClient


def test_contactus_get_contact():
    client = APIClient()
    response = client.get(reverse('v1:contactus-list'))
    assert response.status_code == 200
    assert response.json() == []


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
    assert response.json()['name'] == 'New Name'


def test_contactus_delete():
    client = APIClient()
    contact = ContactUs.objects.create(name=23, email_from=settings.DEFAULT_FROM_EMAIL, subject='Subject Example',
                                       message='Example Text\n' * 10)
    response = client.delete(reverse('v1:contactus-detail', args=[contact.id]))
    assert response.status_code == 204
    assert response.content == b''
