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
import schedule
import time


def keyword_scraping():
    #학교
    scraping_no1()#학사 #키워드 알림을 위해 그 전 공지사항으로 제목 맞추기
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
    
    # scraping_libraryInfo()#문헌정보학과
    # scraping_socialWelfare()#사회복지학과  
    # scraping_japanese()#일어일문학과
    # scraping_germany()#독어독문학과
    

schedule.every(3).minutes.do(keyword_scraping)

while True:
    schedule.run_pending()
    time.sleep(1)