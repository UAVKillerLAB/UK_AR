import socket  # 引入套接字
import threading  # 引入并行
import pymysql
import struct
import serial
import datetime
import matplotlib.pyplot as plt

plt.ion()  # 开启一个画图的窗口
ax = []  # 定义一个 x 轴的空列表用来接收动态的数据

ach1 = []  # 定义一个 y 轴的空列表用来接收动态的数据
ach2 = []
ach3 = []
ach4 = []


# DB_IPAddr = "192.168.3.6"
# DB_Name = "uav_data"


def Print4(counnt, ch1_data, ch2_data, ch3_data, ch4_data):
    data = datetime.date.today()
    # data = datetime.datetime.now().strftime('%Y%m%d0%H%M')
    plt.figure(str(data))
    ax.append(counnt)  # 添加 i 到 x 轴的数据中
    ach1.append(ch1_data)
    ach2.append(ch2_data)
    ach3.append(ch3_data)
    ach4.append(ch4_data)

    plt.clf()  # 清除之前画的图
    plt.plot(ax, ach1)  # 画出当前 ax 列表和 ay 列表中的值的图形
    plt.plot(ax, ach2)
    plt.plot(ax, ach3)
    plt.plot(ax, ach4)

    plt.title(str(data) + 'Channel Map')
    plt.xlabel("Time")
    plt.ylabel("Normalized Amplitude")
    plt.pause(0.1)  # 暂停一秒


# plt.ioff()                   # 关闭画图的窗口


def Print1(counnt, ch1_data):
    ax.append(counnt)  # 添加 i 到 x 轴的数据中
    ach1.append(ch1_data)

    plt.clf()  # 清除之前画的图
    plt.plot(ax, ach1)  # 画出当前 ax 列表和 ay 列表中的值的图形
    plt.pause(0.1)


def udp_send(udp_socket):
    while True:
        num1 = '192.168.3.5'
        num2 = 8080
        # send_data = input('请输入要发送的数据：')
        send_data = "123"
        send_data = send_data.encode('utf-8')
        udp_socket.sendto(send_data, (num1, num2))  # sendto（发送数据，发送地址）
    udp_socket.close()


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
        print("CH1_Raw_data:%.15f\nCH2_Raw_data:%.15f\nCH3_Raw_data:%.15f\nCH4_Raw_data:%.15f" % (
            data[0], data[1], data[2], data[3]))
        InsertAngelData(distance, data[0], data[1], data[2], data[3])
        # Print4(count, data[0], data[1], data[2], data[3])
        # Print1(count,SelectAngle(data[0], data[1], data[2], data[3]))
    udp_socket.close()


def main():
    GetInfo()
    print("%s米开始定标" % distance)
    try:
        conn = pymysql.connect(host=DB_IPAddr, port=3306, db=DB_Name, user='root', passwd='123456',
                               charset='utf8')
        cs1 = conn.cursor()
        sql = "CREATE TABLE IF NOT EXISTS {} (no INT DEFAULT NULL, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, distance int, ch1 VARCHAR(255), ch2 VARCHAR(255), ch3 VARCHAR(255), ch4 VARCHAR(255), ch5 VARCHAR(255), ch6 VARCHAR(255), ch7 VARCHAR(255), ch8 VARCHAR(255), ch1_raw VARCHAR(255), ch2_raw VARCHAR(255), ch3_raw VARCHAR(255), ch4_raw VARCHAR(255), ch5_raw VARCHAR(255), ch6_raw VARCHAR(255), ch7_raw VARCHAR(255), ch8_raw VARCHAR(255))"
        count = cs1.execute(sql.format(TableName))
        # count = cs1.execute(sql)
        if count == 0:
            print("{}数据表创建成功！".format(TableName))
        else:
            print("{}数据表创建失败！".format(TableName))
        conn.commit()
        conn.commit()
        cs1.close()
        conn.close()
    except Exception as e:
        print(e)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建套接字
    udp_socket.bind((PC_IPAddr, PC_Port))  # 服务器绑定ip和端口

    # 接收数据
    # t = threading.Thread(target=udp_recv, args=(udp_socket,))
    t = threading.Thread(target=USB_recv)

    # 发送数据
    # t1 = threading.Thread(target=udp_send, args=(udp_socket,))  # Thread函数用于并行
    # t1.start()  # 发送并行开始
    t.start()


'''
##
@brief:定标函数
@param:
        angle:度数
        n:定标次数
        ch1:通道一数据
        ch2:通道二数据
        ch3:通道三数据
        ch4:通道四数据
@retval:无
##
'''


