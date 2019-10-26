import pymysql

try:
    conn = pymysql.connect(host='192.168.3.2', port=3306, db='UAV', user='admin_1', passwd='asdfghjkl',
                           charset='utf8')
    cs1=conn.cursor()
    for i in range(1, 14):
        count=cs1.execute("delete from test where no=%d" % i)
        print(count)
    conn.commit()
    cs1.close()
    conn.close()
except Exception as e:
    print(e)