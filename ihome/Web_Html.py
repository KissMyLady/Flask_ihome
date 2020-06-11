# 创建时间: 2020/6/2 7:08
from flask import Blueprint, current_app
from flask import make_response
from flask_wtf import csrf


# 提供静态文件的 Blueprint Web_Html
web_html = Blueprint("web_home", __name__)

# 127.0.0.1:5000/favicon.ico 浏览器通实, 浏览器会自己请求这个资源
# 127.0.0.1:5000/static/html/index.html -> 127.0.0.1/5000/index.html


# 设置访问静态资源--缩短路径
@web_html.route("/<repath(r'.*'):html_file_name>")
def get_html(html_file_name):
	print("html_file_name>>>", html_file_name)
	if not html_file_name:
		html_file_name = r"index.html"

	if html_file_name != "favicon.ico":
		html_file_name = r"html/" + html_file_name  # 固定访问路径

	# CSRF返回--创建一个CSRF的 TOKEN值
	csrf_token = csrf.generate_csrf()
	
	# 设置相应信息
	resp = make_response(current_app.send_static_file(html_file_name))
	
	resp.set_cookie("csrf_token", csrf_token)  # 将csrf设置在body的cookie中, js文件提取经常用到
	return resp
	# 127.0.0.1:5000/favicon.ico