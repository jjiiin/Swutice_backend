from django.apps import AppConfig
import Crypto
import sys
sys.modules['Crypto']=crypto

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

