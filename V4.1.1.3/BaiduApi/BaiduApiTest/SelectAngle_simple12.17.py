# encoding=utf-8
import json
import os
import socket  # 引入套接字
import threading  # 引入并行
import time

import pymysql
import struct
import serial
import matplotlib.pyplot as plt
import datetime
import math
import sys
from geographiclib.geodesic import Geodesic
import configparser
import csv

# import comm_udp_serial

# sys.path.append(r'D:\OneDrive\Python_project\Github\AntiUAV_Python\test')

# from DBInfo import *

plt.ion()  # 开启一个画图的窗口
ax1 = []  # 定义一个 x 轴的空列表用来接收动态的数据
ax2 = []
ach1 = []  # 定义一个 y 轴的空列表用来接收动态的数据
ach2 = []
ach3 = []
ach4 = []

ach = []

count_time = 0
Last_rawdata = 0
Process_data = 0
ch1ch2diff_db_data = []
ch2ch3diff_db_data = []
ch3ch4diff_db_data = []
ch1_db_data = []
ch2_db_data = []
ch3_db_data = []
ch4_db_data = []

angle_db_data = []


def Print4(counnt, ch1_data, ch2_data, ch3_data, ch4_data, angle):
    data = datetime.date.today()
    plt.figure("4 Channel&Matched Angle" + str(data))
    ax2.append(counnt)  # 添加 i 到 x 轴的数据中
    ach1.append(ch1_data)
    ach2.append(ch2_data)
    ach3.append(ch3_data)
    ach4.append(ch4_data)

    ach.append(angle)

    plt.clf()  # 清除之前画的图
    plt.subplot(2, 1, 1)
    plt.plot(ax2, ach1, label="CH1")  # 画出当前 ax 列表和 ay 列表中的值的图形
    plt.plot(ax2, ach2, label="CH2")
    plt.plot(ax2, ach3, label="CH3")
    plt.plot(ax2, ach4, label="CH4")
    plt.title('Channel Data')
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(ax2, ach, label="Matched Angle")
    plt.title('Angle')
    plt.xlabel("Time")
    plt.ylabel("Angle")
    plt.grid(True)
    plt.pause(0.08)  # 暂停一秒
    # plt.ioff()                   # 关闭画图的窗口


def DataProcess(count, angle_now, angle_last):
    if count == 0:
        return angle_now
    else:
        if abs(angle_now - angle_last) >= 20:
            # print("平均")
            # result = (angle1 + angle2) / 2
            if angle_now - angle_last > 0:
                return angle_last + 10
            if angle_now - angle_last < 0:
                return angle_last - 10
        else:
            return angle_now


def Print1(counnt, ch_data):
    ax1.append(counnt)  # 添加 i 到 x 轴的数据中
    ach.append(ch_data)

    plt.clf()  # 清除之前画的图
    plt.subplot(2, 1, 1)
    plt.plot(ax1, ach1)  # 画出当前 ax 列表和 ay 列表中的值的图形
    plt.pause(0.1)


def fetch_data():
    global ch1_db_data
    global ch2_db_data
    global ch3_db_data
    global ch4_db_data

    global angle_db_data
    try:
        conn = pymysql.connect(host=db_host, port=3306, db=db_name, user='root', passwd="123456",
                               charset='utf8')
        cs1 = conn.cursor()
        cs1.execute("select ch1 from final_table")
        result1 = cs1.fetchall()
        cs1.execute("select ch2 from final_table")
        result2 = cs1.fetchall()
        cs1.execute("select ch3 from final_table")
        result3 = cs1.fetchall()
        cs1.execute("select ch4 from final_table")
        result4 = cs1.fetchall()

        cs1.execute("select angle from final_table")
        result5 = cs1.fetchall()
        # print(result1)
        # print(result2)
        # print(result3)
        # print(result4)
        for i in range(len(result5)):
            ch1_db_data.append(float((result1[i])[0]))
            ch2_db_data.append(float((result2[i])[0]))
            ch3_db_data.append(float((result3[i])[0]))
            ch4_db_data.append(float((result4[i])[0]))
            angle_db_data.append(float((result5[i])[0]))
        # print(result1[0])
        conn.commit()
        cs1.close()
        conn.close()
    except Exception as e:
        print(e)
        pass


