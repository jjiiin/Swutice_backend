from django.apps import AppConfig
from .scrap_no1 import *
from .scrap_no2 import *
from .scrap_no3 import *
from .scrap_no4 import *
from .scrap_no5 import *
from .scrap_security import *
from .scrap_korean import *
from .scrap_biz import *
from .scrap_digitalMedia import *
from .scrap_libraryInfo import *
from .scrap_socialWelfare import *
from .scrap_software import *
from .scrap_japanese import *
from .scrap_german import *
from .scrap_history import *
from .push_fcm_notification import send_to_firebase_cloud_messaging_test
import schedule
import time
def keyword_scraping():
    #학교
    scraping_no1()#학사 
    scraping_no2()#장학
    scraping_no3()#행사
    scraping_no4()#채용/취업
    scraping_no5()#일반/봉사

    #학과
    scraping_security()#정보보호학과
    scraping_dm()#디지털미디어학과
    scraping_software()#소프트웨어융합학과
    scraping_korean()#국어국문학과
    scraping_history()#사학과
    scraping_biz()#경영학과

def job():
    print("do")
    schedule.every(3).seconds.do(keyword_scraping)

class MyAppConfig(AppConfig):
    name='myapp'
    verbose_name=" MY app"

    def ready(self):
        job()
        pass
