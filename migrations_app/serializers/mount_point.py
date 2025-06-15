from rest_framework import serializers

from ..models.mount_point import MountPoint


class MountPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = MountPoint
        fields = ['id', 'name', 'total_size', 'workload']