def SelectAngle(ch1_raw_data, ch2_raw_data, ch3_raw_data, ch4_raw_data):
    """
    :param ch1_raw_data: 通道一数据
    :param ch2_raw_data: 通道二数据
    :param ch3_raw_data: 通道三数据
    :param ch4_raw_data: 通道四数据
    :return: result:查表得到的角度值
    """
    global ch1ch2diff_db_data, ch2ch3diff_db_data, ch3ch4diff_db_data, ch4_db_data, count_time, Last_rawdata, Process_data
    # 归一化
    min_ch_data = min(ch1_raw_data, ch2_raw_data, ch3_raw_data, ch4_raw_data)
    min_ch_data = float(min_ch_data)
    ch1_data = float(ch1_raw_data) / min_ch_data
    ch2_data = float(ch2_raw_data) / min_ch_data
    ch3_data = float(ch3_raw_data) / min_ch_data
    ch4_data = float(ch4_raw_data) / min_ch_data
    if ch1_data + ch2_data + ch3_data + ch4_data <= 4:
        print("数据可能有误！\n数据可能有误！\n数据可能有误！\n数据可能有误！\n数据可能有误！")

    ch1_data = float(ch1_data)
    ch2_data = float(ch2_data)
    ch3_data = float(ch3_data)
    ch4_data = float(ch4_data)
    sum_difference = []

    print("len(angle_db_data):",len(angle_db_data))
    for i in range(len(angle_db_data)):
        ch1ch2_difference = (20 * math.log((ch1_db_data[i] / ch2_db_data[i]), 10) - 20 * math.log((ch1_data / ch2_data),
                                                                                                  10)) ** 2  # 差值放大
        ch2ch3_difference = (20 * math.log((ch2_db_data[i] / ch3_db_data[i]), 10) - 20 * math.log((ch2_data / ch3_data),
                                                                                                  10)) ** 2  # 差值放大
        ch3ch4_difference = (20 * math.log((ch3_db_data[i] / ch4_db_data[i]), 10) - 20 * math.log((ch3_data / ch4_data),
                                                                                                  10)) ** 2  # 差值放大
        sum_difference.append(ch1ch2_difference + ch2ch3_difference + ch3ch4_difference)
    # print(sum_difference)
    # print(min(sum_difference))
    # print(sum_difference.index(min(sum_difference)))
    # return sum_difference.index(min(sum_difference))

    global count_time
    global Last_rawdata
    global Process_data
    Last_rawdata = Process_data
    Process_data = sum_difference.index(min(sum_difference))
    Process_data=angle_db_data[Process_data]
    result = DataProcess(count_time, Process_data, Last_rawdata)

    count_time += 1

    return result


def init():
    global ser, usb_data_len, udp_socket, usb_com, db_host, db_name, db_pwd, db_user, db_port, pc_host, pc_port, s10_correction_angle, s8_correction_angle, station10_latitude, station10_longitude, station8_latitude, station8_longitude
    print("读取config.json......")
    # Reading data from file
    with open("config.json", 'r') as f:
        config_json_data = json.load(f)
        db_host = config_json_data["db_host"]
        print("数据库IP地址：", db_host)
        db_name = config_json_data["db_name"]
        print("数据库名：", db_name)
        db_pwd = str(config_json_data["db_password"])
        db_user = config_json_data["db_user"]
        db_port = config_json_data["db_port"]
        usb_com = config_json_data["com"]
        print("COM：", usb_com)
        station10_latitude = config_json_data["station10_latitude"]
        station10_longitude = config_json_data["station10_longitude"]
        print("主站经纬度：({},{})".format(station10_latitude,station10_longitude))
        station8_latitude = config_json_data["station8_latitude"]
        station8_longitude = config_json_data["station8_longitude"]
        print("一站经纬度：({},{})".format(station8_latitude,station8_longitude))
        s10_correction_angle = config_json_data["s10_correction_angle"]
        print("主站0°方位角：" + str(s10_correction_angle))
        s8_correction_angle = config_json_data["s8_correction_angle"]
        print("一站0°方位角：" + str(s8_correction_angle))
        print("\n读取成功！\n")
    create_csv()
    ser = serial.Serial(usb_com, 115200)
    ser.close()
    ser.open()
    usb_data_len = 66
    pc_port = 10001
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建套接字
    udp_socket.bind(("", pc_port))  # 服务器绑定ip和端口
    # 问题描述：套接字必须发送一次才能接收
    udp_socket.sendto("1".encode("utf-8"), ('192.168.3.100', 8080))


