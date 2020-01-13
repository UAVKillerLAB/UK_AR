# encoding=utf-8
import socket  # 引入套接字
import threading  # 引入并行

import numpy as np
import pymysql
import struct
import serial
import matplotlib.pyplot as plt
import datetime
import math
import sys
import time

sys.path.append(r'D:\OneDrive\Python_project\Github\AntiUAV_Python\Python')

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
ch1_db_data = []
ch2_db_data = []
ch3_db_data = []
ch4_db_data = []

matched_angle_buff = []

matched_angle = 0
matched_angle_mid = 0
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
angle_db_data = []
run_flag = 0

'''
##
@brief:定标函数
@param:
        ch1_raw_data:通道一数据
        ch2_raw_data:通道二数据
        ch3_raw_data:通道三数据
        ch4_raw_data:通道四数据
@retval:
        查表得到的角度值
##
'''


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
    plt.ylabel("Normalized Amplitude")
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


def SelectData():
    global ch1_db_data
    global ch2_db_data
    global ch3_db_data
    global ch4_db_data

    global angle_db_data
    try:
        conn = pymysql.connect(host=DB_IPAddr, port=3306, db=DB_Name, user='root', passwd="123456",
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
    # print("Raw_CH1_data:%.15f\nRaw_CH2_data:%.15f\nRaw_CH3_data:%.15f\nRaw_CH4_data:%.15f" % (
    # ch1_raw_data, ch2_raw_data, ch3_raw_data, ch4_raw_data))
    global ch1_db_data
    global ch2_db_data
    global ch3_db_data
    global ch4_db_data
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
    Process_data = angle_db_data[Process_data]
    result = DataProcess(count_time, Process_data, Last_rawdata)

    count_time += 1

    return result


def udp_send(udp_socket, BetaAngle):
    mhesIPAddr = '192.168.3.2'  # 民航二所IP
    mhesPort = 10002

    # 民航二所Port
    # send_data = input('请输入要发送的数据：')
    send_data_head = 0xb3b3
    send_data_headlen = 34
    send_data_latitude = 103
    send_data_longitude = 31
    send_data_height = 790
    send_data_tarqua = 1
    send_data_end = 0xb1af
    send_data_tracknum = 1
    send_data_trackdis = 0
    send_data_bata = BetaAngle
    send_data_time = time.time()
    send_data_trackrate = 0
    send_data = struct.pack('<HHdddIHidddd', send_data_head, send_data_headlen, send_data_latitude,
                            send_data_longitude, send_data_height, send_data_tarqua, send_data_end,
                            send_data_tracknum, send_data_trackdis, send_data_bata, send_data_time,
                            send_data_trackrate)

    print(len(send_data))
    # input('enter')
    # send_data = send_data.encode('utf-8') #这行代码需要测试 一达测试版本中没有这一行
    udp_socket.sendto(send_data, (mhesIPAddr, mhesPort))  # sendto（发送数据，发送地址）
    # udp_socket.close()


def udp_recv(udp_socket):
    send_data = '1'
    send_data = send_data.encode('utf-8')
    udp_socket.sendto(send_data, ('192.168.3.10', 7))
    # 问题描述：套接字必须发送一次才能接收
    count = 0
    while True:
        # for i in range(1000):
        receive_message, client = udp_socket.recvfrom(4096)
        # print(receive_message)
        data = struct.unpack('<4q', receive_message)  # 调用struct库解包，>4q代表4个long long 大端对齐<4q代表4个long long 小端对齐
        warning = "板子是小端，网络调试助手是大端！！！"
        # for i in range(len(data)):  # 循环打印data结构体的值
        #     print(data[i])
        count = count + 1
        print("Raw_CH1_data:%.15f\nRaw_CH2_data:%.15f\nRaw_CH3_data:%.15f\nRaw_CH4_data:%.15f" % (
            data[0], data[1], data[2], data[3]))
        matched_angle = SelectAngle(data[0], data[1], data[2], data[3])
        Print4(count, data[0], data[1], data[2], data[3], matched_angle)
        # Print1(count,SelectAngle(data[0], data[1], data[2], data[3]))
        print("当前角度为: %d°" % matched_angle)
        print("\n\n")
    udp_socket.close()


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def USB_recv():
    ser = serial.Serial("COM5", 115200)
    ser.close()
    ser.open()
    num = 66
    count = 0
    size = 11
    process_buff = []
    global matched_angle_buff
    global matched_angle_mid
    global run_flag
    while True:
        if run_flag == 1:
            run_flag = 0
            # 解析数据
            USB_recv_data = ((ser.read(num)).decode('ASCII')).replace("\r\n", "")
            USB_recv_data = bytes(USB_recv_data, encoding="utf8")
            data = []
            data.append(int(("0x" + (USB_recv_data[0: 16].decode())), 16))
            data.append(int(("0x" + (USB_recv_data[16: 32].decode())), 16))
            data.append(int(("0x" + (USB_recv_data[32: 48].decode())), 16))
            data.append(int(("0x" + (USB_recv_data[48: 64].decode())), 16))
            count = count + 1
            # 动态画图
            print("Raw_CH1_data:%.15f\nRaw_CH2_data:%.15f\nRaw_CH3_data:%.15f\nRaw_CH4_data:%.15f" % (
                data[0], data[1], data[2], data[3]))

            matched_angle = SelectAngle(data[0], data[1], data[2], data[3])

            # matched_angle_buff.append(matched_angle)
            #
            # if len(matched_angle_buff) >= 5:
            #     # matched_angle_mid=matched_angle_buff[0]+matched_angle_buff[1]+matched_angle_buff[2]
            #     # matched_angle_mid=matched_angle_mid/3
            #
            #     matched_angle_mid = sum(matched_angle_buff) / (len(matched_angle_buff) * 1.0)  # 求平均，平滑数据
            #     matched_angle_buff = []
            process_buff.append(matched_angle)

            if len(process_buff) >= size:
                buff_std = np.std(process_buff)
                buff_mean = np.mean(process_buff)

                loss = abs(matched_angle- buff_mean)


                if loss > 10:
                    #                         print('++++++++\n++++++++\n')

                    if matched_angle - np.mean(process_buff) < 0:
                        process_buff.pop()

                        process_buff.append(process_buff[-1] - 1)

                    if matched_angle - np.mean(process_buff) > 0:
                        process_buff.pop()

                        process_buff.append(process_buff[-1] + 1)
                print(process_buff)
                process_buff.pop(0)

            matched_angle = process_buff[-1]



            udp_send(udp_socket, matched_angle)
            Print4(count, data[0], data[1], data[2], data[3], matched_angle)

            # Print1(count,SelectAngle(data[0], data[1], data[2], data[3]))
            print("\033[31m当前角度为:{} \033[0m".format(matched_angle))
            print("\n\n")
    ser.close()


def GetInfo():
    global DB_IPAddr
    global DB_Name
    global distance
    global NowTime
    global PC_IPAddr
    global PC_Port
    global TableName
    DB_IPAddr = input("请输入数据库IP地址(默认192.168.3.2):192.168.")
    if DB_IPAddr == "":
        DB_IPAddr = "192.168.3.2"
        print("192.168.3.2")
    else:
        DB_IPAddr = "192.168." + DB_IPAddr
        print(DB_IPAddr)
        pass
    DB_Name = input("请输入数据库名(默认uav_data):")
    if DB_Name == "":
        DB_Name = "uav_data"
        print(DB_Name)
    else:
        print(DB_Name)
        pass
    # while True:
    #     distance = input("距离：")
    #     if distance != "":
    #         break
    #     else:
    #         print("\033[31m请输入距离!\033[0m")
    # NowTime = datetime.datetime.now().strftime('%Y%m%d%H%M')
    # PC_IPAddr = get_host_ip()
    # PC_Port = 8080
    # TableName = "m" + distance + "d" + NowTime


def read_time():
    nts = [0, 0]
    global run_flag
    while True:
        # 获取当前时间
        # nts[1] = int(time.strftime('%S', time.localtime(time.time())))
        nts[1] = time.time()
        # 如果秒钟突变
        # if nts[1] != nts[0]:

        print('nts[1]:',nts[1])
        print('nts[0]:',nts[0])
        print('nts[1]-nts[0]:',nts[1]-nts[0])

        if nts[1] - nts[0] >= 0.2:
            run_flag = 1
            # print(nts)
            nts[0] = nts[1]
        print('1')
        # 延时30ms
        time.sleep(0.03)


def main():
    GetInfo()
    a = input("Press any key to start.")
    print("等待接收数据")
    SelectData()
    global udp_socket
    global matched_angle

    PC_IPAddr = get_host_ip()
    PC_Port = 8080
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建套接字
    udp_socket.bind((PC_IPAddr, PC_Port))  # 服务器绑定ip和端口

    # 接收数据
    # t = threading.Thread(target=udp_recv, args=(udp_socket,))
    t = threading.Thread(target=USB_recv)
    t1 = threading.Thread(target=read_time)
    t.start()
    # 发送数据
    # t1 = threading.Thread(target=udp_send, args=(udp_socket,))  # Thread函数用于并行
    # t1.start()  # 发送并行开始
    t1.start()


if __name__ == '__main__':
    main()
