import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from migrations_app.models.migration import MigrationState


@pytest.fixture
def client(db):
    u = User.objects.create_user(username='t', password='pw')
    c = APIClient()
    c.login(username='t', password='pw')
    return c


@pytest.mark.django_db
def test_workload_and_credentials_and_ip_guard(client):
    r = client.post('/api/credentials/', {'username': 'u', 'password': 'p', 'domain': 'd'}, format='json')
    assert r.status_code == 201
    cred = r.data['id']
    r = client.post('/api/workloads/', {'ip': '1.2.3.4', 'credentials': cred}, format='json')
    assert r.status_code == 201
    wid = r.data['id']
    r = client.patch(f'/api/workloads/{wid}/', {'ip': '9.9.9.9'}, format='json')
    assert r.status_code == 400


@pytest.mark.django_db
def test_mount_point_crud(client):
    r = client.post('/api/credentials/', {'username': 'u', 'password': 'p', 'domain': 'd'}, format='json')
    cred = r.data['id']
    r = client.post('/api/workloads/', {'ip': '1.1.1.1', 'credentials': cred}, format='json')
    wid = r.data['id']
    r = client.post('/api/mount-points/', {'name': 'X:\\', 'total_size': 10, 'workload': wid}, format='json')
    assert r.status_code == 201
    mp = r.data['id']
    r = client.get('/api/mount-points/')
    assert r.status_code == 200
    r = client.put(f'/api/mount-points/{mp}/', {'name': 'Y:\\', 'total_size': 20, 'workload': wid}, format='json')
    assert r.status_code == 200
    r = client.patch(f'/api/mount-points/{mp}/', {'total_size': 30}, format='json')
    assert r.status_code == 200


@pytest.mark.django_db
def test_migration_target_crud_and_immutable(client):
    r = client.post('/api/credentials/', {'username': 'u1', 'password': 'p1', 'domain': 'd'}, format='json')
    cred1 = r.data['id']
    r = client.post('/api/workloads/', {'ip': '2.2.2.2', 'credentials': cred1}, format='json')
    vm1 = r.data['id']
    r = client.post('/api/credentials/', {'username': 'u2', 'password': 'p2', 'domain': 'd'}, format='json')
    cred2 = r.data['id']
    r = client.post('/api/workloads/', {'ip': '2.2.2.3', 'credentials': cred2}, format='json')
    vm2 = r.data['id']
    r = client.post('/api/migration-targets/', {'cloud_type': 'aws', 'cloud_credentials': cred2, 'target_vm': vm2},
                    format='json')
    assert r.status_code == 201
    mt = r.data['id']
    r = client.patch(f'/api/migration-targets/{mt}/', {'cloud_type': 'azure'}, format='json')
    assert r.status_code == 400


@pytest.mark.django_db
def test_migration_start_and_status(client, monkeypatch):
    monkeypatch.setattr('migrations_app.models.migration.time.sleep', lambda x: None)
    # source
    r = client.post('/api/credentials/', {'username': 'u1', 'password': 'p1', 'domain': 'd'}, format='json')
    cred1 = r.data['id']
    r = client.post('/api/workloads/', {'ip': '3.3.3.3', 'credentials': cred1}, format='json')
    src = r.data['id']
    r = client.post('/api/mount-points/', {'name': 'C:\\', 'total_size': 10, 'workload': src}, format='json')
    mp = r.data['id']
    # target
    r = client.post('/api/credentials/', {'username': 'u2', 'password': 'p2', 'domain': 'd'}, format='json')
    cred2 = r.data['id']
    r = client.post('/api/workloads/', {'ip': '3.3.3.4', 'credentials': cred2}, format='json')
    tgt_vm = r.data['id']
    r = client.post('/api/migration-targets/',
                    {'cloud_type': 'vcloud', 'cloud_credentials': cred2, 'target_vm': tgt_vm}, format='json')
    tgt = r.data['id']
    # migration
    r = client.post('/api/migrations/', {'source': src, 'target': tgt, 'selected_mount_points': [mp]}, format='json')
    assert r.status_code == 201
    mid = r.data['id']
    r = client.post(f'/api/migrations/{mid}/start/')
    assert r.status_code == 200 and r.data['status'] == 'migration started'
    r = client.get(f'/api/migrations/{mid}/status/')
    assert r.status_code == 200 and r.data['state'] == MigrationState.SUCCESS
