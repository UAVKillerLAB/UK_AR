# encoding=utf-8
import pymysql
from django.http import HttpResponse
import json
import webbrowser

url = r'http://127.0.0.1:8000/'
url2 = r'http://127.0.0.1:8000/ajax_list/'


def main(request):
    try:
        conn = pymysql.connect(host="localhost", port=3306, db="UAV_test", user='root', passwd="123456",
                               charset='utf8')
        cs1 = conn.cursor()
        cs1.execute("SELECT longitude, latitude from test where id = (SELECT max(id) FROM test)")
        data_show = cs1.fetchone()
        cs1.execute("SELECT  id, time from test where id = (SELECT max(id) FROM test)")
        data_show2 = list(cs1.fetchone())  ##  transform SQL tuple data to list data
        data_show2[1] = data_show2[1].strftime("%Y-%m-%d %H:%M:%S")  ##  transform datatime to a standard char data
        cs1.close()
        conn.close()
    except Exception as e:
        print(e)
        pass
    data_show = [float(x) for x in data_show]

    data = data_show + data_show2
    jsontemp = json.dumps(data)
    return HttpResponse(jsontemp, content_type='application/json')


webbrowser.open(url)
webbrowser.open(url2)
