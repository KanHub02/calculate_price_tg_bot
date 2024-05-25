from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "common"



class CustomAuthConfig(AppConfig):
    name = 'django.contrib.auth'
    verbose_name = 'Пользователи'