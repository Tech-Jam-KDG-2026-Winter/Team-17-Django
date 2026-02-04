from .base import *  # noqa

DEBUG = True
# 開発のために上書きしてAI機能をOFFにしておく
AI_ENABLED = False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "greyson-pointilla-cindi.ngrok-free.dev",
]

CSRF_TRUSTED_ORIGINS = [
    "https://greyson-pointilla-cindi.ngrok-free.dev",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")