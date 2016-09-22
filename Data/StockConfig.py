#coding=utf8
import json
class StockConfig(object):
	"""docstring for StockConfig"""
	def __init__(self):
		super(StockConfig, self).__init__()
		self.datas = {}
		self.ignore = []
		try:
			content = open('Data/Config.txt').read()
			self.datas = json.loads(content)
		except Exception, e:
			pass

		if 'ignore' in self.datas:
			self.ignore = self.datas['ignore']
		else:
			self.datas['ignore'] = self.ignore

		self.specialIdx = [
			'SH000001',
			'SH000016',
			'SH000010',
			'SZ399001',
			'SZ399395',
			'SZ399970',
			'SZ399975',
			'SZ399973',
			'SZ399991',
			'SZ399997',
			'SZ399976',
			'SZ399958',
			'SZ399959',
			'SZ399393',
			'SZ399440',
			'SZ399004',
			'SZ399805',
			'SH000998',
			'SZ399967',
			'SZ399707',
			'SZ399394',
			'SZ399989',
			'SZ399412',
			'SZ399986',
			'SZ399673',
			]

	# 获取股票类型
	# -1 没有该股票记录
	# 0 股票
	# 1 基金
	# 2 指数
	def getTypeByCode(self, code):
		for _idx in self.specialIdx:
			if _idx == code:
				return 2

		if code in self.datas:
			return self.datas[code]

		return -1

	def update(self, array):
		for _array in array:
			key = _array.keys()[0]
			if not key in self.datas:
				self.datas[key] = _array[key]
		self.save()

	def isIgnore(self, code):
		return code in self.ignore

	def removeIgnore(self, code):
		for _index, _code in enumerate(self.ignore):
			if _code == code:
				del self.ignore[_index]
				break

	def save(self):
		fh = open('Data/Config.txt', 'w') 
		fh.write(json.dumps(self.datas)) 
		fh.close()

	# def save(self, code, type):
	# 	pass