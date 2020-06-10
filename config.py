# 创建时间: 2020/6/1 9:32
import redis


class ConfInformation(object):
	# DEBUG = True
	SECRET_KEY = "#riwe#rvds213ew$ewf@1"
	SQLALCHEMY_DATABASE_URI = "mysql://root:YING123ZZ@127.0.0.1:3306/flask_ihome"
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	
	REDIS_HOST = "127.0.0.1"
	REDIS_PORT = "6379"
	REDIS_DB = 0
	
	SESSION_TYPE = 'redis'
	SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
	
	SESSION_USE_SIGNER = True  # 对cookie中的id进行隐藏
	SESSION_PERMANENT = 3600 * 24  # 过期时间秒
	
	
class DevConfig(ConfInformation):
	DEBUG = True
	'''开发模式的配置信息'''
	pass


class ProductConfig(ConfInformation):
	'''生产环境配置信息'''
	pass


conf_map = {
	"dev": DevConfig,
	"pro": ProductConfig
}