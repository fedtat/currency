from django.core.management import call_command

import pytest


@pytest.fixture(autouse=True, scope="function")
def enable_db_access_for_all_tests(db):
    """
    give access to database for all tests
    """


@pytest.fixture(autouse=True, scope="function")
def load_fixtures(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        fixtures = (
            'contactus.json',
            'sources.json',
            'rates.json',
        )
        for fixture in fixtures:
            call_command('loaddata', f'app/tests/fixtures/{fixture}')
