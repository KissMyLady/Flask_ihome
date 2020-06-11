# 文件名: Flask_Project_Code -> insert_areas
# 创建时间: 2020/6/6 16:48
from pymysql import *
import os, sys
import datetime


# 删除数据
# delete from study_flask_note where id >100;

def main():
	n = datetime.datetime.now()
	conn = connect(host='localhost',
	               port=3306,
	               database='flask_ihome',
	               user='root',
	               password='YING123ZZ',
	               charset='utf8')
	
	cs1 = conn.cursor()
	try:
		count = cs1.execute("INSERT INTO `ih_facility_info`(`name`) VALUES('无线网络'),('热水淋浴'),('空调'),('暖气'),('允许吸烟'),('饮水设备'),('牙具'),('香皂'),('拖鞋'),('手纸'),('毛巾'),('沐浴露、洗发露'),('冰箱'),('洗衣机'),('电梯'),('允许做饭'),('允许带宠物'),('允许聚会'),('门禁系统'),('停车位'),('有线网络'),('电视'),('浴缸');")
		conn.commit()
		cs1.close()
		conn.close()
	except:
		print('error')


if __name__ == '__main__':
	main()
	

