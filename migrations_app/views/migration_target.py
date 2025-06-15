from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models.migration_target import MigrationTarget
from ..serializers.migration_target import MigrationTargetSerializer


class MigrationTargetViewSet(viewsets.ModelViewSet):
    queryset = MigrationTarget.objects.all()
    serializer_class = MigrationTargetSerializer

    def update(self, request, *args, **kwargs):
        inst = self.get_object()
        if 'cloud_type' in request.data and request.data['cloud_type'] != inst.cloud_type:
            return Response({"error": "cloud_type cannot be modified"}, status=status.HTTP_400_BAD_REQUEST)
        if 'target_vm' in request.data and int(request.data['target_vm']) != inst.target_vm_id:
            return Response({"error": "target_vm cannot be modified"}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
