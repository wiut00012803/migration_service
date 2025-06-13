from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.workload import Workload
from ..serializers.workload import WorkloadSerializer

class WorkloadViewSet(viewsets.ModelViewSet):
    queryset = Workload.objects.all()
    serializer_class = WorkloadSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'ip' in request.data and request.data['ip'] != instance.ip:
            return Response(
                {"error": "IP address cannot be modified"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'ip' in request.data and request.data['ip'] != instance.ip:
            return Response(
                {"error": "IP address cannot be modified"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().partial_update(request, *args, **kwargs)