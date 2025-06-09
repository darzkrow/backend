from django.apps import AppConfig


class ManualsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manuals'
    verbose_name = 'Manuales & Procedimientos'

    def ready(self):
        import manuals.signals # Importa tus señales aquí