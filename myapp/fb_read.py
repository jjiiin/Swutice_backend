import pyrebase
import firebase_admin
import json
from firebase_admin import credentials
from firebase_admin import db
from collections import OrderedDict

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
