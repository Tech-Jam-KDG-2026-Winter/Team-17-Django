import os
from django.core.asgi import get_asgi_application
# src/config/asgi.py

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

application = get_asgi_application()
