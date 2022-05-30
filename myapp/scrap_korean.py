import requests
from bs4 import BeautifulSoup
from .fb_read import*
from .db_crud import*

dept='korean'
dept_kr='국어국문학과'
deptNum=1
def scraping_korean():
    url="http://korean.swu.ac.kr/bbs/bbs/?bbs_no=5&page_no=1"
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
    # title_before=""
    title_before=titleGetDB(dept)[0].replace(" ","")
    cnt=0
    count=0
    title_update=""
    for index, value in enumerate(announcements):
        temp=value.find_all("td")
        temp_index=str(temp[0].text).replace("\n","")
        if count == 1:
            title_before=titleGetDB(dept)[0].replace(" ","")
        if temp_index not in "공지":
            title_=str(temp[1].text).replace("\n","").replace("N","").replace(" ","")
            title=str(temp[1].text).replace("\n","").replace("N","")
            print("title_crawli"+title_)
            print("title_before"+title_before)
            #sqlite에 저장된 공지(제목)과 크롤링해온 제목 비교하기
            if title_before != title_:
                cnt+=1
                print("cnt"+str(cnt))
                find_link=str(temp[1].a.attrs["value"])
                link="http://korean.swu.ac.kr/bbs/bbs/view.php?bbs_no=5&data_no="+find_link+"&page_no=1&sub_id="
                contents=contentExtraction(link)
                #키워드 리스트랑 비교해서 푸쉬알림 보내기
                content=title+contents
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
    content_text=soup.find("div",{"class":"col-xs-12","style":"padding:100px 20px;"}).text.replace("\n","").replace("&nbsp","")
    return(str(content_text))

