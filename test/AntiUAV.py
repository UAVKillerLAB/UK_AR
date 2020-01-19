import socket  # 引入套接字
import threading  # 引入并行
import pymysql
import struct
import serial
import datetime
import matplotlib.pyplot as plt

class Connection:

    def USB_recv(self):
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
            # InsertAngelData(distance, data[0], data[1], data[2], data[3])
            print("Raw_CH1_data:{:.15f}\nRaw_CH2_data:{:.15f}\nRaw_CH3_data:{:.15f}\nRaw_CH4_data:{:.15f}".format(data[0], data[1], data[2], data[3]))

    def udp_send(self):
        while True:
            num1 = '192.168.3.5'
            num2 = 8080
            # send_data = input('请输入要发送的数据：')
            send_data = "123"
            send_data = send_data.encode('utf-8')
            self.sendto(send_data, (num1, num2))  # sendto（发送数据，发送地址）
        self.close()

    def udp_recv(self):
        send_data = '1'
        send_data = send_data.encode('utf-8')
        self.sendto(send_data, ('192.168.3.10', 7))
        # 问题描述：套接字必须发送一次才能接收
        count = 0
        while True:
            # for i in range(1000):
            receive_message, client = self.recvfrom(4096)
            # print(receive_message)
            data = struct.unpack('<4q', receive_message)  # 调用struct库解包，>4q代表4个long long 大端对齐<4q代表4个long long 小端对齐
            warning = "板子是小端，网络调试助手是大端！！！"
            # for i in range(len(data)):  # 循环打印data结构体的值
            #     print(data[i])
            count = count + 1
            print("CH1_Raw_data:%.15f\nCH2_Raw_data:%.15f\nCH3_Raw_data:%.15f\nCH4_Raw_data:%.15f" % (
                data[0], data[1], data[2], data[3]))
            # InsertAngelData(distance, data[0], data[1], data[2], data[3])
        self.close()

if __name__ == '__main__':
    main()
