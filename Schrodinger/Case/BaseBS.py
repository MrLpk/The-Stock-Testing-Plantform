#coding=utf8
from Formula import Formula

class BaseBS(object):
	"""docstring for BaseBS"""
	def __init__(self):
		super(BaseBS, self).__init__()
		self.formulas = []

	def getIntroduce(self):
		introduce = ''
		for f in self.formulas:
			introduce = introduce + f.getMsg() + '\n'
		return introduce

	def check(self, obj):
		LIMIT_UP = 0
		LIMIT_DOWN = 6
		MASK = 7
		for f in self.formulas:
			resutl = f.check(obj)

			if resutl['r']:
				if f.getIndex() == LIMIT_UP or f.getIndex() == LIMIT_DOWN or f.getIndex == MASK:
					return {'r':False}

				return resutl

		return {'r':False}