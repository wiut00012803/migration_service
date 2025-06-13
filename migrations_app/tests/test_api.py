import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models.credentials import Credentials
from ..models.workload import Workload

User = get_user_model()


@pytest.mark.django_db
class TestWorkloadAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_cannot_modify_ip(self):
        credentials = Credentials.objects.create(
            username="test",
            password="test",
            domain="test"
        )

        workload = Workload.objects.create(
            ip="192.168.1.1",
            credentials=credentials
        )

        response = self.client.patch(
            reverse('workload-detail', kwargs={'pk': workload.pk}),
            {'ip': '192.168.1.2'},
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        workload.refresh_from_db()
        assert workload.ip == "192.168.1.1"

    def teardown_method(self):
        User.objects.all().delete()
        Workload.objects.all().delete()
        Credentials.objects.all().delete()
