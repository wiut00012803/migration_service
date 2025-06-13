from rest_framework import serializers

from ..models.credentials import Credentials


class CredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credentials
        fields = ['username', 'password', 'domain']
       