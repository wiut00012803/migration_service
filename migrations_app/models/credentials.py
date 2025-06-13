from django.core.exceptions import ValidationError
from django.db import models


class Credentials(models.Model):
    username = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
    domain = models.CharField(max_length=255)

    def clean(self) -> None:
        if not self.username or not self.password:
            raise ValidationError("Username and password cannot be None")
