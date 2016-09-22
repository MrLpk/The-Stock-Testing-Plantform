#coding=utf8
# from BaseData import BaseData
import math

class Elephant(object):
	"""docstring for Elephant"""
	def __init__(self, tax = 0):
		super(Elephant, self).__init__()
		self.tax = tax

	def getIntroduce(self):
		return '奔放买法'

	# 计算当前需要买多少手
	def getBuyStockCount(self, params):
		price = float(params['price'])
		money = params['money']
		count = self.getMaxCount(price, money)
		return count, count * price * (1 + self.tax)

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

