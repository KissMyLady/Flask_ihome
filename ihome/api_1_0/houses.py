# 文件名: Flask_Project_Code -> houses
# 创建时间: 2020/6/6 16:22
from . import api_1_0
from ihome.utils.response_code import RET
from ihome.utils.use_logging import Use_Loggin
from ihome import redis_store, db
from flask import request, g
from flask import jsonify, session
from ihome.models import Area, House, Facility, HouseImage, User, Order
from ihome.utils.commons_self_re_path import login_required
from ihome import constants
import json
from datetime import datetime
from flask import render_template


# 描述: 获取城区分类信息
# 使用redis作为缓存, 保存十来个地区数据
@api_1_0.route("/areas", methods=["GET"])
def ger_area_info():
	logging = Use_Loggin()
	# 尝试从redis读取数据
	try:
		resp_json = redis_store.get("area_info")
	except Exception as e:
		logging.error(e)
	else:
		if resp_json is not None:
			logging.info("hit redis: redis有地区数据")
			return resp_json, 200, {"Content-Type": "application/json"}
		else:
			pass
		
	# 获取城区信息, 不需要前端的参数, 查询数据库
	try:
		areas_li = Area.query.all()
	except Exception as e:
		logging.error("数据库错误")
		return jsonify(errno=RET.DBERR, errmsg="城区-数据库查询错误")
	
	area_dict_li = list()
	for area in areas_li:
		area_dict_li.append(area.to_dict())
	
	# 转换成json字符串, 将数据保存到redis中, 整体存取
	res_dict = dict(errno=RET.OK, errmsg="OK", data=area_dict_li)
	resp_json = json.dumps(res_dict)
	
	# 保存到redis
	try:
		from ihome import constants
		redis_store.setex("area_info", value=resp_json, time=constants.EREA_INFO_CACHE_EXPIRES)
	except Exception as e:
		logging.warning("警告: json保存redis失败, 跳过")
	
	return resp_json, 200, {"Content-Type": "application/json"}


# 保存发布房屋信息接口
@api_1_0.route("/houses/info", methods=["POST"])
@login_required
def send_houses_info():
	'''
    前端发送过来的json数据
    {
        "title":"",
        "price":"",
        "area_id":"1",
        "address":"",
        "room_count":"",
        "acreage":"",
        "unit":"",
        "capacity":"",
        "beds":"",
        "deposit":"",
        "min_days":"",
        "max_days":"",
        "facility":["7","8"]
    }
	'''
	logging = Use_Loggin()
	# 获取参数
	user_id = g.user_id
	house_dict = request.get_json()
	
	title = house_dict.get("title")
	price = house_dict.get("price")
	area_id = house_dict.get("area_id")
	address = house_dict.get("address")
	room_count = house_dict.get("room_count")
	acreage = house_dict.get("acreage")
	unit = house_dict.get("unit")  # 房屋布局
	capacity = house_dict.get("capacity")  # 房屋容纳数量
	beds = house_dict.get("beds")
	deposit = house_dict.get("deposit")  # 押金
	min_days = house_dict.get("min_days")
	max_days = house_dict.get("max_days")
	facility_ids = house_dict.get("facility")  # 设施可能是空
	
	# 校验参数, facility另外校验
	if not all([title, price, area_id, address, room_count, acreage, unit,
	            capacity, beds, deposit, min_days, max_days]):
		return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
	
	# 金额校验
	try:
		price = int(float(price) * 100)
		deposit = int(float(deposit) * 100)
	except Exception as e:
		return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
	
	# 校验城区id是否存在
	try:
		area_sql_id = Area.query.get(area_id)
	except Exception as e:
		area_sql_id = None
	if area_sql_id is None:
		return jsonify(errno=RET.PARAMERR, errmsg="城区信息有误")
	
	# 其他--校验--略
	
	# 保存数据
	house = House(user_id=user_id,
	              area_id=area_id,
	              title=title,
	              price=price,
	              address=address,
	              room_count=room_count,
	              acreage=acreage,
	              unit=unit,
	              capacity=capacity,
	              beds=beds,
	              deposit=deposit,
	              min_days=min_days,
	              max_days=max_days)
	
	# 仅仅保存到session, 不报错
	db.session.add(house)
	
	# 处理房屋的设施信息,
	if facility_ids is not None:
		# ['7', '8']
		try:
			facility_obj = Facility.query.filter(Facility.id.in_(facility_ids)).all()
		except Exception as e:
			logging.error("设备信息数据库查询异常")
			return jsonify(errno=RET.DBERR, errmsg="数据库查询异常")
		
		if facility_obj:
			# 有合法的设施数据
			house.facilities = facility_obj
	
	try:
		db.session.add(house)
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		logging.error("数据库保存失败")
		return jsonify(errno=RET.DBERR, errmsg="房屋信息统一提交数据失败")
	
	return jsonify(errno=RET.OK, errmsg="保存数据成功", data={"house_id": house.id})


