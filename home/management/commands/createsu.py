from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            User.objects.filter(username='admin').first().delete()
        if not User.objects.filter(username="dj@dminuser").exists():
            User.objects.create_superuser("dj@dminuser", "admin@admin.com", "admin")