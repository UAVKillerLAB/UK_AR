# encoding=utf-8
import pymysql

try:
    conn = pymysql.connect(host='192.168.3.6', port=3306, db='UAV1016', user='admin_0', passwd='asdfghjkl', charset='utf8')
    cs1 = conn.cursor()
    sql = "CREATE TABLE IF NOT EXISTS angle%d (no INT DEFAULT NULL, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, distance int, ch1 VARCHAR(255), ch2 VARCHAR(255), ch3 VARCHAR(255), ch4 VARCHAR(255), ch5 VARCHAR(255), ch6 VARCHAR(255), ch7 VARCHAR(255), ch8 VARCHAR(255), ch1_raw VARCHAR(255), ch2_raw VARCHAR(255), ch3_raw VARCHAR(255), ch4_raw VARCHAR(255), ch5_raw VARCHAR(255), ch6_raw VARCHAR(255), ch7_raw VARCHAR(255), ch8_raw VARCHAR(255))"
    sql1 = "CREATE TABLE IF NOT EXISTS final_table (angle INT DEFAULT NULL, ch1 VARCHAR(255), ch2 VARCHAR(255), ch3 VARCHAR(255), ch4 VARCHAR(255), ch5 VARCHAR(255), ch6 VARCHAR(255), ch7 VARCHAR(255), ch8 VARCHAR(255))"
    sql2 = "CREATE TABLE IF NOT EXISTS %dm (no INT DEFAULT NULL, ch1 VARCHAR(255), ch2 VARCHAR(255), ch3 VARCHAR(255), ch4 VARCHAR(255), ch5 VARCHAR(255), ch6 VARCHAR(255), ch7 VARCHAR(255), ch8 VARCHAR(255))"
    sql3 = "INSERT INTO final_table(angle) VALUES('%d')"
    d = 20, 40, 80
    for i in range(0,360):
        count = cs1.execute(sql % i)
        if count == 0:
            print("%d°数据表创建成功！" % i)
        else:
            print("%d°数据表创建失败！" % i)
        conn.commit()
        # time.sleep(0.001)

    count = cs1.execute(sql1)
    for i in range(0, 360):
        count1 = cs1.execute(sql3 % (i))
    if count == 0 and count1 == 1:
        print("final_table数据表创建成功！")
    else:
        print("final_table数据表创建失败！")

    for i in range(len(d)):
        count = cs1.execute(sql2 % d[i])
        if count == 0:
            print("%dm数据表创建成功！" % d[i])
        else:
            print("%dm数据表创建失败！" % d[i])



    conn.commit()
    cs1.close()
    conn.close()
except Exception as e:
    print(e)