def create_csv():
    global csv_name
    if os.path.exists("location_info"):
        pass
    else:
        os.mkdir("location_info")
    os.chdir("location_info")
    temp = time.strftime("%Y%m%d%H%M")
    csv_name = temp + ".csv"
    with open(csv_name, 'w', newline='') as f:
        csv_write = csv.writer(f)
        csv_head = ["time", "latitude", "longitude"]
        csv_write.writerow(csv_head)
        print("创建成功！")

	
def write_csv(time, latitude, longitude):
    with open(csv_name, 'a+', newline='') as f:
        csv_write = csv.writer(f)
        data_row = [time, latitude, longitude]
        csv_write.writerow(data_row)


def positioning(station10_angle, station8_angle, station10_correction, station8_correction, station10_latitude,
                station10_longitude):
    """
    :param station10_angle: 主站方位角
    :param station8_angle: 主站修正角
    :param station10_correction: 一站方位角
    :param station8_correction: 一站修正角
    :param station10_latitude: 主站纬度
    :param station10_longitude: 主站经度
    :return:none
    """
    """
    修正角为地理学上的方位角。
    定义:从标准方向的北端起,顺时针方向到直线的水平角称为该直线的方位角。方位角的取值范围为0°～360°。

    一定要区别于方向角。
    定义:方向角指的是采用某坐标轴方向作为标准方向所确定的方位角。有时，方向角是从正北或正南方向到目标方向所形成的小于九十度的角。
    """
    global station8_latitude, station8_longitude
    station10_latitude = float(station10_latitude)
    station10_longitude = float(station10_longitude)
    station10_correction = int(station10_correction)
    # direction_Zh = ["东偏南", "南偏西", "西偏北", "北偏东"]
    direction_Zh = ["北偏东", "东偏南", "南偏西", "西偏北"]
    """
    DISTANCE_S10_S8, ANGLE_A, ANGLE_B需要确定
    """
    # DISTANCE_S10_S8 = 398
    # ANGLE_A = 69
    # ANGLE_B = 21
    # DISTANCE_S10_S8 = Geodesic.WGS84.Inverse(station10_latitude, station10_longitude, station8_latitude, station8_longitude)["s12"]
    DISTANCE_S10_S8 = 35.2
    ANGLE_A = 25
    ANGLE_B = 65
    # 一顿计算
    """
    两站与目标构成的三角形的内角
    angle_alpha:alpha为主站角
    angle_beta:beta为一站角
    """
    # angle_alpha = math.radians(station10_correction - 180 + station10_angle - ANGLE_A)
    # angle_beta = math.radians(station8_correction - 90 + station8_angle - ANGLE_B)
    # print(180 - station10_angle - ANGLE_A, station8_angle - ANGLE_B)
    angle_alpha = math.radians(180 - station10_angle)
    angle_beta = math.radians(station8_angle)
    distance_s10_target = (math.sin(angle_beta) * DISTANCE_S10_S8) / (math.sin(math.pi - angle_alpha - angle_beta))
    distance_s8_target = (math.sin(angle_alpha) * DISTANCE_S10_S8) / (math.sin(math.pi - angle_alpha - angle_beta))
    # return distance_s10_target, distance_s8_target
    # 获取每一经度间的距离（单位：米）
    longitude_distance = (Geodesic.WGS84.Inverse(station10_latitude, 104.00001, station10_latitude, 104.00002)[
        "s12"]) * 100000
    # print("longitude_distance", longitude_distance)
    LATITUDE_DISTANCE = 110946.304

    # 统一极坐标系
    azimuth = (station10_angle + station10_correction) % 360
    print(azimuth)
    # 通过方位角判断方向
    if 0 < azimuth <= 90:
        direction_flag = 0
        target_direction = azimuth
    elif 90 < azimuth <= 180:
        direction_flag = 1
        target_direction = azimuth - 90
    elif 180 < azimuth <= 270:
        direction_flag = 2
        target_direction = azimuth - 180
    elif 270 < azimuth <= 360:
        direction_flag = 3
        target_direction = azimuth - 270

    # 北偏东
    if direction_flag == 0:
        # 计算纬度方向和经度方向的长度改变量
        latitude_change_distance = distance_s10_target * math.cos(math.radians(target_direction))
        longitude_change_distance = distance_s10_target * math.sin(math.radians(target_direction))
        # 计算目标纬度和经度
        s10_target_latitude = station10_latitude + latitude_change_distance / longitude_distance
        s10_target_longitude = station10_longitude + longitude_change_distance / LATITUDE_DISTANCE
    # 东偏南
    elif direction_flag == 1:
        # 计算纬度方向和经度方向的长度改变量
        latitude_change_distance = distance_s10_target * math.sin(math.radians(target_direction))
        longitude_change_distance = distance_s10_target * math.cos(math.radians(target_direction))
        # 计算目标纬度和经度
        s10_target_latitude = station10_latitude - latitude_change_distance / longitude_distance
        s10_target_longitude = station10_longitude + longitude_change_distance / LATITUDE_DISTANCE
    # 南偏西
    elif direction_flag == 2:
        # 计算纬度方向和经度方向的长度改变量
        latitude_change_distance = distance_s10_target * math.cos(math.radians(target_direction))
        longitude_change_distance = distance_s10_target * math.sin(math.radians(target_direction))
        # 计算目标纬度和经度
        s10_target_latitude = station10_latitude - latitude_change_distance / longitude_distance
        s10_target_longitude = station10_longitude - longitude_change_distance / LATITUDE_DISTANCE
    # 西偏北
    elif direction_flag == 3:
        # 计算纬度方向和经度方向的长度改变量
        latitude_change_distance = distance_s10_target * math.sin(math.radians(target_direction))
        longitude_change_distance = distance_s10_target * math.cos(math.radians(target_direction))
        # 计算目标纬度和经度
        s10_target_latitude = station10_latitude + latitude_change_distance / longitude_distance
        s10_target_longitude = station10_longitude - longitude_change_distance / LATITUDE_DISTANCE

    print("获取主站角度{}°\n目标在主站 {}{}° 方向，距离 {} 米".format(station10_angle, direction_Zh[direction_flag],
                                                     target_direction,
                                                     distance_s10_target))
    # 统一极坐标系
    azimuth = (station8_angle + station8_correction) % 360
    # print(azimuth)
    # 通过方位角判断方向
    if 0 < azimuth <= 90:
        direction_flag = 0
        target_direction = azimuth
    elif 90 < azimuth <= 180:
        direction_flag = 1
        target_direction = azimuth - 90
    elif 180 < azimuth <= 270:
        direction_flag = 2
        target_direction = azimuth - 180
    elif 270 < azimuth <= 360:
        direction_flag = 3
        target_direction = azimuth - 270

    # 北偏东
    if direction_flag == 0:
        # 计算纬度方向和经度方向的长度改变量
        latitude_change_distance = distance_s8_target * math.cos(math.radians(target_direction))
        longitude_change_distance = distance_s8_target * math.sin(math.radians(target_direction))
        # 计算目标纬度和经度
        s8_target_latitude = station8_latitude + latitude_change_distance / longitude_distance
        s8_target_longitude = station8_longitude + longitude_change_distance / LATITUDE_DISTANCE
    # 东偏南
    elif direction_flag == 1:
        # 计算纬度方向和经度方向的长度改变量
        latitude_change_distance = distance_s8_target * math.sin(math.radians(target_direction))
        longitude_change_distance = distance_s8_target * math.cos(math.radians(target_direction))
        # 计算目标纬度和经度
        s8_target_latitude = station8_latitude - latitude_change_distance / longitude_distance
        s8_target_longitude = station8_longitude + longitude_change_distance / LATITUDE_DISTANCE
    # 南偏西
    elif direction_flag == 2:
        # 计算纬度方向和经度方向的长度改变量
        latitude_change_distance = distance_s8_target * math.cos(math.radians(target_direction))
        longitude_change_distance = distance_s8_target * math.sin(math.radians(target_direction))
        # 计算目标纬度和经度
        s8_target_latitude = station8_latitude - latitude_change_distance / longitude_distance
        s8_target_longitude = station8_longitude - longitude_change_distance / LATITUDE_DISTANCE
    # 西偏北
    elif direction_flag == 3:
        # 计算纬度方向和经度方向的长度改变量
        latitude_change_distance = distance_s8_target * math.sin(math.radians(target_direction))
        longitude_change_distance = distance_s8_target * math.cos(math.radians(target_direction))
        # 计算目标纬度和经度
        s8_target_latitude = station8_latitude + latitude_change_distance / longitude_distance
        s8_target_longitude = station8_longitude - longitude_change_distance / LATITUDE_DISTANCE
    print("获取一站角度{}°\n目标在一站 {}{}° 方向，距离 {} 米".format(station8_angle, direction_Zh[direction_flag], target_direction,
                                                     distance_s8_target))

    target_latitude = (s10_target_latitude + s8_target_latitude) / 2
    target_longitude = (s10_target_longitude + s8_target_longitude) / 2
    print("目标WGS84坐标({},{})".format(target_latitude, target_longitude))
    temp = time.strftime("%H%M%S")
    write_csv(temp, target_latitude, target_longitude)
    return target_latitude, target_longitude


