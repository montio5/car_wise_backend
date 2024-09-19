import os
import sys
from django.core.management.base import BaseCommand
from apps.common.tasks import send_notifications


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_notifications()
