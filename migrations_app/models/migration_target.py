from django.db import models
from django.core.exceptions import ValidationError
from .credentials import Credentials
from .workload import Workload


class CloudType(models.TextChoices):
    AWS = 'aws'
    AZURE = 'azure'
    VSPHERE = 'vsphere'
    VCLOUD = 'vcloud'


class MigrationTarget(models.Model):
    cloud_type = models.CharField(
        max_length=10,
        choices=CloudType.choices
    )
    cloud_credentials = models.OneToOneField(
        Credentials,
        on_delete=models.CASCADE
    )
    target_vm = models.OneToOneField(
        Workload,
        on_delete=models.CASCADE
    )