# 保存房屋图片
@api_1_0.route("/houses/image", methods=["POST"])
@login_required
def save_house_img():
	logging = Use_Loggin()
	
	# 获取参数
	# <input type="file" accept="image/*" name="house_image" id="house-image">
	# <input type="hidden" name="house_id" id="house-id" value="">
	raw_image_file = request.files.get("house_image")
	house_id = request.form.get("house_id")
	
	# 校验
	if not all([raw_image_file, house_id]):
		return jsonify(errno=RET.PARAMERR, errmsg="参数不完整1")

	# 判断house_id正确性
	try:
		house = House.query.get(house_id)
	except Exception as e:
		return jsonify(errno=RET.NODATA, errmsg="数据库查询房屋id失败, 请稍后再试")
	
	if house_id is None:
		return jsonify(errno=RET.NODATA, errmsg="房屋id不存在")
	
	image_data = raw_image_file.read()
	try:
		from ihome.utils.updown_image.seven_ox_coludy import down_load_of_Binary
		house_image_name = down_load_of_Binary(image_data)
	except Exception as e:
		logging.error("七牛云图片上传失败")
		return jsonify(errno=RET.THIRDERR, errmsg="上传失败3")
	
	# 保存数据
	house_image = HouseImage(house_id=house_id, url=house_image_name)
	db.session.add(house_image)
	
	# 处理房屋的主图片
	'''
	在第一次保存时, 设置了主图片为保存图片
	如果是多次设置, 应该重写写接口设置为主图片 ?
	'''
	if house.index_image_url is None or not house.index_image_url:
		house.index_image_url = house_image_name
		db.session.add(house)
		
	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		logging.error("数据库保存房屋图片信息异常")
		return jsonify(errno=RET.DATAERR, errmsg="数据库保存失败")
	
	image_url = constants.URL_OF_QINIU_IMAGE_PREFIX + house_image_name
	return jsonify(errno=RET.OK, errmsg="OK", data={"image_url": image_url})


# 获取房东发布的房源信息条目
@api_1_0.route("/user/houses", methods=["GET"])
@login_required
def get_user_house():
	logging = Use_Loggin()
	user_id = g.user_id
	try:
		user = User.query.get(user_id)
		houses = user.houses
	except Exception as e:
		logging.error("数据库查询房东信息错误1")
		return jsonify(errno=RET.DBERR, errmsg="获取数据失败")
	
	# 将查询到的数据转成dict放到list中
	houses_li = list()
	if houses:
		for house in houses:
			houses_li.append(house.to_base_dict())  # 数据库的基本信息
	return jsonify(errno=RET.OK, errmsg="OK", data={"houses": houses_li})


# 获取主页幻灯片展示的房屋基本信息
@api_1_0.route("/houses/index", methods=["GET"])
@login_required
def get_house_info():
	logging = Use_Loggin()
	# 尝试从缓存中读取
	try:
		req_data = redis_store.get("home_page_data")
	except Exception as e:
		logging.error("redis获取index缓存数据错误")
		req_data = None
	
	if req_data:
		logging.info("hit index page redis")
		# logging.info(req_data.decode("utf-8"))
		req_data = req_data.decode("utf-8")
		req = '{"errno":0, "errmsg":"OK", "data":%s}' % req_data, 200, {"Content-Type": "application/json"}
		print("req /house/index:", req)
		print("req type(req): ", type(req))
		return req

	else:
		pass
	
	# redis没有数据, 数据库读取
	try:
		# 返回房屋订单数目最多的5条数据
		houses = House.query.order_by(House.order_count.desc()).limit(constants.HOME_PAGE_MAX_HOUSES)
	except Exception as e:
		logging.error("数据库--查询房屋订单数失败")
		return jsonify(errno=RET.DBERR, errmsg="查询失败")
	
	if not houses:
		return jsonify(errno=RET.NODATA, errmsg="没有数据")
	
	# 有多个房源信息, 用list作为容器,
	house_img_li = list()
	for house in houses:
		# logging.info(house.to_base_dict())
		# {'house_id': 4, 'title': '123',
		# 'price': 12300, 'area_name': '海淀区', 'img_url': '',
		# 'room_count': 123, 'order_count': 0, 'address': '123',
		# 'user_avatar': 'http://qbg25zlw0.bkt.clouddn.com/FnNBWGcBkB9G3UamXjtfqnnD9lFM',
		# 'ctime': '2020-06-08'}
		house_img_li.append(house.to_base_dict())
	
	# 将数据转成json(耗时), 并保存到redis
	json_houses = json.dumps(house_img_li)  # '[{}, {}, {}]'
	try:
		redis_store.setex("home_page_data", value=json_houses, time=constants.HOME_PATH_REDIS_CACHE_EXPIRES)
	except Exception as e:
		logging.error("redis保存缓存失败")
	
	# return jsonify(errno=RET.OK, errmsg="OK", data={"data":json_houses}) 耗时
	req2 = '{"errno"=0, "errmsg"="OK", "data":%s}' % json_houses, 200, {"Content-Type": "application/json"}
	return req2