def USB_recv(ser, usb_data_len):
    # 解析数据
    USB_recv_data = ((ser.read(usb_data_len)).decode('ASCII')).replace("\r\n", "")
    USB_recv_data = bytes(USB_recv_data, encoding="utf8")
    data = [int(("0x" + (USB_recv_data[0: 16].decode())), 16), int(("0x" + (USB_recv_data[16: 32].decode())), 16),
            int(("0x" + (USB_recv_data[32: 48].decode())), 16), int(("0x" + (USB_recv_data[48: 64].decode())), 16)]
    return data


def udp_send_ersuo(udp_socket, BetaAngle):
    mhesIPAddr = '192.168.3.70'  # 民航二所IP
    mhesPort = 10002  # 民航二所Port

    send_data_head = 0xb3b3
    send_data_headlen = 34
    send_data_latitude = 103 + (45 / 60) / 100 + (20 / 3600) / 10000
    send_data_longitude = 31 + (7 / 60) / 100 + (2 / 3600) / 10000
    send_data_height = 790
    send_data_tarqua = 1
    send_data_end = 0xb1af
    send_data_tracknum = 1
    send_data_trackdis = 0
    send_data_bata = BetaAngle
    send_data_alpha = 0
    send_data_trackrate = 0
    send_data = struct.pack('<HHdddIHiffff', send_data_head, send_data_headlen, send_data_latitude,
                            send_data_longitude, send_data_height, send_data_tarqua, send_data_end,
                            send_data_tracknum, send_data_trackdis, send_data_bata, send_data_alpha,
                            send_data_trackrate)

    print(len(send_data))
    # input('enter')
    # send_data = send_data.encode('utf-8') #这行代码需要测试 一达测试版本中没有这一行
    udp_socket.sendto(send_data, (mhesIPAddr, mhesPort))  # sendto（发送数据，发送地址）
    # udp_socket.close()


