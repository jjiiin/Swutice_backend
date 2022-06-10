from django.shortcuts import render
from django.http import HttpResponse
import pyrebase

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# cred = credentials.Certificate('serviceAccountKey.json')
# firebase= firebase_admin.initialize_app(cred)
# firebase_admin.get_app()
# try:
#     app = firebase_admin.get_app()
# except ValueError as e:
#     cred = credentials.Certificate('serviceAccountKey.json')
#     firebase_admin.initialize_app(cred)
#cred_path = os.path.join(BASE_DIR, "serviceAccountKey.json")
# cred = credentials.Certificate('serviceAccountKey.json')
# firebase_admin.initialize_app(cred,{
#     'databaseURL': 'https://swprojectapp-default-rtdb.firebaseio.com'
# })

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import os

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup

firebaseConfig = {
    "apiKey": "AIzaSyAjJNUWcRdpfeuiytIB_22ZjFXn_ydoHqw",
    "authDomain": "swprojectapp.firebaseapp.com",
    "databaseURL": "https://swprojectapp-default-rtdb.firebaseio.com",
    "projectId": "swprojectapp",
    "storageBucket": "swprojectapp.appspot.com",
    "messagingSenderId": "1063005594107",
    "appId": "1:1063005594107:web:2df2ef2ad8ea33a4ebab5e",
    "measurementId": "G-D3J218FJBZ"
}
# firebase =pyrebase.initialize_app(firebaseConfig)


# db=firebase.database()
# auth=firebase.auth()

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

schedule.every(3).seconds.do(keyword_scraping)
#schedule.every(1).hours.do(send_to_firebase_cloud_messaging_test)

def job():
    print("do")
    schedule.run_pending()
    job()
def scrap(request):
    # url="https://www.swu.ac.kr/www/noticea.html"
    # headers={
    #     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    #     "Accept-Language":"ko-KR,ko"}
    # res=requests.get(url,headers=headers)
    # res.raise_for_status()
    # soup = BeautifulSoup(res.text, "lxml")
    # with open("swu_noticea.html","w",encoding="utf8")as f:
    #     f.write(res.text)
    while True :
        job()
        return HttpResponse('hello myapp!0610')
    # db.child("name").push({"company":"google0525_noon"})
    # ref=db.reference('keyword')
    # print(ref.get())
    
    
