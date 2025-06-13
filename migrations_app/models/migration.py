import time
from typing import TYPE_CHECKING

from django.db import models
from django.db.models import QuerySet

from .migration_target import MigrationTarget
from .mount_point import MountPoint
from .workload import Workload



class MigrationState(models.TextChoices):
    NOT_STARTED = 'not_started'
    RUNNING = 'running'
    ERROR = 'error'
    SUCCESS = 'success'


class Migration(models.Model):
    source = models.ForeignKey(
        Workload,
        on_delete=models.CASCADE,
        related_name='source_migrations'
    )
    target = models.ForeignKey(
        MigrationTarget,
        on_delete=models.CASCADE,
        related_name='migrations'
    )
    state = models.CharField(
        max_length=20,
        choices=MigrationState.choices,
        default=MigrationState.NOT_STARTED
    )

    def run(self) -> None:
        if not self._validate_mount_points():
            raise ValueError("Migration cannot run without C:\\ mount point")

        self.state = MigrationState.RUNNING
        self.save()

        try:
            time.sleep(300)

            self._copy_mount_points()

            self.state = MigrationState.SUCCESS
        except Exception as e:
            self.state = MigrationState.ERROR
            raise
        finally:
            self.save()

    def _validate_mount_points(self) -> bool:
        mount_points: QuerySet[MountPoint] = self.selected_mount_points.all()
        return any(
            mp.name.lower().startswith('c:')
            for mp in mount_points
        )

    def _copy_mount_points(self) -> None:
        pass