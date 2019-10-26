import pymysql


'''
##
@brief:定标函数
@param:
        ch1_raw_data:通道一数据
        ch2_raw_data:通道二数据
        ch3_raw_data:通道三数据
        ch4_raw_data:通道四数据
@retval:
        查表得到的角度值
##
'''


def SelectAngle(ch1_data, ch2_data, ch3_data, ch4_data):
	# ch1_data = 9.650872
	# ch2_data = 1.132438
	# ch3_data = 2.504602
	# ch4_data = 1.024494
	ch1_db_data = []
	ch2_db_data = []
	ch3_db_data = []
	ch4_db_data = []
	# print("Raw_CH1_data:%.15f\nRaw_CH2_data:%.15f\nRaw_CH3_data:%.15f\nRaw_CH4_data:%.15f" % (
	#     ch1_raw_data, ch2_raw_data, ch3_raw_data, ch4_raw_data))
	# # 归一化
	# min_ch_data = min(ch1_raw_data, ch2_raw_data, ch3_raw_data, ch4_raw_data)
	# min_ch_data = float(min_ch_data)
	# ch1_data = float(ch1_raw_data) / min_ch_data
	# ch2_data = float(ch2_raw_data) / min_ch_data
	# ch3_data = float(ch3_raw_data) / min_ch_data
	# ch4_data = float(ch4_raw_data) / min_ch_data
	# if ch1_data + ch2_data + ch3_data + ch4_data <= 4:
	#     print("数据可能有误！")

	try:
		conn = pymysql.connect(host='192.168.3.6', port=3306, db='uav1015', user='root', passwd='123456',
							   charset='utf8')
		cs1 = conn.cursor()
		cs1.execute("select ch1 from final_table")
		result1 = cs1.fetchall()
		cs1.execute("select ch2 from final_table")
		result2 = cs1.fetchall()
		cs1.execute("select ch3 from final_table")
		result3 = cs1.fetchall()
		cs1.execute("select ch4 from final_table")
		result4 = cs1.fetchall()
		# print(result1)
		# print(result2)
		# print(result3)
		# print(result4)
		for i in range(181):
			ch1_db_data.append(float((result1[i])[0]))
			ch2_db_data.append(float((result2[i])[0]))
			ch3_db_data.append(float((result3[i])[0]))
			ch4_db_data.append(float((result4[i])[0]))

		# print(result1[0])
		# conn.commit()
		cs1.close()
		conn.close()

	except Exception as e:
		print(e)
		pass

	sum_difference = []
	for i in range(181):
		ch1_difference = (ch1_db_data[i] - float(ch1_data)) ** 2  # 差值放大
		ch2_difference = (ch2_db_data[i] - float(ch2_data)) ** 2  # 差值放大
		ch3_difference = (ch3_db_data[i] - float(ch3_data)) ** 2  # 差值放大
		ch4_difference = (ch4_db_data[i] - float(ch4_data)) ** 2  # 差值放大
		sum_difference.append(ch1_difference + ch2_difference + ch3_difference + ch4_difference)
	# print(sum_difference)
	# print(min(sum_difference))
	# print(sum_difference.index(min(sum_difference)))
	return sum_difference.index(min(sum_difference))
	# print(sum_difference.index(min(sum_difference)))
	# try:
	#     conn = pymysql.connect(host='192.168.3.6', port=3306, db='uav1015', user='root', passwd='123456',
	#                            charset='utf8')
	#     cur = conn.cursor()
	#     cur.execute("select angle from final_table where no=%d + 1" % sum_difference.index(min(sum_difference)))
	#     result = cur.fetchone()
	#     # print(result[0])
	#     cur.close()
	#     conn.close()
	# except Exception as e:
	#     print(e)
	# finally:
	#     return result[0]

print(SelectAngle(10, 1.132438, 2.504602, 1.1))