#coding=utf8
import math

class Segment(object):
	"""docstring for Segment"""
	def __init__(self, totalCount, tax = 0):
		super(Segment, self).__init__()
		self.tax = tax
		self.totalCount = totalCount
		self.curCount = 0

	def getIntroduce(self):
		return u'分批次'

	def isFullCount(self):
		if self.curCount >= self.totalCount:
			return True

		return False

	def getCurCount(self):
		return self.curCount

	def reset(self):
		self.curCount = 0

	# 计算当前需要买多少手
	def getBuyStockCount(self, params):
		price = float(params['price'])
		baseAsset = params['baseAsset']
		
		# money = self.fun1(baseAsset)
		# money = self.fun2(baseAsset)
		money = self.fun3(baseAsset)
		count = self.getMaxCount(price, money)
		
		return count, count * price * (1 + self.tax)

	def fun1(self, baseAsset):
		return baseAsset / self.totalCount

	def fun2(self, baseAsset):
		m = 0.06
		b = 0.08
		rate = m * self.curCount + b

		return baseAsset * rate

	def fun3(self, baseAsset):
		m = -0.06
		b = 0.32
		rate = m * self.curCount + b

		return baseAsset * rate

	# 购买后的回调
	def buyCallBack(self):
		self.curCount = self.curCount + 1

	# 出售后的回调
	def sellCallBack(self):
		self.reset()

	def reset(self):
		self.curCount = 0

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

