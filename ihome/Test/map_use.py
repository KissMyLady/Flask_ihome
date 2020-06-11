# 文件名: Flask_Project_Code -> map_use
# 创建时间: 2020/6/8 8:20

li1 = [1, 2, 3, 4, 5, 6]
li2 = [2, 4, 5, 6, 7, 9]


def add_self(num1, num2):
	return num1 + num2


def add_func(x):
	return x + x


map_d = map(add_self, li1, li2)

#for i in map(add_func, li1):
	#print(i)

for i in map_d:
	print(i)
# print(list(map_d))
'''
2
4
6
8
10
12
[3, 6, 8, 10, 12, 15]
'''