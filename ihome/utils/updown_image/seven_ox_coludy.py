# 文件名: Flask_Project_Code -> seven_ox_coludy
# 创建时间: 2020/6/5 19:41
# 文件名: Flask_Project_Code -> qiniu_test
# 创建时间: 2020/6/5 16:39

# python开发者文档: https://developer.qiniu.com/kodo/sdk/1242/python
# 查看密匙:  https://portal.qiniu.com/user/key


def down_load():
	# flake8: noqa
	from qiniu import Auth, put_file, etag
	import qiniu.config
	
	# 需要填写你的 Access Key 和 Secret Key
	access_key = "LfXjXvG1e6vPXV2UFLfXrJ14uNM792vqONhnLyB2"
	secret_key = "MRL5Y67LWpl_9_pOUPa7OvSY-t8OD9R2pR3luUA_"
	
	# 构建鉴权对象
	q = Auth(access_key, secret_key)
	
	# 要上传的空间
	bucket_name = 'flask-ihome-python65'
	
	# 上传后保存的文件名 可以指明, 也可以不指明(计算结果值当作文件名)
	key = 'my-python-logo.png'
	
	# 生成上传 Token，可以指定过期时间等
	token = q.upload_token(bucket_name, key, 3600)
	
	# 要上传文件的本地路径
	localfile = r'H:\我的文档\me_information\无花果.jpg'
	ret, info = put_file(token, key, localfile)
	print("info:", info)
	print(" ")
	assert ret['key'] == key
	assert ret['hash'] == etag(localfile)
	'''
	_ResponseInfo__response:<Response [200]>,
	exception:None,
	status_code:200,

	text_body:{
	"hash":"FrdIFHYRII6dB2-FQaxWuZ8kOHxs",
	"key":"my-python-logo.png"},

	req_id:R4MAAACP3SZjmRUW,
	x_log:X-Log
	'''


def down_load_of_Binary(file_data):
	'''
	上传文件到七牛
	:param file_data: 要上传的文件数据
	:return:
	'''
	from qiniu import Auth, etag, put_data
	access_key = "LfXjXvG1e6vPXV2UFLfXrJ14uNM792vqONhnLyB2"
	secret_key = "MRL5Y67LWpl_9_pOUPa7OvSY-t8OD9R2pR3luUA_"
	
	q = Auth(access_key, secret_key)
	
	# 上传后保存的文件名 可以指明, 也可以不指明(计算结果值当作文件名)
	# key = 'my-python-logo.png'
	keys = None
	
	# 生成上传 Token，可以指定过期时间等
	token = q.upload_token('flask-ihome-python65', key=keys, expires=3600)
	
	# 要上传文件的本地路径
	ret, info = put_data(token, key=keys, data=file_data)
	# print("info:", info)
	# print("-" * 20)
	# print(ret)
	if info.status_code == 200:
		# 上传成功, 返回文件名
		return ret.get("key")
	else:
		# 上传失败
		raise Exception("图片上传服务器失败")

'''
info: _ResponseInfo__response:                      info
<Response [200]>,
exception:None,
status_code:200,
text_body:{"hash":"FikUyrLA_3Oaf7XJfBFOCbbkgU5J",
"key":"FikUyrLA_3Oaf7XJfBFOCbbkgU5J"},
req_id:K7IAAAAk4lmMmhUW, x_log:X-Log
--------------------                                ret
{'hash': 'FikUyrLA_3Oaf7XJfBFOCbbkgU5J',
 'key':  'FikUyrLA_3Oaf7XJfBFOCbbkgU5J'}
'''


# 直接敲入 hash值即可查看图片:  http://qbg25zlw0.bkt.clouddn.com/FikUyrLA_3Oaf7XJfBFOCbbkgU5J


if __name__ == "__main__":
	# 上传文件
	# down_load()
	
	localfile = r'H:\我的文档\cut_up\test文件.png'
	with open(localfile, "rb") as f:
		binary_img = f.read()
		down_load_of_Binary(binary_img)