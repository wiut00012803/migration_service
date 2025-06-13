from django.core.exceptions import ValidationError
from django.db import models
from .credentials import Credentials

class Workload(models.Model):
    ip = models.CharField(max_length=255, unique=True)
    credentials = models.OneToOneField(
        Credentials,
        on_delete=models.CASCADE,
        related_name='workload'
    )

    def clean(self) -> None:
        if not self.ip:
            raise ValidationError("IP cannot be None")

    def save(self, *args, **kwargs):
        if self.pk:
            orig = Workload.objects.get(pk=self.pk)
            if orig.ip != self.ip:
                raise ValidationError("IP cannot be changed")
        super().save(*args, **kwargs)
