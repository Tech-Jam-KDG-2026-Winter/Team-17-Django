from django.contrib import admin
from django.http import JsonResponse
from django.urls import path

# src/config/urls.py
def root(request):
    return JsonResponse({"service": "django-starter", "status": "ok"})

# 起動確認のため
def healthz(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("",root),
    path("admin/", admin.site.urls),
    path("healthz/", healthz),
]
