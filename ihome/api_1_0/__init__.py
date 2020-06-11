# 创建时间: 2020/6/1 10:52

# API_1.0 版本
from flask import Blueprint

api_1_0 = Blueprint("v_0_1", __name__)

# 导入 demo中的视图函数, 让 Blueprint知道有这个函数存在(执行一遍)
# 个人理解, 视图函数相对来说, 属于 静态文件, 没有任何启动项, 需要外部文件启动
from .demo import set_session
from .demo import hello_world
from .verify_code import get_image_code
from . import profile
from . import houses
from .passport import *