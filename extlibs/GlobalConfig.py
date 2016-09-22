#coding=utf8
from Singleton import Singleton

class GlobalConfig(Singleton):
	"""docstring for GlobalConfig"""
	def __init__(self):
		super(GlobalConfig, self).__init__()
		self.checkAttr('cfg', {})

	def set(self, key, value):
		self.cfg[key] = value

	def get(self, key):
		return self.cfg[key] if key in self.cfg else None

	def log(self):
		print 'Data in GlobalConfig:'
		for key in self.cfg:
			print key + ' : ' + self.cfg[key]

class MyClass(Singleton):  
	a = 1  

if __name__ == '__main__':
	cfg = GlobalConfig()
	cfg.set('name', 'aaa')
	aa = GlobalConfig()
	cfg.set('namea', 'bb')
	print aa.get("name")
	print aa.get("namea")

	print id(cfg)
	print id(aa)

	# one = MyClass()  
	# two = MyClass()  

	# two.a = 3  
	# print one.a 