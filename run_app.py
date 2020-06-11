# 文件名: Flask_Project_Code -> run_app
# 创建时间: 2020/6/10 11:26

from flask import Flask

app = Flask(__name__)


@app.route("/")
def test():
	return "ok"


if __name__ == '__main__':
	app.run()