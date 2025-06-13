from django.db import models


class MountPoint(models.Model):
    name = models.CharField(max_length=255)  # e.g., "c:\"
    total_size = models.IntegerField()
    workload = models.ForeignKey(
        'Workload',
        on_delete=models.CASCADE,
        related_name='mount_points'
    )
