# Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from django.db import connections
import sqlite3
from .fb_read import*

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
    kwList=keywordList()
    #print(kwList)['계절', '방학']
    title_before_tmp=titleGetDB()
    title_before=title_before_tmp[0]
    print(title_before)
    for index, value in enumerate(announcements):
        temp=value.find_all("td")
        temp_index=str(temp[0].text).replace("\n","")
        #print(temp_index)
        if temp_index not in "TOP":
            #print("top:"+temp[0].text)
            id=str(temp[0].text).replace("\n","")
            title=str(temp[1].text).replace("\n","").replace("새글","")
            #sqlite에 저장된 공지(제목)과 크롤링해온 제목 비교하기
            title_before=titleGetDB()
            print(title)
            # if(title_before!=title):
            #     find_link=temp[1].a.attrs["onclick"].split("'")
            #     frag_link=str(find_link[3])
            #     link="http://www.swu.ac.kr/front/boardview.do?&pkid=" + frag_link +"&currentPage=1&menuGubun=1&siteGubun=1&bbsConfigFK=4&searchField=ALL&searchValue=&searchLowItem=ALL"
            #     contents=contentExtraction(link)
            #     updateDB(title,contents,link)
                #fb-keyword목록과 비교하기

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

def updateDB(title,contents,link):
    con=sqlite3.connect('./db.sqlite3')
    cur=con.cursor()
    query="INSERT INTO myapp_recent_ann (content,title,dept,link) VALUES(?,?,?,?)"
    cur.execute(query,(contents,title,"main_1",link))
    con.commit()
    cur.close()
    con.close()