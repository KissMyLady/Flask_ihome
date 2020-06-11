# 文件名: Flask_Project_Code -> datatime
# 创建时间: 2020/6/9 10:12
import time
from datetime import datetime
start_date = "2020-1-06"

start_date = datetime.strptime(start_date, "%Y-%m-%d")
print(start_date)