# 获取房屋详情页面
@api_1_0.route("/houses/<int:house_id>", methods=['GET'])
def get_house_detail(house_id):
	"""
	前端在房屋详情页面展示时，如果浏览页面的用户不是该房屋的房东，则展示预定按钮，否则不展示
	"""
	logging = Use_Loggin()
	# 尝试获取用户登录的信息，若登录，则返回给前端登录用户的user_id，否则返回user_id=-1
	user_id = session.get("user_id", "-1")
	if not house_id:
		return jsonify(errno=RET.PARAMERR, errmsg="参数缺失")
	
	# 从redis提取数据
	try:
		ret = redis_store.get("house_info_%s" % house_id)
	except Exception as e:
		ret = None
		logging.warning(e)
	
	if ret:
		logging.info("hit house info redis")
		ret = ret.decode("utf-8")
		resp = '{"errno":0, errmsg:"OK", "data":{"user_id":%s, "house":%s}}' % (user_id, ret), 200, {"Content-Type": "application/json"}
		return resp
	
	# 如果redis没有数据, 查询数据库--用户未登录也会使用sql查询
	try:
		house = House.query.get(house_id)  # 查询是不是房东在访问
		logging.info("缓存无数据, 从sql中提取")
	except Exception as e:
		logging.error("数据库查询用户登录信息错误")
		return jsonify(errno=RET.DBERR, errmsg="查询错误")
	
	if not house:
		return jsonify(errno=RET.NODATA, errmsg="数据不存在")


	try:
		house_data = house.full_info_dict()
	except Exception as e:
		logging.error("数据库查询失败2")
		return jsonify(errno=RET.DATAERR, errmsg="查询错误2")
	
	json_house = json.dumps(house_data)
	try:
		redis_store.setex("house_info_%s" % user_id, value=json_house, time=constants.HOUSE_DETAIL_REDIS_CACHE_EXPIRES)
	except Exception as e:
		logging.error("Reids保存缓存错误")
	
	test_li = list()
	for i in range(25):
		a = {"%s"%i : "%s"%i}
		test_li.append(a)
	
	test_json = json.dumps(test_li)
	resp2 = '{"errno":"0", "errmsg":"OK", "data":{"user_id":%s, "house":%s, "test_json":%s}}' % (user_id, json_house, test_json), 200, {"Content-Type": "application/json"}
	return resp2  # 返回信息


