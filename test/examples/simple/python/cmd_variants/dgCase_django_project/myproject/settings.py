import os

SECRET_KEY = "dummy-secret-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
]

MIDDLEWARE = []

ROOT_URLCONF = "myproject.urls"

TEMPLATES = []

WSGI_APPLICATION = "myproject.wsgi.application"
