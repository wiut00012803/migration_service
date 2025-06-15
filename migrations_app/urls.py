from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.credentials import CredentialsViewSet
from .views.migration import MigrationViewSet
from .views.migration_target import MigrationTargetViewSet
from .views.mount_point import MountPointViewSet
from .views.workload import WorkloadViewSet

router = DefaultRouter()
router.register(r'credentials', CredentialsViewSet)
router.register(r'workloads', WorkloadViewSet)
router.register(r'mount-points', MountPointViewSet)
router.register(r'migration-targets', MigrationTargetViewSet)
router.register(r'migrations', MigrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
