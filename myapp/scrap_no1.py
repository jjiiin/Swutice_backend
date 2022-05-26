# Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from django.db import connections
import sqlite3
from .fb_read import*
from .push_fcm_notification import *

def scraping():
    url="https://www.swu.ac.kr//front/boardlist.do?bbsConfigFK=4&currentPage=$1"
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Accept-Language":"ko-KR,ko"}
    res=requests.get(url,headers=headers)
    res.raise_for_status()
    soup=BeautifulSoup(res.text,'html.parser',from_encoding="utf-8")
    tbody=soup.find("tbody")
    announcements=tbody.find_all("tr")
    title_before=titleGetDB()[0]
    #print(kwList)['계절', '방학']
    cnt=0
    count=0
    title_update=""
    for index, value in enumerate(announcements):
        temp=value.find_all("td")
        temp_index=str(temp[0].text).replace("\n","")
        #print(temp_index)
        if count == 1:
            title_before=titleGetDB()[0]
        if temp_index not in "TOP":
            #print("top:"+temp[0].text)
            id=str(temp[0].text).replace("\n","")
            title=str(temp[1].text).replace("\n","").replace("새글","")
            #sqlite에 저장된 공지(제목)과 크롤링해온 제목 비교하기
            print("title_before"+title_before)
            if(title_before!=title):
                cnt+=1
                find_link=temp[1].a.attrs["onclick"].split("'")
                frag_link=str(find_link[3])
                link="http://www.swu.ac.kr/front/boardview.do?&pkid=" + frag_link +"&currentPage=1&menuGubun=1&siteGubun=1&bbsConfigFK=4&searchField=ALL&searchValue=&searchLowItem=ALL"
                contents=contentExtraction(link)
                #키워드 리스트랑 비교해서 푸쉬알림 보내기
                pushNotification(title,link)
                print(title)
                if(cnt==1):
                    title_update=title
                #fb-keyword목록과 비교하기
            else: 
                print("title_update"+title_update)
                updateDB(title_update)
                count+=1
                break
    

def contentExtraction(link):
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Accept-Language":"ko-KR,ko"}
    res=requests.get(link,headers=headers)
    res.raise_for_status()
    soup=BeautifulSoup(res.text,'html.parser',from_encoding="utf-8")
    content_text=soup.find("div",{"class":"contents"}).text.replace("\n","")
    return(str(content_text))

def pushNotification(title,link):
    kwList=keywordList()#파이어베이스에서 keyword리스트 가져옴
    print(kwList)
    for i in kwList:
        if(i in title):
            #fb에서 토큰 찾아서 리스트로 만들기
            tkList=tokenList(i)
            print(tkList)
            dept="학사"
            for j in tkList:
                print(j)
                send_to_firebase_cloud_messaging(dept,i,j,link)


def titleGetDB():
    con=sqlite3.connect('./db.sqlite3')
    cur=con.cursor()
    dept=("main_1",)
    cur.execute("SELECT title FROM myapp_recent_ann WHERE dept=?",(dept))
    con.commit()
    result=cur.fetchone()
    cur.close()
    con.close()
    return result

def updateDB(title):
    con=sqlite3.connect('./db.sqlite3')
    cur=con.cursor()
    dept="main_1"
    cur.execute("UPDATE myapp_recent_ann SET title=? WHERE dept= ?",(title, dept,))
    con.commit()
    cur.close()
    con.close()