def InsertAngelData(distance, ch1_raw_data, ch2_raw_data, ch3_raw_data, ch4_raw_data):
    # print("Raw_CH1_data:%.15f\nRaw_CH2_data:%.15f\nRaw_CH3_data:%.15f\nRaw_CH4_data:%.15f" % (
    # ch1_raw_data, ch2_raw_data, ch3_raw_data, ch4_raw_data))
    # 归一化
    min_ch_data = min(ch1_raw_data, ch2_raw_data, ch3_raw_data, ch4_raw_data)
    min_ch_data = float(min_ch_data)
    ch1_data = float(ch1_raw_data) / min_ch_data
    ch2_data = float(ch2_raw_data) / min_ch_data
    ch3_data = float(ch3_raw_data) / min_ch_data
    ch4_data = float(ch4_raw_data) / min_ch_data
    if ch1_data <= 0 or ch2_data <= 0 or ch3_data <= 0 or ch4_data <= 0:
        print("\033[31m数据可能有误！\033[0m")

    try:
        conn = pymysql.connect(host=DB_IPAddr, port=3306, db=DB_Name, user='root', passwd='123456',
                               charset='utf8')
        cs1 = conn.cursor()
        cs1.execute("select count(*) from {}".format(TableName))
        m = cs1.fetchone()
        sql = "INSERT INTO {}(no, distance, ch1, ch2, ch3, ch4, ch1_raw, ch2_raw, ch3_raw, ch4_raw) VALUES('{}', '{}', '{:.15f}', '{:.15f}', '{:.15f}', '{:.15f}', '{}', '{}', '{}', '{}')"
        Print4(m[0], ch1_data, ch2_data, ch3_data, ch4_data)
        count = cs1.execute(sql.format(TableName, m[0] + 1, distance, ch1_data, ch2_data, ch3_data, ch4_data, ch1_raw_data, ch2_raw_data, ch3_raw_data, ch4_raw_data))
        if count:
            print("第%d个值插入成功！\n\n" % (m[0] + 1))
        else:
            print("第%d个值插入失败！\n\n" % (m[0] + 1))
        conn.commit()
        cs1.close()
        conn.close()
    except Exception as e:
        print(e)


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def USB_recv():
    global distance
    ser = serial.Serial("COM5", 115200)
    ser.close()
    ser.open()
    num = 66
    while True:
        USB_recv_data = ((ser.read(num)).decode('ASCII')).replace("\r\n", "")
        USB_recv_data = bytes(USB_recv_data, encoding="utf8")
        data = []
        data.append(int(("0x" + (USB_recv_data[0: 16].decode())), 16))
        data.append(int(("0x" + (USB_recv_data[16: 32].decode())), 16))
        data.append(int(("0x" + (USB_recv_data[32: 48].decode())), 16))
        data.append(int(("0x" + (USB_recv_data[48: 64].decode())), 16))
        InsertAngelData(distance, data[0], data[1], data[2], data[3])
        print("Raw_CH1_data:{:.15f}\nRaw_CH2_data:{:.15f}\nRaw_CH3_data:{:.15f}\nRaw_CH4_data:{:.15f}".format(data[0], data[1], data[2], data[3]))


def Print(counnt, ch1_data, ch2_data, ch3_data, ch4_data):
    ax.append(counnt)  # 添加 i 到 x 轴的数据中
    ach1.append(ch1_data)
    ach2.append(ch2_data)
    ach3.append(ch3_data)
    ach4.append(ch4_data)

    plt.clf()  # 清除之前画的图
    plt.plot(ax, ach1)  # 画出当前 ax 列表和 ay 列表中的值的图形
    plt.plot(ax, ach2)
    plt.plot(ax, ach3)
    plt.plot(ax, ach4)
    plt.pause(0.1)  # 暂停一秒
    # plt.ioff()                   # 关闭画图的窗口


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
        pass
    DB_Name = input("请输入数据库名(默认uav_data):")
    if DB_Name == "":
        DB_Name = "uav_data"
        print("uav_data")
    else:
        pass
    while True:
        distance = input("距离：")
        if distance != "":
            break
        else:
            print("\033[31m请输入距离!\033[0m")
    NowTime = datetime.datetime.now().strftime('%Y%m%d%H%M')
    PC_IPAddr = get_host_ip()
    PC_Port = 8080
    TableName = "m" + distance + "d" + NowTime


if __name__ == '__main__':
    main()
