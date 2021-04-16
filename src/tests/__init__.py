

import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbres_background.settings")  # 应用django api
import django

django.setup()

from src.register_urls import router
from rest_framework.routers import DefaultRouter
print(router.get_urls())
