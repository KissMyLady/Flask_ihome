# 文件名: Flask_Project_Code -> py
# 创建时间: 2020/6/13 10:54
# 描述: 支付宝使用

from ihome.utils.commons_self_re_path import login_required
from ihome.utils.use_logging import Use_Loggin
from flask import g, jsonify, request
from ihome import db, redis_store
from ihome.models import Order
from ihome.utils.response_code import RET
from ihome import constants
import os
from ihome.api_1_0 import api_1_0
from alipay import AliPay


# 支付三方转发逻辑
@api_1_0.route("/orders/<int:order_id>/payment", methods=["POST"])
@login_required
def order_pay(order_id):
	logging = Use_Loggin()
	user_id = g.user_id
	
	# 判断订单状态: 存在, 在字符
	try:
		orders = Order.query.filter(Order.id == order_id,
		                            Order.user_id == user_id,
		                            Order.status=="WAIT_PAYMENT").first()
		sun_amonut = str(orders.amount/100.0)  # 总金额
		
	except Exception as e:
		logging.error("订单数据查询失败")
		return jsonify(errno=RET.DBERR, errmsg="订单-数据库异常2")
	
	if orders is None:
		return jsonify(errno=RET.NODATA, errmsg="订单-订单数据有误")
	
	# 路径拼接
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	alipay_public_key_path = os.path.join(os.path.join(BASE_DIR, "keys_pay"), 'alipay_public_key.pem')
	app_private_key_path = os.path.join(os.path.join(BASE_DIR, "keys_pay"),   'app_private_key.pem')

	# 读取密钥数据
	with open(alipay_public_key_path, "r", encoding="utf-8") as f:
		alipay_public_key_path_read = f.read()
	
	with open(app_private_key_path, "r", encoding="utf-8") as f:
		app_private_key_path_read = f.read()
	
	
	# 初始化阿里与支付模块
	alipay_client = AliPay(appid=constants.ALIPAY_APIT_NUMS,                      # 沙箱环境的apid
	                       app_notify_url=None,                                   # 回调, 不需要回调
	                       app_private_key_string=app_private_key_path_read,      # 给路径即可
	                       alipay_public_key_string=alipay_public_key_path_read,
	                       sign_type="RSA2",                                      # RSA或者 RSA2
	                       debug=False)                                           # 默认

	# 手机网站支付 需要跳转到 https://openapi.alipaydev.com/gateway.do + order_string
	order_string = alipay_client.api_alipay_trade_wap_pay(
		subject=u"爱家租房 %s" % order_id,  # 标题
		out_trade_no=order_id,             # 订单的编号
		total_amount=sun_amonut,           # 总金额
		return_url="http://127.0.0.1:5000/ordersComplete.html",  # 返回的链接地址
		notify_url=None,
	)
	
	# 构建用户跳转的支付宝链接地址
	pay_url = constants.ALIPAY_URL_DEV_PRIFIX + order_string
	
	# 把链接发给前端
	return jsonify(errno=RET.OK, errmsg="OK", data={"pay_url": pay_url})


# 回调函数, 验证是否支付成功
@api_1_0.route("/order/payment", methods=["PUT"])
def save_order_payment_result():
	"""保存订单支付结果"""
	logging = Use_Loggin()
	alipay_dict = request.form.to_dict()
	
	# 对支付宝的数据进行分离  提取出支付宝的签名参数sign 和剩下的其他数据
	alipay_signAture = alipay_dict.pop("sign")  # 计算结果是很长的字符串
	
	# 路径拼接
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	alipay_public_key_path = os.path.join(os.path.join(BASE_DIR, "keys_pay"), 'alipay_public_key.pem')
	app_private_key_path = os.path.join(os.path.join(BASE_DIR, "keys_pay"),   'app_private_key.pem')
	
	# 读取密钥数据
	with open(alipay_public_key_path, "r", encoding="utf-8") as f:
		alipay_public_key_path_read = f.read()
	
	with open(app_private_key_path, "r", encoding="utf-8") as f:
		app_private_key_path_read = f.read()
	
	# 初始化 SDK工具对象
	try:
		alipay_client = AliPay(appid=constants.ALIPAY_APIT_NUMS,
		                       app_notify_url=None,  # 默认回调url
		                       app_private_key_string=app_private_key_path_read,      # 私钥
		                       alipay_public_key_string=alipay_public_key_path_read,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
		                       sign_type="RSA2",     # RSA 或者 RSA2
		                       debug=False)          # 默认False
	except Exception as e:
		logging.error("112行, 订单信息回调信息获取失败, 请管理员注意")
		return jsonify(errno=RET.THIRDERR, errmsg="订单信息回调失败")
	
	# 借助工具验证参数的合法性
	# 如果确定参数是支付宝的，返回True，否则返回false
	try:
		result = alipay_client.verify(alipay_dict, alipay_signAture)
	except Exception as e:
		logging.error("支付回调失败")
		result = False
		return jsonify(errno=RET.THIRDERR, errmsg="支付错误")
		
	if result:
		# 修改数据库的订单状态信息
		order_id = alipay_dict.get("out_trade_no")
		trade_no = alipay_dict.get("trade_no")      # 支付宝的交易号
		# order_id trade_no:  9 2020061822001403580501092285
		try:                                                    # WAIT_COMMENT
			Order.query.filter_by(id=order_id).update({"status": "WAIT_COMMENT", "trade_no": trade_no})
			db.session.commit()
		except Exception as e:
			logging.error("逻辑区提取数据失败")
			db.session.rollback()

	return jsonify(errno=RET.OK, errmsg="OK")
