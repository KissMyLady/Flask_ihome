# 文件名: Flask_Project_Code -> sms_send_tasks
# 创建时间: 2020/6/8 14:06
from celery import Celery
from ihome import constants
from ihome.libs.Send_SMS.Demo_Send import CCP
import os

sms_celery = Celery("ihome", broker="redis://127.0.0.1:6379/1")

# os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')


# 发送短信的异步任务
@sms_celery.task
def send_sms(to, datas, template_id):
	print("to, data, template_id=1: ", to, datas, template_id)
	ccp = CCP.instance()
	ccp.sendTemplateSMS(to, datas, template_id)
	# return res


















