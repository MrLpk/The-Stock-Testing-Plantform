#coding=utf8
# 月版本数据
from BaseData import BaseData

class StockEdit(object):
	"""docstring for StockEdit"""
	def __init__(self, code, edit = None):
		super(StockEdit, self).__init__()
		self.code = code
		self.edit = edit
		self.stockDatas = []
		self.create()

	def create(self):
		path = self.getPath(self.code)
		lines = open(path, 'r').readlines()
		monthData = None
		for lineCount, line in enumerate(lines):
			words = line.split(',')
			if not len(words) == 7:
				continue
			data = BaseData(0, words[0], words[1], words[2], words[3], words[4], words[5], words[6].rstrip())

			key = data.getYM()

			if monthData == None or key in monthData:
				monthData = {key:data}
			elif not key in monthData:
				self.stockDatas.append(monthData.values()[0])
				monthData = {key:data}

			

	def getDatas(self):
		return self.stockDatas
		
	# 根据name生成路径
	def getPath(self, name):
		import os
		path = 'Smaug/%s.txt' %name

		if os.path.isfile(path):
			return path
		else:
			raise TypeError(path)

	def log(self):
		for x in self.getDatas():
			print x.getDate(), x.end
		