from rest_framework import serializers

from ..models.mount_point import MountPoint


class MountPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = MountPoint
        fields = ['name', 'total_size', 'workload']
