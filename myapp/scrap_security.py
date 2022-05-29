from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from django.db import connections
import sqlite3
from .fb_read import*
from .push_fcm_notification import *

def scraping_security():
    url="http://security.swu.ac.kr/sub.html?page=department_notice&page1=1&searchKey=&searchValue="
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Accept-Language":"ko-KR,ko"}
    res=requests.get(url,headers=headers)
    res.raise_for_status()
    soup=BeautifulSoup(res.text,'html.parser',from_encoding="utf-8")
    tbody=soup.find("tbody")
    announcements=tbody.find_all("tr")
    # if titleGetDB()!="":
    #     title_before=titleGetDB()[0]
    # else:
    #     title_before=""
    title_before=titleGetDB()[0].replace(" ","")
    cnt=0
    count=0
    title_update=""
    for index, value in enumerate(announcements):
        temp=value.find_all("td")
        temp_index=str(temp[0].text).replace("\n","")
        if count == 1:
            title_before=titleGetDB()[0].replace(" ","")
        if temp_index not in "공지":
            #print("top:"+temp[0].text)
            title_=str(temp[1].text).replace("\n","").replace("새글","").replace(" ","")
            title=str(temp[1].text).replace("\n","").replace("새글","")
            print("title_crawli"+title_)
            print("title_before"+title_before)
            #sqlite에 저장된 공지(제목)과 크롤링해온 제목 비교하기
            if title_before != title_:
                cnt+=1
                print("cnt"+str(cnt))
                find_link=temp[1].a.attrs["href"]
                link="http://security.swu.ac.kr/"+find_link
                contents=contentExtraction(link)
                #키워드 리스트랑 비교해서 푸쉬알림 보내기
                content=title+contents
                #pushNotification(content,link)
                #print("content"+content)
                if cnt==1:
                    title_update=title
                    print("title_update_cnt"+title_update)
                    # if title_before=="":
                    #     insertDB(title_update,content,link)
                    #     break              
            else: 
                #공지사항이 update됐을 때만 sqlite 수정하기.
                if cnt!=0:
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
    content_text=soup.find("div",{"class":"boardview-content"}).text.replace("\n","")
    return(str(content_text))

def pushNotification(content,link):
    kwList=keywordList()#파이어베이스에서 keyword리스트 가져옴
    print(kwList)
    for i in kwList:
        if(i in content):
            #fb에서 토큰 찾아서 리스트로 만들기
            tkList=tokenList(i)
            print(tkList)
            dept="정보보호학과"
            deptNum=24
            for key, value in tkList:
                #key(=uid)를 검사해서 해당 학과를 구독했는지 알아봐야함.
                check= deptSubscribe(key,deptNum)
                if check==True:
                    notificationList(i,link,key,dept)
                    send_to_firebase_cloud_messaging(dept,i,value,link)


def titleGetDB():
    con=sqlite3.connect('./db.sqlite3')
    cur=con.cursor()
    dept=("security",)
    cur.execute("SELECT title FROM myapp_recent_ann WHERE dept=?",(dept))
    con.commit()
    result=cur.fetchone()
    cur.close()
    con.close()
    return result

def insertDB(title,contents,link):
    con=sqlite3.connect('./db.sqlite3')
    cur=con.cursor()
    query="INSERT INTO myapp_recent_ann(dept, title, content, link) VALUES(?,?,?,?)"
    cur.execute(query,('security',title,contents,link))
    con.commit()
    cur.close()
    con.close()

def updateDB(title):
    con=sqlite3.connect('./db.sqlite3')
    cur=con.cursor()
    cur.execute("UPDATE myapp_recent_ann SET title = ? WHERE dept = ?",(title,'security'))
    con.commit()
    cur.close()
    con.close()