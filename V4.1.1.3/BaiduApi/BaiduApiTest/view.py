from django.http import HttpResponse
from django.shortcuts import render
import json
import serial
import time
import csv
import pandas as pd
from time import sleep
from django.shortcuts import render_to_response

count = 0
lon = []
lat = []


#
# def baidu_testline(request):
#     # file_adress = r'G:\Program Files (x86)\ArcGIS\GPS_test_output.csv'  # 读取文件
#     # data = pd.read_csv(file_adress)
#     # # print(data)
#     #
#     # lon = data.iloc[:, 9] / 100  # 读取经度
#     # lat = data.iloc[:, 7] / 100  # 读取纬度
#     # global count
#     #
#     #
#     # count_buf=[]
#
#     # gpstime=time.strftime('%H:%M:%S',time.localtime(time.time()))           #显示当前时间
#     #
#     # count=count+1
#     #
#     # # if count==len(lon):
#     # if count==26:
#     #     count=0
#     #
#     # for count in range(len(lon)):                                           #显示次数
#     #     count_buf.append(count)
#
#     global count
#     data_show = []
#     print(lon)
#     print(lat)
#     print(count)
#
#     count = count + 1
#
#     if count == len(lon):
#         count = 0
#
#     data_show.append(lon[count]+0.001)                                                 #写入经度
#     data_show.append(lat[count]+0.001)                                                 #写入纬度
#     data_show.append(count)                                          #往data_show里存入数据
#     data_show.append(gpstime)
#
#
#     with open('./rec_gps.csv', 'a', newline='') as csvFile1:
#         writer = csv.writer(csvFile1)
#         writer.writerow((count, gpstime, lon[count], lat[count]))
#         csvFile1.close()
#
#     return HttpResponse(json.dumps(data_show), content_type='application/json')
#     # return render(request, 'index.html', data_show)         #返回一行的数据显示在地图上


def index(request):
    return render_to_response('index.html')

# file_adress = r'G:\Program Files (x86)\ArcGIS\GPS_test_output.csv'  # 读取文件
# data = pd.read_csv(file_adress)
# # print(data)
#
# lon = data.iloc[:, 9] / 100  # 读取经度
# lat = data.iloc[:, 7] / 100  # 读取纬度
#
#
# data_show=[]
# gpstime=time.strftime('%H:%M:%S',time.localtime(time.time()))           #显示当前时间
