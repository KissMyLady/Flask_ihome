# coding:utf-8
# 文件名: Flask_Project_Code -> constants
# 创建时间: 2020/6/2 16:38

# 保存常量数据


# 图片验证码信息 单位: 秒
IMAGE_CODE_REDIS_EXPIES = 180

# 短信验证码--有效时间:  单位: 秒 3分-5分
MSG_CODE_REDIS_EXPIES = 300

# 短信发送间隔时间
MSG_CODE_LONG_EXPIES = 60

# 登录--密码错过多误限制时间输入间隔
# 错误次数
LOGIN_MUNS_COUNTS = 5

# 用户登录输入多次错误后, 限制时间内访问
LOGIN_MUNS_NOTIME = 600

# 云平台, 图皮前面的url常量
URL_OF_QINIU_IMAGE_PREFIX = r"http://qbg25zlw0.bkt.clouddn.com/"

# 用户名长度设置, 小于
USER_SET_NAME_LENG = 9

# 用户名不能包括特殊字符
USER_SET_NAME_NOT_INCLUDE = ["!", "@", "#", "$", "%", "^", "^", "&",
                             "*", "(", ")", "\"", "\'", "_", "~", "`",
                             ".", ">", "<", "/", "\\", ",", " "]

# 城区分类中的redis缓存保存时间 单位: 秒
EREA_INFO_CACHE_EXPIRES = 7200

# 房屋详情页展示的评论最大数
HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS = 30

# 房屋详情页面reids缓存时间
HOUSE_DETAIL_REDIS_CACHE_EXPIRES = 7200

# 房屋最大订单数量
HOME_PAGE_MAX_HOUSES = 5

# 房屋主页--redis缓存失效时间
HOME_PATH_REDIS_CACHE_EXPIRES = 7200

# 房屋搜索列表缓存时间
HOUES_LIST_PAGE_REDIS_CACHE_EXPIRES = 7200

# 房屋列表页面每页数据容量
HOUSE_LIST_PAGE_CAPACITY = 2