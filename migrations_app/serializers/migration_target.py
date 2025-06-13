from rest_framework import serializers

from ..models.migration_target import MigrationTarget


class MigrationTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MigrationTarget
        fields = ['cloud_type', 'cloud_credentials', 'target_vm']

    def validate_cloud_type(self, value):
        valid_types = ['aws', 'azure', 'vsphere', 'vcloud']
        if value.lower() not in valid_types:
            raise serializers.ValidationError(
                f"Cloud type must be one of {', '.join(valid_types)}"
            )
        return value.lower()
