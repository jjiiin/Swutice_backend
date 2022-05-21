from django.shortcuts import render
from django.http import HttpResponse
import pyrebase

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

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

firebase =pyrebase.initialize_app(firebaseConfig)

db=firebase.database()
auth=firebase.auth()


def scrap(request):
    url="https://www.swu.ac.kr/index.do"
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Accept-Language":"ko-KR,ko"}
    res=requests.get(url,headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    with open("swu.html","w",encoding="utf8")as f:
        f.write(res.text)
    
    db.child("name").push({"company":"google"})
    
    
    return HttpResponse('hello myapp!')