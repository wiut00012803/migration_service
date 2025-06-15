from rest_framework import serializers

from ..models.migration_target import MigrationTarget


class MigrationTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MigrationTarget
        fields = ['id', 'cloud_type', 'cloud_credentials', 'target_vm']

    def validate_cloud_type(self, value):
        valid = ['aws', 'azure', 'vsphere', 'vcloud']
        val = value.lower()
        if val not in valid:
            raise serializers.ValidationError(f"Cloud type must be one of {', '.join(valid)}")
        return val
