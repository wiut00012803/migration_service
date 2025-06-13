from rest_framework import serializers
from ..models.migration import Migration


class MigrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Migration
        fields = ['source', 'target', 'selected_mount_points', 'state']
        read_only_fields = ['state']
