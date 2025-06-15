from rest_framework import serializers

from ..models.migration import Migration


class MigrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Migration
        fields = ['id', 'source', 'target', 'selected_mount_points', 'state']
        read_only_fields = ['state']

    def validate(self, data):
        source = data.get('source') or self.instance.source
        for mp in data.get('selected_mount_points', []):
            if mp.workload_id != source.id:
                raise serializers.ValidationError(
                    "All selected mount points must belong to the source workload"
                )
        return data
