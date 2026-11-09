"""Изолированная БД для pytest без изменения рабочей базы Django."""
import os
import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moodtracker.settings")
django.setup()

from django.core.management import call_command  # noqa: E402
from django.test.utils import (  # noqa: E402
    setup_databases, teardown_databases, setup_test_environment,
    teardown_test_environment,
)


@pytest.fixture(scope="session", autouse=True)
def django_database():
    setup_test_environment()
    config = setup_databases(verbosity=0, interactive=False)
    call_command("import_pr7", verbosity=0)
    yield
    teardown_databases(config, verbosity=0)
    teardown_test_environment()
