# migrations_app/apps.py
from django.apps import AppConfig

class MigrationsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'migrations_app'