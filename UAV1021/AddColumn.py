# encoding=utf-8
import pymysql
import time
try:
    conn = pymysql.connect(host='192.168.3.6', port=3306, db='UAV', user='admin_0', passwd='asdfghjkl', charset='utf8')
    cs1 = conn.cursor()
    sql = "alter table angle%d add distance int, add ch1_raw varchar(255), add ch2_raw varchar(255), add ch3_raw varchar(255), add ch4_raw varchar(255), add ch5_raw varchar(255), add ch6_raw varchar(255), add ch7_raw varchar(255), add ch8_raw varchar(255)"
    sql1 = "ALTER TABLE angle%d  CHANGE distance distance int AFTER time"
    for i in range(3,360):
        count = cs1.execute(sql % i)
        count1 = cs1.execute(sql1 % i)
        if count == 0 and count1 == 0:
            print("%d°数据表插入新字段成功！" % (i))
        else:
            print("%d°数据表插入新字段失败！" % (i))
        conn.commit()
        time.sleep(0.01)
    cs1.close()
    conn.close()
except Exception as e:
    print(e)