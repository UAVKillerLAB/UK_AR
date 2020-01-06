import mysql.connector

class data_opreation():

    def __init__(self):
        self.host="localhost"
        self.user="root"
        self.passwd="123456"
        self.database="UAV_test"
        self.mydb = mysql.connector.connect(
            host=self.host,
            user = self.user,
            passwd = self.passwd,
            database = self.database)
        self.mycursor = self.mydb.cursor()

    def db_connect(self):
        self.mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )

        self.mycurcor = self.mydb.cursor()

        self.mycurcor.execute("SHOW DATABASES")

        for x in self.mycurcor:
            print(x)
        print("CONNECT SUSSCESSFUL!!")

    def creat_db(self, db_name= 'UAV_test'):
        self.mycurcor.execute("CREATE DATABASE {}".format(db_name))
        return None

    def creat_db_table(self, table_name= 'test'):
        self.mycurcor.execute("CREATE TABLE {} (id INT AUTO_INCREMENT PRIMARY KEY, "
                              "time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                              "latitude VARCHAR(255), longitude VARCHAR(255), "
                              "angle10 VARCHAR(255), distance10 VARCHAR(255), "
                              "angle8 VARCHAR(255), distance8 VARCHAR(255), "
                              "time10 VARCHAR(255), time8 VARCHAR(255))".format(table_name))

    def db_write_test(self):
        latitude = 30.999
        longitude = 104.999
        angle10 = 45.999
        distance10 = 45.999
        angle8 = 45.999
        distance8 = 45.999
        time10 = 45.999
        time8 = 45.999
        sql = "INSERT INTO test (latitude, longitude, angle10, distance10, angle8, distance8, time10, time8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (latitude, longitude, angle10, distance10, angle8, distance8, time10, time8)
        self.mycurcor.execute(sql, val)
        self.mydb.commit()  # 数据表内容有更新，必须使用到该语句

# latitude = 30.999
# longitude = 104.999
# angle10 = 45.999
# distance10 = 45.999
# angle8 = 45.999
# distance8 = 45.999
# time10 = 45.999
# time8 = 45.999
# sql = "INSERT INTO test (latitude, longitude, angle10, distance10, angle8, distance8, time10, time8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
# val = (latitude, longitude, angle10, distance10, angle8, distance8, time10, time8)
# mycursor.execute(sql, val)
# my



db_op= data_opreation()
# db_op.creat_db(db_name='UAV_test2')

print(db_op.database)

db_op.database='UAV_test2'
db_op.db_connect()
db_op.db_write_test()



