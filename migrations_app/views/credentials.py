from rest_framework import viewsets

from ..models.credentials import Credentials
from ..serializers.credentials import CredentialsSerializer


class CredentialsViewSet(viewsets.ModelViewSet):
    queryset = Credentials.objects.all()
    serializer_class = CredentialsSerializer
