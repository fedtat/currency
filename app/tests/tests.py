from currency.models import ContactUs

from django.conf import settings


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_contact_us_get(admin_custom_client):
    response = admin_custom_client.get('/currency/contactus/create/')
    assert response.status_code == 200


def test_contact_us_post_empty_data(admin_custom_client):
    response = admin_custom_client.post('/currency/contactus/create/')
    assert response.status_code == 200  # when post 200 is error
    assert response.context_data['form'].errors == {
        'name': ['This field is required.'],
        'email_from': ['This field is required.'],
        'subject': ['This field is required.'],
        'message': ['This field is required.'],
    }


def test_contact_us_post_valid_data(admin_custom_client, mailoutbox):
    initial_count = ContactUs.objects.count()
    payload = {
        'name': 'Example Name',
        'email_from': 'emailcontactus@example.com',
        'subject': 'Subject Example',
        'message': 'Example Text\n' * 10,
    }
    response = admin_custom_client.post('/currency/contactus/create/', data=payload)
    assert response.status_code == 302
    assert response.url == '/'

    assert len(mailoutbox) == 1
    assert mailoutbox[0].to == [settings.DEFAULT_FROM_EMAIL]
    assert mailoutbox[0].subject == 'User ContactUs'

    assert ContactUs.objects.count() == initial_count + 1


def test_contact_us_post_invalid_email(admin_custom_client, mailoutbox):
    initial_count = ContactUs.objects.count()
    payload = {
        'name': 'Example Name',
        'email_from': 'emailcontactus',
        'subject': 'Subject Example',
        'message': 'Example Text\n' * 10,
    }
    response = admin_custom_client.post('/currency/contactus/create/', data=payload)
    assert response.status_code == 200
    assert response.context_data['form'].errors == {'email_from': ['Enter a valid email address.']}
    assert len(mailoutbox) == 0

    assert ContactUs.objects.count() == initial_count
