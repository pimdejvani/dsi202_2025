from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # กำหนด default_auto_field
    name = 'myapp'  # กำหนดชื่อแอป

    def ready(self):
        import myapp.signals  # นำเข้า signals ในเมธอด ready()