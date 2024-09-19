from django.apps import AppConfig
import logging


class CommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.common"

    # comment this for first time running.
    # comment , migrate and then un comment it
    def ready(self):
        from .scheduler import start_scheduler

        # Start the scheduler
        start_scheduler()
