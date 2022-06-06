from django.apps import AppConfig
import sys
# import crypto
# sys.modules['Crypto']=crypto
#from crypto.Cipher import AES

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

