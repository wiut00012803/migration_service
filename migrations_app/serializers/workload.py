from rest_framework import serializers
from ..models.workload import Workload


class WorkloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workload
        fields = ['ip', 'credentials']
        read_only_fields = ['ip']
