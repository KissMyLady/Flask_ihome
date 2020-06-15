# 文件名: Flask_Project_Code -> passport
# 创建时间: 2020/6/4 9:55
# passport.py: 用户 存取 注册 登录
from . import api_1_0
from ihome.utils.response_code import RET
from ihome.utils.use_logging import Use_Loggin
from sqlalchemy.exc import IntegrityError
from ihome import redis_store, db
from flask import request, session, g
from flask import jsonify
from ihome import constants
from ihome.models import User
import re
from ihome.utils.commons_self_re_path import login_required


# 用户注册验证
@api_1_0.route("/users", methods=["POST"])
def register():
	logging = Use_Loggin()
	"""
	请求参数: 1. 手机号
			 2. 短信验证码
			 3. 密码, 确认密码
	参数格式: json
	:return:
	"""
	from flask import request
	req_dict = request.get_json()  # 获取请求的json, 返回字典
	mobile = req_dict.get("mobile")
	sms_code = req_dict.get("sms_code")
	password = req_dict.get("password")
	password2 = req_dict.get("password2")
	
	# 校验参数
	if not all([mobile, sms_code, password, password2]):
		return jsonify(error_num=RET.PARAMERR, errmsg="数据不完整")
	
	# 校验手机格式
	if not re.match(r"1[34578]\d{9}", mobile):
		return jsonify(error_num=RET.PARAMERR, errmsg="手机格式不正确")
	# 校验密码
	if password != password2:
		return jsonify(error_num=RET.PARAMERR, errmsg="两次输入密码不一致")
	
	# 业务逻辑处理, 从 redis取出短信验证码
	try:
		# 注意: 从redis提取的数据属于 bytes类型, 需要decode
		real_sms_txt = redis_store.get("sms_code_%s" % mobile)
		
	except Exception as e:
		logging.error("redis数据读取错误")
		logging.error(e)
		return jsonify(error_num=RET.PARAMERR, errmsg="读取真实短信验证码异常")
	
	# 判断短信验证码是否过期
	if real_sms_txt is None:
		return jsonify(error_num=RET.NODATA, errmsg="短信验证码过期")
	
	if constants.MSG_CODE_True_OR_False is False:
		# 删除redis中的短信验证码, 防止校验失败后的重复校验 这里我不删除, 短信可以重复利用
		try:
			redis_store.delete("sms_code_%s" % mobile)
		except Exception as e:
			logging.error("短信验证码删除失败")
			logging.error(e)
	
	# 判断用户填写的短信验证码的正确性
	# print("->"*10, type(real_sms_txt), real_sms_txt, type(sms_code), sms_code)
	# <class 'bytes'> b'075857' <class 'str'> 075857
	if real_sms_txt.decode("utf-8") != sms_code:
		return jsonify(error_num=RET.DATAERR, errmsg="短信验证码错误")
	
	# 判断手机号是否注册过
	# 手机号是否存在
	from ihome.models import User
	try:
		user = User.query.filter_by(mobile=mobile).first()
	except Exception as e:
		logging.error("注册时, 数据库手机号查询错误")
		logging.error(e)
		return jsonify(error_num=RET.DATAERR, errmsg="数据库查询是否重复手机号时异常")
	else:
		if user != None:
			return jsonify(error_num=RET.DATAEXIST, errmsg="注册手机已存在")
	
	# 保存到数据库中
	# 加密处理
	user = User(name=mobile, mobile=mobile)
	# user.generate_password_hash(password)
	user.password = password   # 设置值
	# print(user.password())   # 读取值--设置了报错
	
	try:
		db.session.add(user)
		db.session.commit()    # 数据正式保存
	except IntegrityError as e:
		db.session.rollback()  # 数据库操作错误的回滚
		logging.error(e)
		logging.error("手机号出现重复值, 用户已经注册")
		return jsonify(error_num=RET.DATAEXIST, errmsg="手机号出现重复值")
	except Exception as e:
		logging.error(e)
		logging.error("数据库出现了问题")
		return jsonify(error_num=RET.DATAEXIST, errmsg="查询数据库异常")
	
	# 保存登录状态到session中
	from flask import session  # 从flask中导入全局的请求上下文
	session["name"] = mobile
	session["mobile"] = mobile
	session["user_id"] = user.id
	return jsonify(errno=RET.OK, errmsg="用户注册成功")
	

# 用户登录验证
@api_1_0.route("/session", methods=["POST"])
def login():
	logging = Use_Loggin()
	# 参数提取
	reqs_dice = request.get_json()
	mobile = reqs_dice.get("mobile")
	pwd = reqs_dice.get("password")
	
	# 参数校验
	if not all([mobile, pwd]):
		return jsonify(error_num=RET.PARAMERR, errmsg="参数不完整")
	
	mobile_re = re.match(r'1[34578]\d{9}', mobile)
	if mobile_re == None:
		return jsonify(error_num=RET.PARAMERR, errmsg="手机号格式错误")
	
	# 判断错误次数, 保存到redis中, 时间限制
	try:
		user_ip = request.remote_addr
		# "access_nums_ip地址": "次数"
		access_conut = redis_store.get("access_nums_%s" % user_ip)
	except Exception as e:
		logging.warning("警告: redis查询用户ip地址次数错误, 这里不限制访问, 让用户继续访问")
	else:
		if access_conut != None:
			if int(access_conut.decode('utf-8')) >= constants.LOGIN_MUNS_COUNTS:
				return jsonify(error_num=RET.REQERR, errmsg="请求次数过于频繁")
		else:
			pass
		
	# 比对数据库账号密码
	try:
		user = User.query.filter_by(mobile=mobile).first()
	except:
		logging.error("错误: 数据库查询错误")
		return jsonify(error_num=RET.DATAERR, errmsg="获取用户信息失败")
	
	# 如果输入错误, 记录错误次数, 次数过多, 封ip
	if user is None or not user.check_pwd(pwd):   # 如果找不到用户 or 密码  返回错误信息
		try:
			# 额外配置, 错误后计数访问主机的ip地址
			redis_store.incr("access_nums_%s" % user_ip, amount=1)
			redis_store.expire("access_nums_%s" % user_ip, time=constants.LOGIN_MUNS_NOTIME)
		except:
			pass
		# 因为用户名或者密码错误, 这里直接返回错误信息
		return jsonify(error_num=RET.NODATA, errmsg="用户名或密码不存在")
	
	# 验证成功
	from flask import session
	session["name"] = user.name
	session["mobile"] = user.mobile
	session["user_id"] = user.id
	
	return jsonify(errno=RET.OK, errms="登录成功")


# 主页, 询问用户是否已经登录
@api_1_0.route("/session", methods=["GET"])
def check_login():
	name = session.get("name")
	# print("name: ", name) 有显示用户名
	if name is not None:
		return jsonify(errno=RET.OK, errmsg="true", data={"name": name})
	else:
		return jsonify(errno=RET.SESSIONERR, errmsg="false")


# 删除session
@api_1_0.route("/session", methods=["DELETE"])
def delete_session():
	csrf_token = session.get("csrf_token")
	session.clear()
	session["csrf_token"] = csrf_token
	return jsonify(errno=RET.OK, errmsg="Delete session OK")







