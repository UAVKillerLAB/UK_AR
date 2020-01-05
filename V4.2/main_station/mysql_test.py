import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="LYD618618",
    database="UAV_test"
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE UAV_test")
# mycursor.execute(
#     "CREATE TABLE test (time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, latitude VARCHAR(255), longitude VARCHAR(255), angle10 VARCHAR(255), distance10 VARCHAR(255), angle8 VARCHAR(255), distance8 VARCHAR(255), time10 VARCHAR(255), time8 VARCHAR(255))")
# mycursor.execute("ALTER TABLE test ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

# mycursor.execute("CREATE TABLE test (id INT AUTO_INCREMENT PRIMARY KEY, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, latitude VARCHAR(255), longitude VARCHAR(255), angle10 VARCHAR(255), distance10 VARCHAR(255), angle8 VARCHAR(255), distance8 VARCHAR(255), time10 VARCHAR(255), time8 VARCHAR(255))")

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
mycursor.execute(sql, val)
mydb.commit()  # 数据表内容有更新，必须使用到该语句