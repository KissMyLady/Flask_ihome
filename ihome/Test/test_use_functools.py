# 创建时间: 2020/6/1 7:44
import functools


def login_required(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		pass
	return wrapper


@login_required
def mylady():
	"""mylayd python"""
	pass

print(mylady.__name__)
print(mylady.__doc__)
