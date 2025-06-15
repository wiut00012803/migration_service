import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from migrations_app.models.credentials import Credentials
from migrations_app.models.migration import Migration, MigrationState
from migrations_app.models.migration_target import MigrationTarget, CloudType
from migrations_app.models.mount_point import MountPoint
from migrations_app.models.workload import Workload


@pytest.mark.django_db
def test_credentials_clean_empty():
    c = Credentials(username='', password='', domain='x')
    with pytest.raises(ValidationError):
        c.clean()


@pytest.mark.django_db
def test_workload_unique_and_immutable():
    c1 = Credentials.objects.create(username='u1', password='p1', domain='d')
    w1 = Workload.objects.create(ip='10.0.0.1', credentials=c1)
    with pytest.raises(ValidationError):
        w1.ip = '1.2.3.4'
        w1.save()
    c2 = Credentials.objects.create(username='u2', password='p2', domain='d')
    with pytest.raises(IntegrityError):
        Workload.objects.create(ip='10.0.0.1', credentials=c2)


@pytest.mark.django_db
def test_mount_point_fk_relation():
    c = Credentials.objects.create(username='u', password='p', domain='d')
    w = Workload.objects.create(ip='10.0.0.2', credentials=c)
    mp = MountPoint.objects.create(name='C:\\', total_size=100, workload=w)
    assert list(w.mount_points.all()) == [mp]


@pytest.mark.django_db
def test_migration_run_no_c(monkeypatch):
    monkeypatch.setattr('migrations_app.models.migration.time.sleep', lambda x: None)
    c1 = Credentials.objects.create(username='u1', password='p1', domain='d')
    src = Workload.objects.create(ip='10.0.0.3', credentials=c1)
    MountPoint.objects.create(name='D:\\', total_size=50, workload=src)
    c2 = Credentials.objects.create(username='u2', password='p2', domain='d')
    tgt_vm = Workload.objects.create(ip='10.0.0.4', credentials=c2)
    mt = MigrationTarget.objects.create(
        cloud_type=CloudType.AWS, cloud_credentials=c2, target_vm=tgt_vm
    )
    mig = Migration.objects.create(source=src, target=mt)
    with pytest.raises(ValidationError):
        mig.run()
    assert mig.state == MigrationState.NOT_STARTED


@pytest.mark.django_db
def test_migration_run_success_and_copy(monkeypatch):
    monkeypatch.setattr('migrations_app.models.migration.time.sleep', lambda x: None)
    c1 = Credentials.objects.create(username='u1', password='p1', domain='d')
    src = Workload.objects.create(ip='10.0.0.5', credentials=c1)
    mp_c = MountPoint.objects.create(name='C:\\', total_size=100, workload=src)
    mp_d = MountPoint.objects.create(name='D:\\', total_size=50, workload=src)
    c2 = Credentials.objects.create(username='u2', password='p2', domain='d')
    tgt_vm = Workload.objects.create(ip='10.0.0.6', credentials=c2)
    mt = MigrationTarget.objects.create(
        cloud_type=CloudType.AZURE, cloud_credentials=c2, target_vm=tgt_vm
    )
    mig = Migration.objects.create(source=src, target=mt)
    mig.selected_mount_points.set([mp_c])
    mig.run()
    assert mig.state == MigrationState.SUCCESS
    copied = tgt_vm.mount_points.all()
    assert copied.count() == 1
    assert copied[0].name == 'C:\\'
    assert copied[0].total_size == 100
