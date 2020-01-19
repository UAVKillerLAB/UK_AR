# encoding=utf-8

import json
import socket # 引入套接字
import threading  # 引入并行
import time
from numpy import mean
import pymysql
import struct
import serial
import matplotlib.pyplot as plt
import datetime
import math
from geographiclib.geodesic import Geodesic


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

matched_angle_buff = []
s10_matched_angle = 0

angle_db_data = []
angle_buffer = [math.pi / 4, math.pi / 4, 0, 0]
recv_mess = []
run_flag = 0


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
    plt.legend(loc='upper left')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(ax2, ach, label="Matched Angle")
    plt.title('Angle')
    plt.xlabel("Time")
    plt.ylabel("Angle")
    plt.grid(True)
    plt.pause(0.08) # 暂停一秒
    # plt.ioff()    # 关闭画图的窗口


def DataProcess(count, angle_now, angle_last):
    if count == 0:
        return angle_now
    else:
        if abs(angle_now - angle_last) >= 20:
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
        conn = pymysql.connect(host=db_host, port=db_port, db=db_name, user=db_user, passwd=db_pwd,
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

    print("len(angle_db_data):", len(angle_db_data))
    for i in range(len(angle_db_data)):
        ch1ch2_difference = (20 * math.log((ch1_db_data[i] / ch2_db_data[i]), 10) - 20 * math.log((ch1_data / ch2_data),
                                                                                                  10)) ** 2  # 差值放大
        ch2ch3_difference = (20 * math.log((ch2_db_data[i] / ch3_db_data[i]), 10) - 20 * math.log((ch2_data / ch3_data),
                                                                                                  10)) ** 2  # 差值放大
        ch3ch4_difference = (20 * math.log((ch3_db_data[i] / ch4_db_data[i]), 10) - 20 * math.log((ch3_data / ch4_data),
                                                                                                  10)) ** 2  # 差值放大
        sum_difference.append(ch1ch2_difference + ch2ch3_difference + ch3ch4_difference)

    global count_time
    global Last_rawdata
    global Process_data
    Last_rawdata = Process_data
    Process_data = sum_difference.index(min(sum_difference))
    Process_data = angle_db_data[Process_data]
    result = DataProcess(count_time, Process_data, Last_rawdata)

    count_time += 1

    return result


def init():
    global ser, usb_data_len, udp_socket, usb_com, db_host, db_name, db_pwd, db_user, db_port, pc_host, pc_port, \
        s10_correction_angle, s8_correction_angle, station10_latitude, station10_longitude, station8_latitude, \
        station8_longitude, baseline_angle, DISTANCE_S10_S8
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
        print("主站经纬度：({},{})".format(station10_latitude, station10_longitude))

        station8_latitude = config_json_data["station8_latitude"]
        station8_longitude = config_json_data["station8_longitude"]
        print("一站经纬度：({},{})".format(station8_latitude, station8_longitude))

        s10_correction_angle = config_json_data["s10_correction_angle"]
        print("主站0°方位角：" + str(s10_correction_angle))
        s8_correction_angle = config_json_data["s8_correction_angle"]
        print("一站0°方位角：" + str(s8_correction_angle))
        DISTANCE_S10_S8 = config_json_data["DISTANCE_S10_S8"]
        print("两站水平距离差：" + str(DISTANCE_S10_S8))
        print("\n读取成功！\n")
    ser = serial.Serial(usb_com, 115200)
    ser.close()
    ser.open()
    usb_data_len = 66
    pc_port = 10002
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建套接字
    udp_socket.bind(("", pc_port))  # 服务器绑定ip和端口
    # 问题描述：套接字必须发送一次才能接收
    udp_socket.sendto("1".encode("utf-8"), ('192.168.3.100', 8080))
    baseline_angle = math.degrees(math.atan(abs(station10_longitude - station8_longitude)
                                            / abs(station10_latitude - station8_latitude)))
    print("基准线方位角：" + str(baseline_angle))


def positioning(station10_angle, station8_angle, station10_correction, station8_correction, station10_latitude,
                station10_longitude, station8_latitude, station8_longitude, baseline_angle, DISTANCE_S10_S8):
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
    station10_latitude = float(station10_latitude)
    station10_longitude = float(station10_longitude)
    station10_correction = int(station10_correction)
    direction_Zh = ["北偏东", "东偏南", "南偏西", "西偏北"]
    """
    两站与目标构成的三角形的内角
    angle_alpha:alpha为主站角
    angle_beta:beta为一站角
    """
    angle_alpha = math.radians(180 - (station10_angle + s10_correction_angle - baseline_angle))
    angle_beta = math.radians(station8_angle + s8_correction_angle - baseline_angle)

    # 剔除异常值
    angle_buffer[2] = angle_alpha
    angle_buffer[3] = angle_beta
    if angle_alpha + angle_beta >= math.pi:
        # 输出上一个值
        angle_alpha = angle_buffer[0]
        angle_beta = angle_buffer[1]
    angle_buffer[0] = angle_alpha
    angle_buffer[1] = angle_beta

    distance_s10_target = (math.sin(angle_beta) * DISTANCE_S10_S8) / (math.sin(math.pi - angle_alpha - angle_beta))
    distance_s8_target = (math.sin(angle_alpha) * DISTANCE_S10_S8) / (math.sin(math.pi - angle_alpha - angle_beta))
    # 获取每一经度间的距离（单位：米）
    longitude_distance = (Geodesic.WGS84.Inverse(station10_latitude, 104.00001, station10_latitude, 104.00002)[
        "s12"]) * 100000
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
    return target_latitude, target_longitude, station10_angle, distance_s10_target, station8_angle, distance_s8_target


def USB_recv(ser, usb_data_len):
    # 解析数据
    USB_recv_data = ((ser.read(usb_data_len)).decode('ASCII')).replace("\r\n", "")
    USB_recv_data = bytes(USB_recv_data, encoding="utf8")
    data = [int(("0x" + (USB_recv_data[0: 16].decode())), 16), int(("0x" + (USB_recv_data[16: 32].decode())), 16),
            int(("0x" + (USB_recv_data[32: 48].decode())), 16), int(("0x" + (USB_recv_data[48: 64].decode())), 16)]
    return data


def udp_recv(udp_socket):
    global recv_mess
    while True:
        receive_message, client = udp_socket.recvfrom(4096)
        # data = struct.unpack('<4q', receive_message)  # 调用struct库解包，>4q代表4个long long 大端对齐<4q代表4个long long 小端对齐
        data = struct.unpack('<HHdddIHidddd', receive_message)  # 调用struct库解包，>4q代表4个long long 大端对齐<4q代表4个long long 小端对齐
        recv_mess = data[9], data[10]
    # return data[9]


def read_time():
    nts = [0, 0]
    global run_flag
    while True:
        # 获取当前时间
        nts[1] = time.time()
        # 如果秒钟突变
        if (nts[1] - nts[0]) >= 0.2:
            run_flag = 1
            # print(nts)
            nts[0] = nts[1]
        # 延时30ms
        time.sleep(0.03)


def main():
    init()
    input("Press any key to start.......")
    print("Waiting for data......")
    fetch_data()
    global count
    global run_flag
    global matched_angle_buff
    global s10_matched_angle
    global recv_mess
    count = 0
    size = 11
    process_buff = []
    t = threading.Thread(target=udp_recv, args=(udp_socket,))
    t1 = threading.Thread(target=read_time)
    t.start()
    t1.start()

    while True:
        if run_flag == 1:
            run_flag = 0
            count += 1
            decoded_data = USB_recv(ser, usb_data_len)
            print("Raw_CH1_data:{:.15f}\nRaw_CH2_data:{:.15f}\nRaw_CH3_data:{:.15f}\nRaw_CH4_data:{:.15f}".format(
                decoded_data[0], decoded_data[1], decoded_data[2], decoded_data[3]))
            s10_matched_angle = SelectAngle(decoded_data[0], decoded_data[1], decoded_data[2], decoded_data[3])

            process_buff.append(s10_matched_angle)

            if len(process_buff) >= size:
                buff_mean = mean(process_buff)

                loss = abs(s10_matched_angle - buff_mean)

                if loss > 10:
                    #                         print('++++++++\n++++++++\n')

                    if s10_matched_angle - mean(process_buff) < 0:
                        process_buff.pop()

                        process_buff.append(process_buff[-1] - 1)

                    if s10_matched_angle - mean(process_buff) > 0:
                        process_buff.pop()

                        process_buff.append(process_buff[-1] + 1)
                print(process_buff)
                process_buff.pop(0)

            s10_matched_angle = process_buff[-1]

            print('s10_matched_angle:', s10_matched_angle)
            # # 求平均，平滑数据
            # matched_angle_buff = []
            matched_angle_buff.append(s10_matched_angle)

            # test_count=test_count+1
            # if len(matched_angle_buff) >= 5:
            #     matched_angle_mid = sum(matched_angle_buff) / (len(matched_angle_buff) * 1.0)
            #     matched_angle_buff = []  # 覆盖为一个没有元素的列表
            #     test_count=0

            # print('test_count',test_count)

            Print4(count, decoded_data[0], decoded_data[1], decoded_data[2], decoded_data[3], s10_matched_angle)
            print("当前角度为:{}".format(s10_matched_angle))
            """
            解算函数
            """
            s8_matched_angle = recv_mess[0]
            time10 = time.time()
            save = positioning(s10_matched_angle, s8_matched_angle, s10_correction_angle, s8_correction_angle,
                               station10_latitude, station10_longitude, station8_latitude, station8_longitude,
                               baseline_angle, DISTANCE_S10_S8)
            print("\n\n")
            try:
                conn = pymysql.connect(host=db_host, port=db_port, db=db_name, user=db_user, passwd=db_pwd,
                                       charset='utf8')
                cs1 = conn.cursor()
                sql = "INSERT INTO test (latitude, longitude, angle10, distance10, angle8, distance8, time10, time8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (save[0], save[1], save[2], save[3], save[4], save[5], time10, recv_mess[1])
                cs1.execute(sql, val)
                conn.commit()
                cs1.close()
                conn.close()
            except Exception as e:
                print(e)
                pass


if __name__ == '__main__':
    main()
