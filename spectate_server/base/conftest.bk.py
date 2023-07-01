import pytest
from django.conf import settings
from django.core.management import call_command
from django.db import connections

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture(scope='session')
def django_db_setup():
    # Create a SQLite in-memory database for testing
    # settings = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': ':memory',
    #     }
    # }
    # # Create the test database
    # connections.databases = settings

    # Override the DATABASES setting for testing
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
    call_command('makemigrations')
    call_command('migrate')


@pytest.fixture
def db(django_db_setup, django_db_blocker):
    # Use a Django database connection for each test
    with django_db_blocker.unblock():
        yield


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
