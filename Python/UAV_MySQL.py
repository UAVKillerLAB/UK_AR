import pymysql
import datetime

DB_IPAddr = "192.168.3.6"
global NowTime
NowTime = datetime.datetime.now().strftime('%Y%m%d%H%M')
NowTime = "201910232212"
def ExecuteMySQL(DBName, sql, *values):
    try:
        conn = pymysql.connect(host=DB_IPAddr, port=3306, db=DBName, user='root', passwd='123456',
                               charset='utf8')
        cs1 = conn.cursor()
        NowTime = "201910181815"
        # 判断执行类型
        if "SELECT" in sql or "select" in sql:
            # for j in s1:
            if "*" in sql:
                print("fectchone")
                cs1.execute("select count(*) from d%s" % NowTime)
            else:
                print("fectchall")
        else:
        # 增加数据命令
            # print("insert")
            # print(type(values[0]))
            sql = sql.split("(n")
            sql[0] = (sql[0] % NowTime)
            sql = sql[0] +"(n" + sql[1]
            count = cs1.execute(sql % values)
            # if count:
            #     print("第%d个值插入成功！\n\n" % (i + 1))
            # else:
            #     print("第%d个值插入失败！\n\n" % (i + 1))
        conn.commit()
        cs1.close()
        conn.close()
        return count
    except Exception as e:
        print(e)


# ExecuteMySQL("uav_data", "INSERT INTO", 1,11)
# ExecuteMySQL("uav_data", "select count(*) from d%s", 1,11)
sql1 = "INSERT INTO d%s(no, distance, ch1, ch2, ch3, ch4, ch1_raw, ch2_raw, ch3_raw, ch4_raw) VALUES('%d', '%d', '%.15f', '%.15f', '%.15f', '%.15f', '%d', '%d', '%d', '%d')"
temp  = 123.123
result = ExecuteMySQL("uav1015", sql1, temp, temp, temp, temp, temp, temp, temp, temp, temp, temp)
# ExecuteMySQL("uav1015", sql1, temp, temp, temp, temp, temp, temp, temp, temp, temp, temp)
if result:
    print("第%d个值插入成功！\n\n" % 1)
else:
    print("第%d个值插入失败！\n\n" % 1)
# print(datetime.datetime.now().strftime('%Y%m%d-%H%M'))