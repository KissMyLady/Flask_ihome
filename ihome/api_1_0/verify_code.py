# 文件名: Flask_Project_Code -> verify_code
# 创建时间: 2020/6/2 15:33
from . import api_1_0
from flask import jsonify, request
from ihome import redis_store
from ihome.utils.use_logging import Use_Loggin
from ihome.utils.response_code import RET
from ihome import db
from ihome.models import User
from ihome.constants import MSG_CODE_LONG_EXPIES


@api_1_0.route("/image_code/<image_code_id>")
def get_image_code(image_code_id):
	"""
	获取图片验证码
	: params image_code_id 验证码编号
	:return:  正常: 返回验证码图片   不正常: 抛出异常json
	"""
	from ihome.utils.captcha_for_python3 import captcha
	captcha = captcha.Captcha.instance()
	img_name, img_text, img_data = captcha.generate_captcha()
	# redis  还要设置有效期
	# "key":"xxx-xxx-xxx"
	# "image_code_id": {"编号1":"真实文本", "id2":"真实文本2"}
	# "image_code_id": {"id1":"abc", "id2":"vdc"} hset("image_code_id", "id1", "abc", "")

	# 有效期
	from ihome.constants import IMAGE_CODE_REDIS_EXPIES
	# redis_store.set("image_code_%s" % image_code_id, img_text)
	# redis_store.expire("image_code_%s" % image_code_id, IMAGE_CODE_REDIS_EXPIES)  # 秒
	try:
		redis_store.setex("image_code_%s" % image_code_id, value=img_text, time=IMAGE_CODE_REDIS_EXPIES)
	
	except Exception as e:
		from ihome.utils import use_logging
		logg = use_logging.Use_Loggin()
		logg.error("警告, Redis未启动或是错误, 请查看 ihome->api_1_o->verify_code.py文件的验证模块是否错误")
		logg.error(e)
		return jsonify(error_num=RET.DBERR, errmsg="Save image is Error in verify_code.py")
	
	from flask import make_response
	resp = make_response(img_data)              # 返回二进制数据
	resp.headers["Content-Type"] = "image/jpg"  # 声明为图片格式
	return resp


# http://127.0.0.1:5000/api/v1.0/sms_code/?13207297072?image_code=COMR&image_code_id=11
# GET /api/v1.0/sms_codes/<mobile>?image_code=xxxx&image_code_id=xxxx
@api_1_0.route("sms_code/<repath(r'1[34578]\d{9}'):msg_code_phone>")
def get_msm_code(msg_code_phone):
	logg = Use_Loggin()         # 获取日志对象
	# 获取参数
	phone_nums = msg_code_phone                          # 获取: 手机号这个参数
	image_code = request.args.get("image_code")          # 获取: 验证码真实值
	image_code_id = request.args.get("image_code_id")    # 获取: 验证码对应的图片, 需要及时删除 Js生成的UUID

	# 校验数据
	if not all([image_code, image_code_id]):
		return jsonify(error_num=RET.DATAERR, errmsg="参数不完整")

	# 从redis取出 真实的图片value
	from ihome.utils.response_code import RET
	try:
		real_image_code = redis_store.get("image_code_%s" % image_code_id)

	except Exception as e:
		logg.error("错误, 短信验证--redis_store.get(image_code_ image_code_id)提取信息错误")
		return jsonify(error_num=RET.DBERR, errmsg="Redis 数据库异常")

	if real_image_code is None:
		return jsonify(error_num=RET.NODATA, errmsg="Redis 没有验证码信息")

	# -------------判断验证码值是否正确-------------
	# print("real_image_code: ", real_image_code, "  real_image_code.lower(): ", real_image_code.lower().decode('utf-8'))
	# print("image_code: ", image_code, "  image_code.lower(): ", image_code.lower())
	# print(type(real_image_code.lower()))

	# -存在撞库风险, 如果在之后删除redis数据,
	# 为什么选择这里 ?
	try:
		redis_store.delete("image_code_%s" % image_code_id)
	except Exception as e:
		logg.warning("警告: Redis删除验证码图片失败 (非主要错误) , ")
		logg.warning(e)

	if real_image_code.lower().decode('utf-8') != image_code.lower():
		return jsonify(error_num=RET.DBERR, errmsg="图片验证码错误")

	# 判断对于手机号操作, 60s之内不允许操作
	try:
		second_info = redis_store.get("def_sms_code_%s" % phone_nums)
	except Exception as e:
		pass
	else:
		if second_info is not None:
			return jsonify(error_num=RET.REQERR, errmsg="请求频繁")

	# 手机号是否存在
	try:
		user = User.query.filter_by(mobile=phone_nums).first()
	except Exception as e:
		user = None
		logg.error("注册时, 数据库手机号查询错误")

	else:
		if user is not None:
			return jsonify(error_num=RET.DATAEXIST, errmsg="注册手机已存在")

	# 返回短信验证码, 保存在 redis中
	from random import randint
	sms_code = "%06d" % randint(0, 999999)  # 发送的验证码真实值
	try:
		# 有效期
		from ihome.constants import MSG_CODE_REDIS_EXPIES  # 保存到 redis的验证码值
		redis_store.setex("sms_code_%s" % phone_nums, value=sms_code, time=MSG_CODE_REDIS_EXPIES)

		# 保存60s设置, 防止60s内再次触发发送短信的请求
		redis_store.setex("def_sms_code_%s" % phone_nums, value="1", time=MSG_CODE_LONG_EXPIES)

	except Exception as e:
		logg.error("注册时, 保存短信验证码异常1")
		logg.error(e)
		return jsonify(error_num=RET.DBERR, errmsg="Redis 保存短信验证码异常")
	
	# 异步发送短信 windows不支持 celery ?
	# try:
	# 	from ihome.task.sms_send_tasks import send_sms
	# 	send_sms.delay(phone_nums,
	# 	               [sms_code,
	# 	                int(MSG_CODE_REDIS_EXPIES / 60)],
	# 	               1)
	# 	return jsonify(error_num=RET.OK, errmsg="短信发送成功")
	# except Exception as e:
	# 	logg.error("异步发送邮件失败, 使用同步发送邮件")
	
	# 同步发送邮件
	try:
		from ihome.constants import MSG_CODE_REDIS_EXPIES  # 提取配置文件的设置
		from ihome.libs.Send_SMS.Demo_Send import CCP
		ccp = CCP.instance()
		res = ccp.sendTemplateSMS(phone_nums, [sms_code, int(MSG_CODE_REDIS_EXPIES/60)], 1)  # 5是有效期, 1是模板
	
	except Exception as e:
		logg.error("注册时, 保存短信验证码异常2")
		logg.error(e)
		return jsonify(error_num=RET.DBERR, errmsg="保存短信验证码异常")

	if res:
		# 发送成功
		return jsonify(error_num=RET.OK, errmsg="短信发送成功")
	else:
		return jsonify(error_num=RET.THIRDERR, errmsg="短信发送失败")