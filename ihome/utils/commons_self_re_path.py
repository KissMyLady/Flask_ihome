# 创建时间: 2020/6/2 7:14
from werkzeug.routing import BaseConverter
from flask import session, jsonify, g  # g对象-全局上下文
from ihome.utils.response_code import RET
import functools


class BaseReConverter(BaseConverter):
	# 定义正则转换器
	def __init__(self, url_map, regex):
		super().__init__(url_map)
		self.regex = regex


# g对象提供保存数据
# 验证登录状态的装饰器
def login_required(view_func):
	@functools.wraps(view_func)  # 使用装饰器, 恢复被装饰对象的属性
	def wrapper(*args, **kwargs):
		user_id = session.get("user_id")
		if user_id is not None:
			g.user_id = user_id
			return view_func(*args, **kwargs)
		else:
			return jsonify(error_num=RET.SESSIONERR, errmsg="未登录")  # 4101
	return wrapper


# @login_required
# def set_user_avatar():
# 	user_id = g.user_id  # 使用g对象
# 	return jsonify("")