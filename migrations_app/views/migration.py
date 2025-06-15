from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models.migration import Migration
from ..serializers.migration import MigrationSerializer


class MigrationViewSet(viewsets.ModelViewSet):
    queryset = Migration.objects.all()
    serializer_class = MigrationSerializer

    def update(self, request, *args, **kwargs):
        inst = self.get_object()
        if 'source' in request.data and int(request.data['source']) != inst.source_id:
            return Response({"error": "source cannot be modified"}, status=status.HTTP_400_BAD_REQUEST)
        if 'target' in request.data and int(request.data['target']) != inst.target_id:
            return Response({"error": "target cannot be modified"}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        mig = self.get_object()
        try:
            mig.run()
            return Response({'status': 'migration started'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        mig = self.get_object()
        return Response({'state': mig.state})
