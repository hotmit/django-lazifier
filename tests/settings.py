# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import
import os

import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
USE_TZ = True

USE_I18N = True
USE_L10N = True
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'django_lazifier', 'locale')
]

LANGUAGE_CODE = 'en'
LANGUAGES = [
  ('en', 'English'),
  ('vi', 'Tiếng Việt'),
]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django_lazifier",
]

SITE_ID = 1

if django.VERSION >= (1, 10):
    MIDDLEWARE = ()
else:
    MIDDLEWARE_CLASSES = ()
