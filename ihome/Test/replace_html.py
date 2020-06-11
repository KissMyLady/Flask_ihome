# 文件名: Flask_Project_Code -> replace_html
# 创建时间: 2020/6/8 8:53
# 描述: 替换html中的特定字符
import sys
import re
sys.argv[1]
path = r'H:\我的文档\编程学习文档__集合\50--发布房源----提交房屋基本信息与图片逻辑处理.html'

try:
	f = open(path, 'r', encoding='utf-8')
	data = f.read()
	
except Exception as e:
	pass

finally:
	f.close()
	
cc = re.sub(pattern='H:/我的文档/cut_up/typoer_img/', repl='/static/images/note_imf/', string=data)
print(cc)

with open(path, 'w', encoding='utf-8') as f:
	f.write(cc)