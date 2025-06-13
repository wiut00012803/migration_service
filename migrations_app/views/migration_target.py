from rest_framework import viewsets

from ..models.migration_target import MigrationTarget
from ..serializers.migration_target import MigrationTargetSerializer


class MigrationTargetViewSet(viewsets.ModelViewSet):
    queryset = MigrationTarget.objects.all()
    serializer_class = MigrationTargetSerializer
