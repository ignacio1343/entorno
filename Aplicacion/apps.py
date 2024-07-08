from django.apps import AppConfig


class AplicacionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Aplicacion'

class AppConfig(AppConfig):
    name = 'app'
    verbose_name = "Otaku Odyssey"
    
from django.apps import AppConfig

