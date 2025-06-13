from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.migration import MigrationViewSet
from .views.migration_target import MigrationTargetViewSet
from .views.mount_point import MountPointViewSet
from .views.workload import WorkloadViewSet

router = DefaultRouter()
router.register(r'workloads', WorkloadViewSet)
router.register(r'migrations', MigrationViewSet)
router.register(r'mount-points', MountPointViewSet)
router.register(r'migration-targets', MigrationTargetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
