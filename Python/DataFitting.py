# encoding=utf-8
import pymysql

'''
##
@brief:定标函数
@param:
        ch1:通道一数据
        ch2:通道二数据
        ch3:通道三数据
        ch4:通道四数据
@retval:
        查表得到的角度值
##
'''
DB_IPAddr = "192.168.3.6"
db_name = "uav1016"

def SelectAngle(m):
    ch1_db_data = []
    ch2_db_data = []
    ch3_db_data = []
    ch4_db_data = []
    try:
        conn = pymysql.connect(host=DB_IPAddr, port=3306, db=db_name, user='admin_0', passwd='asdfghjkl',
                               charset='utf8')
        cs1 = conn.cursor()
        cs1.execute("select ch1 from angle%d where distance = 20" % m)
        result1_20 = cs1.fetchall()
        cs1.execute("select ch2 from angle%d where distance = 20" % m)
        result2_20 = cs1.fetchall()
        cs1.execute("select ch3 from angle%d where distance = 20" % m)
        result3_20 = cs1.fetchall()
        cs1.execute("select ch4 from angle%d where distance = 20" % m)
        result4_20 = cs1.fetchall()

        cs1.execute("select ch1 from angle%d where distance = 40" % m)
        result1_40 = cs1.fetchall()
        cs1.execute("select ch2 from angle%d where distance = 40" % m)
        result2_40 = cs1.fetchall()
        cs1.execute("select ch3 from angle%d where distance = 40" % m)
        result3_40 = cs1.fetchall()
        cs1.execute("select ch4 from angle%d where distance = 40" % m)
        result4_40 = cs1.fetchall()

        cs1.execute("select ch1 from angle%d where distance = 80" % m)
        result1_80 = cs1.fetchall()
        cs1.execute("select ch2 from angle%d where distance = 80" % m)
        result2_80 = cs1.fetchall()
        cs1.execute("select ch3 from angle%d where distance = 80" % m)
        result3_80 = cs1.fetchall()
        cs1.execute("select ch4 from angle%d where distance = 80" % m)
        result4_80 = cs1.fetchall()
        print(result1_20)
        # print(result2)
        # print(result3)
        # print(result4)
        '''
        for i in range(4):
            ch1_db_data.append(float((result1[i])[0]))
            ch2_db_data.append(float((result2[i])[0]))
            ch3_db_data.append(float((result3[i])[0]))
            ch4_db_data.append(float((result4[i])[0]))
        print(ch1_db_data)
        print(ch2_db_data)
        print(ch3_db_data)
        print(ch4_db_data)
        # print(ch1_db_data[0])
        conn.commit()
        cs1.close()
        conn.close()
    except Exception as e:
        print(e)
    ch1_sum = 0
    ch2_sum = 0
    ch3_sum = 0
    ch4_sum = 0
    for i in range(len(ch1_db_data)):
        ch1_sum += ch1_db_data[i]
        ch2_sum += ch2_db_data[i]
        ch3_sum += ch3_db_data[i]
        ch4_sum += ch4_db_data[i]
    ch1_avg = ch1_sum / len(ch1_db_data)
    ch2_avg = ch2_sum / len(ch2_db_data)
    ch3_avg = ch3_sum / len(ch3_db_data)
    ch4_avg = ch4_sum / len(ch4_db_data)
    print("%.15f" % ch1_avg)
    print("%.15f" % ch2_avg)
    print("%.15f" % ch3_avg)
    print("%.15f" % ch4_avg)
    print(type(ch4_sum / len(ch4_db_data)))

    try:
        conn = pymysql.connect(host=DB_IPAddr, port=3306, db=db_name, user='admin_1', passwd='asdfghjkl',
                               charset='utf8')
        cs1 = conn.cursor()
        angle = 50
        # sql = "INSERT INTO final_table(angle, ch1, ch2, ch3, ch4) VALUES('%s', '%.15f', '%.15f', '%.15f', '%.15f')"
        sql = "UPDATE final_table SET ch1='%.15f', ch2='%.15f', ch3='%.15f', ch4='%.15f' WHERE angle=%d"
        count = cs1.execute(sql % (ch1_avg, ch2_avg, ch3_avg, ch4_avg, angle))
        if count:
            print("%d°拟合成功！" % angle)
        else:
            print("%d°拟合失败！可能是因为数据无需拟合。" % angle)
        conn.commit()
        cs1.close()
        conn.close()
        '''
    except Exception as e:
        print(e)



for i in range(50,51):
    SelectAngle(i)
