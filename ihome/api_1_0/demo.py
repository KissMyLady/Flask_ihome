# 创建时间: 2020/6/1 10:54
from flask import session
from flask import Blueprint
from . import api_1_0  # 导入init文件下的 Blueprint
from ihome import db
from ihome import models
from flask import render_template


# 将 route映射到 Blueprint中
@api_1_0.route("/set_session")
def set_session():
	session["good"] = "ok"
	session["nice"] = "man"
	return render_template
	# return "session is set ok <a href='/'>返回主页<>"


@api_1_0.route('/')
def hello_world():
	name = session.get("good")
	name2 = session.get("nice")
	return 'Hello World! %s %s' % (name, name2)
