from django.http import HttpResponse
from django.shortcuts import render
import json
import serial
import time
import csv
import pandas as pd
from time import sleep
from django.shortcuts import render_to_response


def hello(request):
    context = {}
    context['hello'] = 'Hello World!'

    file_adress = r'G:\Program Files (x86)\ArcGIS\GPS_test_output.csv'  # 读取文件
    data = pd.read_csv(file_adress)

    # print(data)
    lon = data.iloc[:, 9] / 100  # 读取经度
    lat = data.iloc[:, 7] / 100  # 读取纬度

    count = 0
    count_buf = []
    data_show = []
    gpstime = time.strftime('%H:%M:%S', time.localtime(time.time()))  # 显示当前时间

    for count in range(len(lon)):  # 显示次数
        count_buf.append(count)

    print(lon)
    print(lat)
    print(count_buf)

    data_show.append(lon[0])  # 写入经度
    data_show.append(lat[0])  # 写入纬度
    data_show.append(count_buf[0])  # 往data_show里存入数据
    data_show.append(gpstime)

    list_show = {}
    list_show['data_show'] = data_show
    return render(request, 'hello.html', list_show)
