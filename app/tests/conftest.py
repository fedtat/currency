import uuid

from accounts.models import User

from django.core.management import call_command

import pytest

from rest_framework.test import APIClient


@pytest.fixture(autouse=True, scope="function")
def enable_db_access_for_all_tests(db):
    """
    give access to database for all tests
    """


@pytest.fixture(autouse=True, scope="session")
def load_fixtures(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        fixtures = (
            'contactus.json',
            'sources.json',
            'rates.json',
        )
        for fixture in fixtures:
            call_command('loaddata', f'app/tests/fixtures/{fixture}')


@pytest.fixture()
def api_client():
    client = APIClient()
    yield client


@pytest.fixture(scope='module')
def admin_custom_client(django_db_setup, django_db_blocker):
    from django.test.client import Client

    with django_db_blocker.unblock():
        email = str(uuid.uuid4()).replace('-', '') + '@gmail.com'
        user = User.objects.create(email=email, is_staff=True, is_superuser=True, is_active=True)

        client = Client()
        client.force_login(user)
        yield client
