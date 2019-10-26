import socket  # 引入套接字
import threading  # 引入并行
import pymysql

global recv_data


def udp_send(udp_socket):
    while True:
        num1 = '192.168.3.14'
        num2 = 8080
        # send_data = input('请输入要发送的数据：')
        send_data = recv_data
        # send_data = send_data.encode('utf-8')
        udp_socket.sendto(send_data, (num1, num2))  # sendto（发送数据，发送地址）


def udp_recv(udp_socket):
    while True:
        # recv_data = 0, 0, 0, 0
        # recv_data = list(recv_data)

        recv_data = udp_socket.recv(4096)
        # recv_data = recv_data.decode('utf-8')
        # print('收到信息为:%s'%recv_data)
        print(recv_data)
        # num = int.from_bytes(recv_data, 'little')
        # print(num)
        # print(type(num))
        # print(type(recv_data))
        # udp_socket.sendto(recv_data, ('192.168.3.14', 8080))  # sendto（发送数据，发送地址）

        # 数据解析(4个为一组)
        # recv_data_1 = int("0x" + (recv_data[4 * 0: 4 * 8].decode()).replace("/x", ""), 16)  # 第0-7个元素
        # recv_data_2 = int("0x" + (recv_data[4 * 8: 4 * 16].decode()).replace("/x", ""), 16)  # 第8-15个元素
        # recv_data_3 = int("0x" + (recv_data[4 * 16: 4 * 24].decode()).replace("/x", ""), 16)  # 第16-23个元素
        # recv_data_4 = int("0x" + (recv_data[4 * 24: 4 * 32].decode()).replace("/x", ""), 16)  # 第24-31个元素
        # recv_data_1 = int(recv_data_1, 16)
        # recv_data_2 = int(recv_data_2, 16)
        # recv_data_3 = int(recv_data_3, 16)
        # recv_data_4 = int(recv_data_4, 16)

        # print(recv_data_1)
        # print(recv_data_2)
        # print(recv_data_3)
        # print(recv_data_4)

        # angle = input("请输入定标角度：")
        # InsertAngelData(angle, 1, recv_data_1, recv_data_2, recv_data_3, recv_data_4)


def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建套接字
    # ip = '192.168.3.9'  # 服务器ip和端口
    # port = 8080
    udp_socket.bind((PC_IPAddr, PC_Port))  # 服务器绑定ip和端口
    # 发送数据
    # t=threading.Thread(target=udp_send,args=(udp_socket,))     	# Thread函数用于并行
    # 接收数据
    t1 = threading.Thread(target=udp_recv, args=(udp_socket,))
    # t.start()  # 发送并行开始
    t1.start()


PC_IPAddr = '192.168.3.10'
PC_Port = 8080

if __name__ == '__main__':
    main()

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
DB_IPAddr = "192.168.3.2"


def InsertAngelData(angle, n, ch1_data, ch2_data, ch3_data, ch4_data):
    # 归一化
    min_data = min(ch1_data, ch2_data, ch3_data, ch4_data)
    ch1_data = ch1_data / min_data
    ch2_data = ch2_data / min_data
    ch3_data = ch3_data / min_data
    ch4_data = ch4_data / min_data

    try:
        conn = pymysql.connect(host=DB_IPAddr, port=3306, db='UAV', user='admin_1', passwd='asdfghjkl',
                               charset='utf8')
        cs1 = conn.cursor()
        # str1 = "INSERT INTO "
        # str2 = "angle" + str(angle)
        # str3 = "(id, ch1, ch2, ch3, ch4) VALUES('%d', '%d', '%d', '%d', '%d')"
        sql = "INSERT INTO angle%s(no, ch1, ch2, ch3, ch4) VALUES('%d', '%d', '%d', '%d', '%d')"
        for i in range(1, n + 1):
            count = cs1.execute(sql % (str(angle), i + 1, ch1_data, ch2_data, ch3_data, ch4_data))
            if count:
                print("%d°第%d个值插入成功！" % (angle, i + 1))
            else:
                print("%d°第%d个值插入失败！" % (angle, i + 1))
            conn.commit()
        cs1.close()
        conn.close()
    except Exception as e:
        print(e)
