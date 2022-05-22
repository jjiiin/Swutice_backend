# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup

def scraping(request):
    url="https://www.swu.ac.kr/www/noticea.html"
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Accept-Language":"ko-KR,ko"}
    res=requests.get(url,headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    with open("swu.html","w",encoding="utf8")as f:
        f.write(res.text)