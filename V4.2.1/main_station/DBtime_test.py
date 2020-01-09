from django.http import HttpResponse
from django.shortcuts import render
import json
import mysql.connector
# from . import config
import webbrowser
import time

import datetime
import json


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="LYD618618",
    database="UAV_test"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT longitude, latitude from test where id = (SELECT max(id) FROM test)")

data_show = mycursor.fetchone()

mycursor.execute("SELECT  id, time from test where id = (SELECT max(id) FROM test)")
data_show2 = list(mycursor.fetchone())
# data_show2[1]= time.strftime('%Y-%m-%d %H:%M',data_show2[1])
mydb.commit()
data_show = [float(x) for x in data_show]

print(data_show)
print(data_show2)

print(data_show2[1])

data_show2[1]= data_show2[1].strftime("%Y-%m-%d %H:%M:%S")
data=data_show + data_show2

print(data)

# print(json.dumps(data,cls=DateEncoder))
jsontemp = json.dumps(data)

print(jsontemp)