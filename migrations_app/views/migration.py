from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models.migration import Migration
from ..serializers.migration import MigrationSerializer


class MigrationViewSet(viewsets.ModelViewSet):
    queryset = Migration.objects.all()
    serializer_class = MigrationSerializer

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        migration = self.get_object()
        try:
            migration.run()
            return Response({'status': 'migration started'})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        migration = self.get_object()
        return Response({'state': migration.state})
