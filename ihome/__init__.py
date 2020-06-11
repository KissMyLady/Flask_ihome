# coding=utf-8
# 创建时间: 2020/6/1 9:48
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
import redis
from ihome.utils import use_logging
from logging.handlers import RotatingFileHandler


# db = SQLAlchemy(app) 第一种创建方式
# 第二种创建方式 嵌入到创建函数里面
db = SQLAlchemy()

redis_store = None
logg = use_logging.Use_Loggin()


def Create_app_Factroy(conf_name="dev"):
	"""
	描述: 传入配置的名字, 实例化 对应配置的app
	"""
	app = Flask(__name__)
	from config import conf_map
	conf_class = conf_map.get(conf_name)
	
	app.config.from_object(conf_class)   # 导入设置
	db.init_app(app)                     # 数据库嵌入式启动
	
	global redis_store                   # 导入设置.参数
	redis_store = redis.StrictRedis(host=conf_class.REDIS_HOST,
	                                port=conf_class.REDIS_PORT,
	                                db=conf_class.REDIS_DB)
	
	Session(app)
	CSRFProtect(app)
	
	# 注册转换了的转换器
	from ihome.utils import commons_self_re_path
	app.url_map.converters["repath"] = commons_self_re_path.BaseReConverter
	
	from .api_1_0 import api_1_0
	app.register_blueprint(api_1_0, url_prefix="/api/v1.0")  # http://127.0.0.1:5000/v_0_1/
	
	# 注册静态文件的蓝图
	from ihome.Web_Html import web_html
	app.register_blueprint(web_html)  # 不用加前缀了
	return app




