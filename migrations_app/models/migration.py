import time

from django.core.exceptions import ValidationError
from django.db import models

from .migration_target import MigrationTarget
from .mount_point import MountPoint
from .workload import Workload


class MigrationState(models.TextChoices):
    NOT_STARTED = "not_started"
    RUNNING = "running"
    ERROR = "error"
    SUCCESS = "success"


class Migration(models.Model):
    source = models.ForeignKey(
        Workload, on_delete=models.CASCADE, related_name="source_migrations"
    )
    target = models.ForeignKey(
        MigrationTarget, on_delete=models.CASCADE, related_name="migrations"
    )
    selected_mount_points = models.ManyToManyField(
        MountPoint, related_name="migrations"
    )
    state = models.CharField(
        max_length=20, choices=MigrationState.choices, default=MigrationState.NOT_STARTED
    )

    def run(self) -> None:
        if self.state == MigrationState.RUNNING:
            raise ValidationError("Migration is already running")
        if not any(mp.name.lower().startswith("c:") for mp in self.selected_mount_points.all()):
            raise ValidationError("Migration must include at least one C:\\ volume")
        self.state = MigrationState.RUNNING
        self.save()
        try:
            time.sleep(1)
            self._copy_mount_points()
            self.state = MigrationState.SUCCESS
        except Exception:
            self.state = MigrationState.ERROR
            raise
        finally:
            self.save()

    def _copy_mount_points(self) -> None:
        tgt_vm = self.target.target_vm
        tgt_vm.mount_points.all().delete()
        for mp in self.selected_mount_points.all():
            MountPoint.objects.create(
                name=mp.name, total_size=mp.total_size, workload=tgt_vm
            )
