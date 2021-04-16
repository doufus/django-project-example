
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# print(BASE_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbres_background.settings")  # 应用django api
import django

django.setup()
from rest_framework.authtoken.models import Token
token = Token.objects.create(user_id=1)
print(token.key)