#coding=utf8

from BaseData import BaseData
import math
''' Turtle '''

class Turtle(object):
	"""docstring for Turtle"""
	def __init__(self, atrKey = '0', tax = 0):
		super(Turtle, self).__init__()
		self.atrKey = atrKey # atr key
		self.tax = tax

	def getIntroduce(self):
		return '海龟买法'

	# 计算当前需要买多少手
	def getBuyStockCount(self, data, money):
		atr = data.atr[self.atrKey]
		count = self.fixStockCount(money / 100 / atr)
		maxCount = self.getMaxCount(data.end, money)

		if count > maxCount:
			count = maxCount

		return count, count * float(data.end) * (1 + self.tax)

	# 最大购买数
	def getMaxCount(self, price, money):
		price = float(price)
		return self.fixStockCount( money / price / (1 + self.tax))

	# 把数字修正为100的倍数，不足100返回100
	def fixStockCount(self, stockCount):
		stockCount = int(math.floor(stockCount))

		if stockCount < 100:
			return 100

		num = stockCount % 100

		if num == 0:
			return stockCount
		else:
			return stockCount - num