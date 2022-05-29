from calendar import c
import pyrebase
import firebase_admin
import json
from firebase_admin import credentials
from firebase_admin import db
from collections import OrderedDict
from datetime import datetime

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
# cred = credentials.Certificate('./serviceAccountKey.json')
# firebase=firebase_admin.initialize_app(cred,{
#     'databaseURL': 'https://swprojectapp-default-rtdb.firebaseio.com'
# })

db=firebase.database()
auth=firebase.auth()

def keywordList():
    keyword=db.child('keyword').get()
    kwList=[]
    #print(keyword.val())#OrderedDict([('-N2e-1UHxGapWtFUs_0i', '계절'), ('-N2e-7i8dWKJYDqaberz', '방학')])
    for key, val in keyword.val().items():
        kwList.append(val)
    return kwList

def tokenList(keyword):
    token=db.child('keyword_subscribe').child(keyword).get()
    tokenList=[]
    print(token.val().items())
    for key, val in token.val().items():
        tokenList.append(val)
    return token.val().items()


def notificationList(keyword, link, uid, dept):
    body=f'\"{keyword}\"키워드가 포함된 공지사항이 등록됐습니다.'
    current_time = datetime.now()
    date={'year':current_time.year, 'month': current_time.month, 'day':current_time.day, 'hour':current_time.hour, 'minute':current_time.minute, 'second':current_time.second,}
    db.child('users').child(uid).child(
        'notification').push({'dept':dept, 'body':body, 'date':date, 'link':link,})

def deptSubscribe(uid, deptNum):
    for i in range(1,4):
        major_="major"+str(i)
        sub_major=db.child('users').child(uid).child(major_).get()
        if sub_major.val()==deptNum:
            return True
    else:
        return False