def udp_recv(udp_socket):
    receive_message, client = udp_socket.recvfrom(4096)
    # data = struct.unpack('<4q', receive_message)  # 调用struct库解包，>4q代表4个long long 大端对齐<4q代表4个long long 小端对齐
    data = struct.unpack('<HHdddIHiffff', receive_message)  # 调用struct库解包，>4q代表4个long long 大端对齐<4q代表4个long long 小端对齐
    warning = "板子是小端，网络调试助手是大端！！！"
    return data[9]


def main():
    # get_info()
    init()
    input("Press any key to start.......")
    print("Waiting for data......")
    fetch_data()
    global count
    count = 0
    while True:
        count += 1
        decoded_data = USB_recv(ser, usb_data_len)
        print("Raw_CH1_data:{:.15f}\nRaw_CH2_data:{:.15f}\nRaw_CH3_data:{:.15f}\nRaw_CH4_data:{:.15f}".format(
            decoded_data[0], decoded_data[1], decoded_data[2], decoded_data[3]))
        s10_matched_angle = SelectAngle(decoded_data[0], decoded_data[1], decoded_data[2], decoded_data[3])
        print('s10_matched_angle:', s10_matched_angle)
        # # 求平均，平滑数据
        # matched_angle_buff = []
        # matched_angle_buff.append(s10_matched_angle)
        # if len(matched_angle_buff) >= 5:
        #     matched_angle_mid = sum(matched_angle_buff) / (len(matched_angle_buff) * 1.0)
        #     matched_angle_buff = []  # 覆盖为一个没有元素的列表
        """
        udp发送函数
        """
        # udp_send_ersuo(udp_socket, matched_angle_mid)
        Print4(count, decoded_data[0], decoded_data[1], decoded_data[2], decoded_data[3], s10_matched_angle)
        print("当前角度为:{}".format(s10_matched_angle))
        """
        解算函数
        """
        s8_matched_angle = udp_recv(udp_socket)
        positioning(s10_matched_angle, s8_matched_angle, s10_correction_angle, s8_correction_angle, station10_latitude,
                    station10_longitude)
        print("\n\n")


if __name__ == '__main__':
    main()
