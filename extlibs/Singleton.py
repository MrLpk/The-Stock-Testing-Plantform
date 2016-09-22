#coding=utf8

class Singleton(object):  
	def __new__(cls, *args, **kw):  
		if not hasattr(cls, '_instance'):  
			orig = super(Singleton, cls)  
			cls._instance = orig.__new__(cls, *args, **kw)  
		return cls._instance  

	def checkAttr(self, name, default):
		if not hasattr(self, name):
			setattr(self, name, default)

class MyClass(Singleton):  
	def __init__(self):
		super(MyClass, self).__init__()
		self.checkAttr('abc', 'abc')
  
if __name__ == '__main__':
	one = MyClass()  	
	print one.abc
	one.abc = 'ff'
	two = MyClass()  
	# two.abc = 'dd'

  
	print two.abc