# coding=utf-8
# 文件名: Flask_Project_Code -> Send_Temp
# 创建时间: 2020/6/3 10:57

import sys
sys.path.append("..")

from Cloudy_SMG import send_msg
# import ConfigParser    # 官网sdk带的，没有使用

# 账号id
accountSid = '8aaf07087249953401727761ea6d1662'  # 8aaf07087249953401727761ea6d1662
# 账号Token
accountToken = 'a55b30d921814c0f9fff0619889335d1'  # a55b30d921814c0f9fff0619889335d1
# 应用Id
appId = '8aaf07087249953401727761eb6c1669'  # token请自行去官网申请  # 8aaf07087249953401727761eb6c1669
# 服务地址
serverIP = 'app.cloopen.com'
# 服务端口
serverPort = '8883'
# REST版本
softVersion = '2013-12-26'

'''
ACCOUNT SID：  8aaf07087249953401727761ea6d1662
(主账户ID)
AUTH TOKEN：   a55*******35d1查看
(账户授权令牌)
Rest URL(生产)：  https://app.cloopen.com:8883
AppID(默认)：   8aaf07087249953401727761eb6c1669未上线
(APP TOKEN 请到应用管理中获取)
鉴权IP：
已开启IP设置

'''


class CCP(object):
	def __init__(self):
		# send_msg.REST
		self.rest = send_msg.REST(serverIP, serverPort, softVersion)
		self.rest.setAccount(accountSid, accountToken)
		self.rest.setAppId(appId)
	
	@staticmethod
	def instance():
		if not hasattr(CCP, "_instance"):
			CCP._instance = CCP()
		return CCP._instance
	
	def sendTemplateSMS(self, to, datas, tempId):
		try:
			result = self.rest.sendTemplateSMS(to, datas, tempId)
		except Exception as e:
			try:
				from ihome.utils.use_logging import Use_Loggin
				logg = Use_Loggin()
				logg.error(e)
				logg.error("短信发送错误, 请查看Send_Temp模块是否有误")
			except:
				print("logg模块导入错误, 请查看是否有误")
				
			raise e
		success = "<statusCode>000000</statusCode>"
		if success in result:
			return True
		else:
			return False


if __name__ == "__main__":
	ccp = CCP.instance()
	res = ccp.sendTemplateSMS("13207297072", ["1234", 5], 1)
	print(res)
	
	'''
	这是请求的URL：
	https://app.cloopen.com:8883/2013-12-26/Accounts/xxxxxx/SMS/TemplateSMS?sig=B90B42C4C5DCDAAD5F5D9BAAB9559624
	这是请求包体:
	<?xml version="1.0" encoding="utf-8"?><SubAccount><datas><data>1234</data><data>5</data></datas><to>185xxxxxxxx</to><templateId>1</templateId><appId>xxxxxx</appId>            </SubAccount>
	这是响应包体:
	<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<Response>
	    <statusCode>111141</statusCode>
	    <statusMsg>【账号】主账户不存在</statusMsg>
	</Response>
	
	********************************
	False
	
	'''