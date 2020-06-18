# 文件名: Flask_Project_Code -> path_test
# 创建时间: 2020/6/13 11:09

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
alipay_public_key_path = os.path.join(os.path.join(BASE_DIR, "keys_pay"), 'alipay_publice_key.pem')
app_private_key_path = os.path.join(BASE_DIR, "keys_pay") + r'\app_private_key.pem'

print(alipay_public_key_path)
print(app_private_key_path)