# 房屋搜索页面
# GET /api/v1.0/houses?sd=2017-12-01&ed=2017-12-31&aid=10&sk=new&p=1
@api_1_0.route("/house/search")
def search_house():
	logging = Use_Loggin()
	
	# 获取参数, 可有可无
	# http://127.0.0.1:5000/search.html?aid=1&aname=%E4%B8%9C%E5%9F%8E%E5%8C%BA&sd=2020-06-23&ed=2020-07-25
	start_date = request.args.get(key="sd", default="")   # 用户想要的起始时间  sd=2020-06-23
	end_date = request.args.get(key="ed", default="")     # 结束时间          ed=2020-07-25
	area_id = request.args.get(key="aid", default="")     # 区域编号          aname=东城区
	sort_key = request.args.get(key="ks", default="new")  # 排序关键字
	page = request.args.get(key="p", default="")  # 页数
	
	print("1 start_date: ", start_date, type(start_date))
	print("1 end_date: ", end_date, type(end_date))
	print("1 area_id: ", area_id, type(area_id))
	print("1 sort_key: ", sort_key, type(sort_key))
	print("1 page: ",page , type(page))
	
	# 因为参数可传可不传, 所以这里参数校验没必要
	
	# try:
	# 	if start_date is not None:
	# 		start_date = datetime.strftime(start_date, "%Y-%m-%d")
	# 		print("start_date 2: ", start_date)
	# 	if end_date is not None:
	# 		end_date = datetime.strftime(end_date, "%Y-%m-%d")
	# 		print("end_date 2: ", end_date)
	#
	# 	if start_date and end_date  is not None:
	# 		assert end_date <= start_date
	#
	# except Exception as e:
	# 	return jsonify(errno=RET.PARAMERR, errmsg="日期输入有误")
	
	# 区域判断
	try:
		areas = Area.query.get(area_id)
	except Exception as e:
		return jsonify(errno=RET.PARAMERR, errmsg="区域信息有误")

	# 处理页数
	try:
		page = int(page)
	except Exception as e:
		page = 1
	
	# 查询数据库
	# 获取缓存数据 存储每个搜索组合, 增加内存开销
	redis_key = "house_%s_%s_%s_%s" % (start_date, end_date, area_id, sort_key)
	try:
		resp_json = redis_store.hget(redis_key, page)
	except Exception as e:
		resp_json = None
		logging.error("reids 获取缓存失败")
	else:
		if resp_json:
			return resp_json, 200, {"Content-Type": "application/json"}
	
	# 过滤条件的参数列表容器
	filter_params = list()
	
	# 形成参数:　填充过滤参数　时间条件
	conflict_orders = None
	try:
		if start_date and end_date:
			# 查询冲突的订单　　
			conflict_orders = Order.query.filter(Order.begin_date <= end_date, Order.end_date >= start_date).all()
		elif start_date:
			conflict_orders = Order.query.filter(Order.end_date >= start_date).all()
		elif end_date:
			conflict_orders = Order.query.filter(Order.begin_date <= end_date).all()
			
	except Exception as e:
		logging.error("Order数据库查询错误")
		return jsonify(errno=RET.DBERR, errmsg="数据库异常")
	
	if conflict_orders:
		# 从订单中获取冲突的房屋id
		conflict_house_ids = [order.house_id for order in conflict_orders]
		
		# 如果冲突的房屋id不为空，向查询参数中添加条件
		if conflict_house_ids:
			filter_params.append(House.id.notin_(conflict_house_ids))
	
	# 区域条件
	if area_id:
		# 放进去的是表达式: __eq__()方法的执行
		filter_params.append(House.area_id == area_id)
		
	# 查询数据库
	# 补充排序条件
	if sort_key == "booking":  # 入住做多
		house_query = House.query.filter(*filter_params).order_by(House.order_count.desc())
	elif sort_key == "price-inc":
		house_query = House.query.filter(*filter_params).order_by(House.price.asc())
	elif sort_key == "price-des":
		house_query = House.query.filter(*filter_params).order_by(House.price.desc())
	else:  # 新旧
		house_query = House.query.filter(*filter_params).order_by(House.create_time.desc())
	
	# 处理分页
	try:
		#                               当前页数          每页数据量                               自动的错误输出
		page_obj = house_query.paginate(page=page, per_page=constants.HOUSE_LIST_PAGE_CAPACITY, error_out=False)
	except Exception as e:
		logging.error("数据库查询错误")
		return jsonify(errno=RET.DBERR, errmsg="数据库异常")
	
	# 获取页面数据
	house_li = page_obj.items
	houses = []
	for house in house_li:
		houses.append(house.to_base_dict())
	
	# 获取总页数
	total_page = page_obj.pages
	
	resp_dict = dict(errno=RET.OK, errmsg="OK",
	                 data={"total_page": total_page,
	                       "houses": houses,
	                       "current_page": page})
								
	resp_json = json.dumps(resp_dict)
	
	if page <= total_page:
		# 设置缓存数据
		redis_key = "house_%s_%s_%s_%s" % (start_date, end_date, area_id, sort_key)
		# 哈希类型
		try:
			# redis_store.hset(redis_key, page, resp_json)
			# redis_store.expire(redis_key, constants.HOUES_LIST_PAGE_REDIS_CACHE_EXPIRES)
			
			# 创建redis管道对象，可以一次执行多个语句
			pipeline = redis_store.pipeline()
			
			# 开启多个语句的记录
			pipeline.multi()
			
			pipeline.hset(redis_key, page, resp_json)
			pipeline.expire(redis_key, constants.HOUES_LIST_PAGE_REDIS_CACHE_EXPIRES)
			
			# 执行语句
			pipeline.execute()
		except Exception as e:
			logging.error("redis设置错误")
			
	return resp_json, 200, {"Content-Type": "application/json"}

