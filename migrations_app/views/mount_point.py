from rest_framework import viewsets

from ..models.mount_point import MountPoint
from ..serializers.mount_point import MountPointSerializer


class MountPointViewSet(viewsets.ModelViewSet):
    queryset = MountPoint.objects.all()
    serializer_class = MountPointSerializer
