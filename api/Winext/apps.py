from django.apps import AppConfig

class WinextConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Winext'

    def ready(self):
        import Winext.signals
