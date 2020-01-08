# encoding=utf-8

from django.http import HttpResponse
from django.shortcuts import render
import json
import mysql.connector
# from . import config
import webbrowser

# from DBInfo import *

url = r'http://127.0.0.1:8000/'
url2 = r'http://127.0.0.1:8000/ajax_list/'


def main(request):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT longitude, latitude from test where id = (SELECT max(id) FROM test)")
    data_show = mycursor.fetchone()
    data_show = [float(x) for x in data_show]
    jsontemp = json.dumps(data_show)
    return HttpResponse(jsontemp, content_type='application/json')


# if __name__ == '__main__':
#     main()

webbrowser.open(url)
webbrowser.open(url2)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="LYD618618",
    database="UAV_test"
)
