# encoding:utf-8
# 文件名: Flask_Project_Code -> profile
# 创建时间: 2020/6/5 19:25
from . import api_1_0
from flask import request, session
from flask import jsonify
from ihome.utils.commons_self_re_path import login_required  # 登录装饰器
from flask import g
from ihome.utils.response_code import RET
from ihome.utils.use_logging import Use_Loggin
from ihome.utils.updown_image.seven_ox_coludy import down_load_of_Binary
from ihome.models import User
from ihome import constants, db


# 设置用户的头像
@api_1_0.route("/user/avatar", methods=["POST"])
@login_required
def set_use_avatar():
	logging = Use_Loggin()
	# 获取用户参数: 用户id() 图片(多媒体表单, 二进制)
	user_id = g.user_id  # 装饰器代码中已经将user_id保存在g对象, 所以视图可以直接读取
	
	# 获取图片
	row_image_file = request.files.get("avatar")
	if row_image_file is None:
		return jsonify(errno=RET.PARAMERR, errmsg="未上传图片")
	image_data = row_image_file.read()
	
	# 调用七牛云平台上传图片
	try:
		# 正常应该返回文件名
		image_file_name = down_load_of_Binary(image_data)
	except Exception as e:
		logging.error(e)
		return jsonify(errno=RET.THIRDERR, errmsg="上传服务器失败2")
	
	# http://www.mylady.top/static/note_flask --第21节
	'''
	In [31]: User.query.all()
	Out[31]: [User object: name=ying, User object: name=chen, User object: name=zhou]
	​
	In [32]: User.query.filter_by(name='chen').update({'name':'cheng'})
	Out[32]: 1
	​
	In [33]: User.query.all()
	Out[33]: [User object: name=ying, User object: name=cheng, User object: name=zhou]
	'''
	from ihome import db
	try:
		User.query.filter_by(id=user_id).update({"avatar_url": image_file_name})
		db.session.commit()
	except Exception as e:
		db.session.rollback()  # 回滚
		logging.error(e)
		return jsonify(errno=RET.DATAERR, errmsg="数据库保存用户图片url地址失败")
	
	# 成功
	from ihome.constants import URL_OF_QINIU_IMAGE_PREFIX
	http_image_url = str(URL_OF_QINIU_IMAGE_PREFIX + image_file_name)  # 拼接为完整图片url地址
	return jsonify(errno=RET.OK, errmsg="图上保存成功", data={"image_file_name": http_image_url})


# 查询用户是否登录
@api_1_0.route("/user", methods=["GET"])
@login_required
def get_user_profile():
	# 获取个人信息
	user_id = g.user_id
	try:
		user = User.query.get(user_id)
	except Exception as e:
		return jsonify(errno=RET.DATAERR, errmsg="数据库查询错误")
	
	if user is None:
		return jsonify(errno=RET.NODATA, errmsg="无效操作")
	return jsonify(errno=RET.OK, errmsg="OK", data=user.to_dict())


# 用户名字修改
@api_1_0.route("/user/set_name", methods=["PUT"])
@login_required
def set_user_name():
	logging = Use_Loggin()
	# 获取参数
	user_id = g.user_id  # 能够登录装饰器, 说明一定有用户名, 就不验证了
	reqs_data = request.get_json()
	
	if not reqs_data:
		return jsonify(errno=RET.NODATA, errmsg="参数不完整")
	
	row_user_name = reqs_data.get("name")
	if not row_user_name:
		return jsonify(errno=RET.NODATA, errmsg="名字未输入")
	
	# 用户名长度限制
	if len(str(row_user_name)) > constants.USER_SET_NAME_LENG:
		return jsonify(errno=RET.PARAMERR, errmsg="用户名过长")
	
	# 校验参数, 用户名限制在字数以内, 不得使用特殊符号
	for i in constants.USER_SET_NAME_NOT_INCLUDE:
		if i in row_user_name:
			booler = False
			break
		else:
			booler = True

	if booler is False:
		return jsonify(errno=RET.PARAMERR, errmsg="用户不得包含特殊字符")
	
	# 保存用户昵称name，并同时判断name是否重复(利用数据库的唯一索引)
	from ihome import db
	try:
		User.query.filter_by(id=user_id).update({"name": row_user_name})
		#  name = db.Column(db.String(32), unique=True, nullable=False)  # 用户暱称
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		logging.error("用户保存用户名失败, 数据库更新失败")
		return jsonify(errno=RET.DBERR, errmsg="数据库设置用户名失败")
	
	session["name"] = row_user_name
	
	# 返回修改结果
	return jsonify(errno=RET.OK, errmsg="修改成功", data={"name": row_user_name})


# 用户身份证查询
@api_1_0.route("/user/auth", methods=["GET"])
@login_required
def get_idcard():
	# 获取参数
	user_id = g.user_id
	print("user_id: ", user_id)
	try:
		user = User.query.get(user_id)
		print("user: ", user)
	except Exception as e:
		return jsonify(errno=RET.DBERR, errmsg="数据库错误")
	
	if user is None:
		return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
	
	return jsonify(errno=RET.OK, errmsg="OK", data=user.auth_to_dict())


# 用户身份证修改
@api_1_0.route("/user/auth", methods=["POST"])
@login_required
def set_user_idcart():
	user_id = g.user_id
	reqs_dict = request.get_json()
	if not reqs_dict:
		return jsonify(errno=RET.NODATA, errmsg="参数不完整")
	
	real_name = reqs_dict.get("real_name")
	id_card = reqs_dict.get("id_card")
	print("real_name, id_card: ",  real_name, id_card)
	if not all([reqs_dict, id_card]):
		return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
	
	# 参数规格校验
	import re
	try:
		group = re.match('\d{16,18}', id_card)
	except:
		group = False
	if not group:
		return jsonify(errno=RET.PARAMERR, errmsg="身份证格式校验失败")
	try:
		User.query.filter_by(id=user_id, real_name=None, id_card=None).update({"id_card": id_card, "real_name": real_name})
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		return jsonify(errno=RET.DBERR, errmsg="数据更新身份证数据错误/身份证已经存在,禁止更改")

	return jsonify(errono=RET.OK, errmsg="OK")
