# 创建时间: 2020/6/1 14:22
import logging
from logging.handlers import RotatingFileHandler
import os


def Use_Loggin():
	"""
	描述: 日志模块, 控制台与文件内同时记载
	注意: Flask开启调试模式会强制让logging=DEBUG
	:return: logger
	"""
	logger = logging.getLogger()    # 实例化log对象
	logger.setLevel(logging.DEBUG)  # Log等级总开关
	
	PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r"\logs\test_log2.txt"
	
	# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限  Bytes字节 = 8位
	file_log_handler = RotatingFileHandler(PATH, maxBytes=1024*1024*20, backupCount=10, encoding="utf-8")
	
	# 创建一个handler，用于输出到控制台
	ch_set3 = logging.StreamHandler()
	ch_set3.setLevel(logging.INFO)  # 输出到console的log等级的开关
	
	formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
	
	ch_set3.setFormatter(formatter)             # 控制台 设置格式
	file_log_handler.setFormatter(formatter)    # 日志器 设置格式
	
	# 为全局的日志工具对象（flask app使用的）添加日记录器
	logger.addHandler(file_log_handler)
	
	# 将logger添加到handler里面
	logger.addHandler(ch_set3)
	return logger


if __name__ == "__main__":
	logger = Use_Loggin()

	# 日 志
	logger.debug('这是 logger debug message')
	logger.info('-'*30)
	logger.info('这是 logger info message')
	logger.warning('这是 logger warning message')
	logger.error('这是 logger error message')
	logger.critical('这是 logger critical message')