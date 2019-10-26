# encoding=utf-8
import pymysql
import socket  # 引入套接字
import threading  # 引入并行

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
DB_IPAddr = "192.168.3.6"


def InsertAngelData(angle, n, ch1_data, ch2_data, ch3_data, ch4_data):
    # 归一化
    # min_data = min(ch1_data, ch2_data, ch3_data, ch4_data)
    # ch1_data = ch1_data / min_data
    # ch2_data = ch2_data / min_data
    # ch3_data = ch3_data / min_data
    # ch4_data = ch4_data / min_data

    try:
        conn = pymysql.connect(host=DB_IPAddr, port=3306, db='uav1015', user='root', passwd='123456',
                               charset='utf8')
        cs1 = conn.cursor()
        # str1 = "INSERT INTO "
        # str2 = "angle" + str(angle)
        # str3 = "(id, ch1, ch2, ch3, ch4) VALUES('%d', '%d', '%d', '%d', '%d')"
        cs1.execute("select count(*) from angle%s" % str(angle))
        m = cs1.fetchone()
        sql = "INSERT INTO angle%s(no, ch1, ch2, ch3, ch4) VALUES('%d', '%d', '%d', '%d', '%d')"
        for i in range(m[0], n + m[0]):
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


temp = 18446744073709551615
InsertAngelData(99, 1, temp, temp, temp, temp)

# def InsertAngelData_c():
#     # 归一化
#
#     try:
#         conn = pymysql.connect(host=DB_IPAddr, port=3306, db='UAV', user='admin_1', passwd='asdfghjkl',
#                                charset='utf8')
#         cs1 = conn.cursor()
#         sql = "INSERT INTO final_table(angle) VALUES('%d')"
#         for i in range(0, 360):
#             count = cs1.execute(sql % (i))
#             # if count:
#             #     print("%d°第%d个值插入成功！" % (angle, i + 1))
#             # else:
#             #     print("%d°第%d个值插入失败！" % (angle, i + 1))
#             conn.commit()
#         cs1.close()
#         conn.close()
#     except Exception as e:
#         print(e)


# InsertAngelData_c()
