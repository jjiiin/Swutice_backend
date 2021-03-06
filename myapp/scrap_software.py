from types import NoneType
import requests
from bs4 import BeautifulSoup
from .fb_read import *
from .db_crud import *

dept='software'
dept_kr='소프트웨어융합학과'
deptNum=25
def scraping_software():
    url="http://swuswc.cafe24.com/%ea%b3%b5%ec%a7%80%ec%82%ac%ed%95%ad/%ED%95%99%EA%B3%BC-%EA%B3%B5%EC%A7%80%EC%82%AC%ED%95%AD/?pageid=1"
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Accept-Language":"ko-KR,ko"}
    res=requests.get(url,headers=headers)
    res.raise_for_status()
    soup=BeautifulSoup(res.text,'html.parser',from_encoding="utf-8")
    tbody=soup.find("tbody")
    announcements=tbody.find_all("tr")
    #title_before=""
    title_before=titleGetDB(dept)[0].replace(" ","")
    cnt=0
    count=0
    title_update=""
    for index, value in enumerate(announcements):
        temp=value.find_all("td")
        if count == 1:
            title_before=titleGetDB(dept)[0].replace(" ","")
        title_=str(temp[1].text).replace("\n","").replace("N","").replace(" ","")
        title=str(temp[1].text).replace("\n","").replace("N","")
        print("title_crawli"+title_)
        print("title_before"+title_before)
            #sqlite에 저장된 공지(제목)과 크롤링해온 제목 비교하기
        if title_before != title_:
            cnt+=1
            print("cnt"+str(cnt))
            find_link=str(temp[1].a.attrs["href"])
            link="http://swuswc.cafe24.com/"+find_link
            contents=contentExtraction(link)
                #키워드 리스트랑 비교해서 푸쉬알림 보내기
            content=title+contents
            print(link)
            print(contents)
            pushNotification(content,link,dept_kr,deptNum)
            if cnt==1:
                title_update=title
                print("title_update_cnt"+title_update)
                # if title_before=="":
                #     insertDB(title_update,content,link,dept)
                #     break              
        else: 
            #공지사항이 update됐을 때만 sqlite 수정하기.
            if cnt!=0:
                print("title_update"+title_update)
                updateDB(title_update,dept)
                count+=1
            break
    

def contentExtraction(link):
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Accept-Language":"ko-KR,ko"}
    res=requests.get(link,headers=headers)
    res.raise_for_status()
    soup=BeautifulSoup(res.text,'html.parser',from_encoding="utf-8")
    result=""
    try:
        content_text=soup.find("div",{"class":"box_bd_view"}).text.replace("\n","")
        return(str(content_text))  
    except Exception as e:
        print(str(e))
        return result 