from io import StringIO

import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_check():
    out = StringIO()
    call_command('check', stdout=out)
    assert 'db:\tok' in out.getvalue()
    assert 'env:\tok' in out.getvalue()
