import pytest
from django.core.exceptions import ValidationError

from ..models.credentials import Credentials
from ..models.workload import Workload


@pytest.mark.django_db
class TestWorkload:
    def test_ip_cannot_be_none(self):
        with pytest.raises(ValidationError):
            workload = Workload(ip=None)
            workload.full_clean()

    def test_ip_cannot_be_changed(self):
        credentials = Credentials.objects.create(
            username="test",
            password="test",
            domain="test"
        )
        workload = Workload.objects.create(
            ip="192.168.1.1",
            credentials=credentials
        )

        with pytest.raises(ValidationError):
            workload.ip = "192.168.1.2"
            workload.save()
